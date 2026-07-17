from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Mapping

from .baseline import RobustEMA
from .metrics import GradientGeometry


class Mode(str, Enum):
    CALIBRATION = "calibration"
    NORMAL = "normal"
    DAMPED = "damped"
    RECOVERY = "recovery"
    COOLDOWN = "cooldown"


@dataclass
class ControllerConfig:
    calibration_steps: int = 100
    trigger_persistence: int = 3
    return_persistence: int = 8
    cooldown_steps: int = 20
    damp_threshold: float = 2.0
    recovery_threshold: float = 5.0
    return_threshold: float = 0.5
    lr_gain: float = 0.35
    momentum_gain: float = 0.2
    min_lr_scale: float = 0.1
    min_momentum_scale: float = 0.25
    max_update_norm: float = 1.0
    ema_beta: float = 0.02
    checkpoint_stability_steps: int = 5
    weights: Mapping[str, float] | None = None

    def resolved_weights(self) -> dict[str, float]:
        return dict(self.weights or {
            "alignment_incoherence": 1.0,
            "spectral_entropy": 0.8,
            "severe_antagonistic_mass": 1.2,
            "gradient_variance": 0.6,
            "parameter_energy_delta": 0.7,
            "hessian_excess": 0.8,
        })


@dataclass(frozen=True)
class Observation:
    geometry: GradientGeometry
    parameter_energy: float = 0.0
    parameter_energy_delta: float = 0.0
    hessian_max_eigenvalue: float = 0.0
    hessian_limit: float = float("inf")
    hard_violation: bool = False


@dataclass(frozen=True)
class Decision:
    mode: Mode
    instability_score: float
    lr_scale: float
    momentum_scale: float
    max_update_norm: float | None
    reject_update: bool
    rollback: bool
    admit_checkpoint: bool
    residuals: dict[str, float]


class ActiveStabilityController:
    def __init__(self, config: ControllerConfig | None = None):
        self.config = config or ControllerConfig()
        self.mode = Mode.CALIBRATION
        self.step_index = 0
        self.high_count = 0
        self.low_count = 0
        self.cooldown_remaining = 0
        self.stable_count = 0
        self.baselines = {
            name: RobustEMA(beta=self.config.ema_beta)
            for name in self.config.resolved_weights()
        }

    def _signals(self, obs: Observation) -> dict[str, float]:
        return {
            "alignment_incoherence": obs.geometry.alignment_incoherence,
            "spectral_entropy": obs.geometry.spectral_entropy,
            "severe_antagonistic_mass": obs.geometry.severe_antagonistic_mass,
            "gradient_variance": obs.geometry.gradient_variance,
            "parameter_energy_delta": max(0.0, obs.parameter_energy_delta),
            "hessian_excess": max(0.0, obs.hessian_max_eigenvalue - obs.hessian_limit),
        }

    def observe(self, obs: Observation) -> Decision:
        self.step_index += 1
        signals = self._signals(obs)

        residuals = {
            name: self.baselines[name].residual(value)
            for name, value in signals.items()
        }
        weights = self.config.resolved_weights()
        score = sum(weights[name] * max(0.0, residuals[name]) for name in weights)

        if self.mode == Mode.CALIBRATION:
            for name, value in signals.items():
                self.baselines[name].update(value)
            if self.step_index >= self.config.calibration_steps:
                self.mode = Mode.NORMAL

        elif self.mode == Mode.RECOVERY:
            self.mode = Mode.COOLDOWN

        elif self.mode == Mode.COOLDOWN:
            self.cooldown_remaining -= 1
            if obs.hard_violation:
                self.mode = Mode.RECOVERY
                self.cooldown_remaining = self.config.cooldown_steps
            elif self.cooldown_remaining <= 0:
                self.mode = Mode.DAMPED

        elif obs.hard_violation or score >= self.config.recovery_threshold:
            self.mode = Mode.RECOVERY
            self.cooldown_remaining = self.config.cooldown_steps
            self.high_count = self.low_count = 0

        else:
            if score >= self.config.damp_threshold:
                self.high_count += 1
                self.low_count = 0
            elif score <= self.config.return_threshold:
                self.low_count += 1
                self.high_count = 0
            else:
                self.high_count = self.low_count = 0

            if self.high_count >= self.config.trigger_persistence:
                self.mode = Mode.DAMPED
                self.high_count = 0
            elif self.mode == Mode.DAMPED and self.low_count >= self.config.return_persistence:
                self.mode = Mode.NORMAL
                self.low_count = 0

            if score < self.config.damp_threshold:
                for name, value in signals.items():
                    self.baselines[name].update(value)

        stable = (
            self.mode in {Mode.NORMAL, Mode.CALIBRATION}
            and not obs.hard_violation
            and score < self.config.damp_threshold
        )
        self.stable_count = self.stable_count + 1 if stable else 0
        admit_checkpoint = self.stable_count >= self.config.checkpoint_stability_steps

        if self.mode in {Mode.DAMPED, Mode.COOLDOWN}:
            lr_scale = max(
                self.config.min_lr_scale,
                1.0 / (1.0 + self.config.lr_gain * max(score, 1.0)),
            )
            momentum_scale = max(
                self.config.min_momentum_scale,
                1.0 / (1.0 + self.config.momentum_gain * max(score, 1.0)),
            )
            max_update_norm = self.config.max_update_norm
        elif self.mode == Mode.RECOVERY:
            lr_scale = self.config.min_lr_scale
            momentum_scale = self.config.min_momentum_scale
            max_update_norm = 0.0
        else:
            lr_scale = momentum_scale = 1.0
            max_update_norm = None

        return Decision(
            mode=self.mode,
            instability_score=float(score),
            lr_scale=float(lr_scale),
            momentum_scale=float(momentum_scale),
            max_update_norm=max_update_norm,
            reject_update=self.mode == Mode.RECOVERY,
            rollback=self.mode == Mode.RECOVERY,
            admit_checkpoint=admit_checkpoint,
            residuals=residuals,
        )

    def state_dict(self) -> dict:
        return {
            "config": asdict(self.config),
            "mode": self.mode.value,
            "step_index": self.step_index,
            "high_count": self.high_count,
            "low_count": self.low_count,
            "cooldown_remaining": self.cooldown_remaining,
            "stable_count": self.stable_count,
            "baselines": {
                name: {"mean": b.mean, "deviation": b.deviation}
                for name, b in self.baselines.items()
            },
        }
