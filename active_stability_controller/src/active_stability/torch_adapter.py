from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .controller import ActiveStabilityController, Decision, Observation
from .metrics import compute_gradient_geometry


@dataclass
class StableCheckpoint:
    model_state: dict
    optimizer_state: dict
    step: int
    score: float


def flatten_gradients(parameters: Iterable) -> np.ndarray:
    chunks = []
    for p in parameters:
        if p.grad is not None:
            chunks.append(p.grad.detach().reshape(-1).cpu().numpy())
    if not chunks:
        raise RuntimeError("no gradients were produced")
    return np.concatenate(chunks)


def clip_update_vector(update: np.ndarray, max_norm: float | None) -> np.ndarray:
    if max_norm is None:
        return update
    norm = float(np.linalg.norm(update))
    if norm <= max_norm or norm == 0.0:
        return update
    return update * (max_norm / norm)


class TorchSupervisor:
    """Optimizer supervisor. Microbatch gradient extraction stays in the training loop."""

    def __init__(self, controller: ActiveStabilityController):
        self.controller = controller
        self.checkpoint: StableCheckpoint | None = None
        self.base_lrs: list[float] | None = None
        self.base_momentum: list[float | None] | None = None

    def _capture_optimizer_bases(self, optimizer) -> None:
        if self.base_lrs is None:
            self.base_lrs = [group["lr"] for group in optimizer.param_groups]
            self.base_momentum = [group.get("momentum") for group in optimizer.param_groups]

    def apply_scales(self, optimizer, decision: Decision) -> None:
        self._capture_optimizer_bases(optimizer)
        for i, group in enumerate(optimizer.param_groups):
            group["lr"] = self.base_lrs[i] * decision.lr_scale
            base_m = self.base_momentum[i]
            if base_m is not None:
                group["momentum"] = base_m * decision.momentum_scale

    def evaluate(
        self,
        microbatch_gradients: list[np.ndarray],
        *,
        parameter_energy: float = 0.0,
        parameter_energy_delta: float = 0.0,
        hessian_max_eigenvalue: float = 0.0,
        hessian_limit: float = float("inf"),
        hard_violation: bool = False,
    ) -> Decision:
        geometry = compute_gradient_geometry(microbatch_gradients)
        return self.controller.observe(Observation(
            geometry=geometry,
            parameter_energy=parameter_energy,
            parameter_energy_delta=parameter_energy_delta,
            hessian_max_eigenvalue=hessian_max_eigenvalue,
            hessian_limit=hessian_limit,
            hard_violation=hard_violation,
        ))

    def maybe_checkpoint(self, model, optimizer, decision: Decision, step: int) -> None:
        if decision.admit_checkpoint:
            self.checkpoint = StableCheckpoint(
                model_state=deepcopy(model.state_dict()),
                optimizer_state=deepcopy(optimizer.state_dict()),
                step=step,
                score=decision.instability_score,
            )

    def rollback(self, model, optimizer) -> bool:
        if self.checkpoint is None:
            return False
        model.load_state_dict(self.checkpoint.model_state)
        optimizer.load_state_dict(self.checkpoint.optimizer_state)
        return True
