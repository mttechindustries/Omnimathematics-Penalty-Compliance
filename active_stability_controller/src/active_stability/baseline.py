from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RobustEMA:
    beta: float = 0.02
    eps: float = 1e-8
    mean: float | None = None
    deviation: float | None = None

    def update(self, value: float) -> None:
        if self.mean is None:
            self.mean = value
            self.deviation = 0.0
            return
        delta = value - self.mean
        self.mean += self.beta * delta
        self.deviation = (1.0 - self.beta) * float(self.deviation) + self.beta * abs(delta)

    def residual(self, value: float, clip: float = 10.0) -> float:
        if self.mean is None:
            return 0.0
        scale = max(float(self.deviation), self.eps)
        z = (value - self.mean) / scale
        return max(-clip, min(clip, z))
