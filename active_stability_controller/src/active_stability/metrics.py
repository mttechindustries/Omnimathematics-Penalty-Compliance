from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

EPS = 1e-12


@dataclass(frozen=True)
class GradientGeometry:
    mean_alignment: float
    alignment_incoherence: float
    gradient_variance: float
    spectral_entropy: float
    effective_rank: float
    antagonistic_mass: float
    severe_antagonistic_mass: float


def _as_matrix(gradients: list[np.ndarray] | np.ndarray) -> np.ndarray:
    g = np.asarray(gradients, dtype=np.float64)
    if g.ndim != 2:
        raise ValueError("gradients must have shape [microbatches, parameters]")
    if g.shape[0] < 2:
        raise ValueError("at least two microbatch gradients are required")
    if not np.isfinite(g).all():
        raise ValueError("gradients contain NaN or infinity")
    return g


def compute_gradient_geometry(gradients: list[np.ndarray] | np.ndarray) -> GradientGeometry:
    g = _as_matrix(gradients)
    norms = np.linalg.norm(g, axis=1)
    normalized = g / np.maximum(norms[:, None], EPS)

    gram = normalized @ normalized.T
    m = g.shape[0]
    off_diag = gram[~np.eye(m, dtype=bool)]
    mean_alignment = float(off_diag.mean())
    alignment_incoherence = float(np.clip((1.0 - mean_alignment) / 2.0, 0.0, 1.0))

    mean_g = g.mean(axis=0)
    gradient_variance = float(np.mean(np.sum((g - mean_g) ** 2, axis=1)))

    eigvals = np.linalg.eigvalsh(gram)
    eigvals = np.clip(eigvals, 0.0, None)
    rho = eigvals / max(float(eigvals.sum()), EPS)
    nz = rho[rho > EPS]
    raw_entropy = float(-np.sum(nz * np.log(nz)))
    max_rank = min(g.shape)
    spectral_entropy = raw_entropy / math.log(max_rank) if max_rank > 1 else 0.0
    effective_rank = float(math.exp(raw_entropy))

    aggregate_norm = float(np.linalg.norm(mean_g))
    if aggregate_norm <= EPS:
        influence = np.zeros(m, dtype=np.float64)
    else:
        influence = (g @ mean_g) / np.maximum(norms * aggregate_norm, EPS)

    antagonistic = influence < 0.0
    denom = max(float(norms.sum()), EPS)
    antagonistic_mass = float(norms[antagonistic].sum() / denom)
    severe_antagonistic_mass = float(
        np.sum(norms * np.maximum(0.0, -influence)) / denom
    )

    return GradientGeometry(
        mean_alignment=mean_alignment,
        alignment_incoherence=alignment_incoherence,
        gradient_variance=gradient_variance,
        spectral_entropy=float(np.clip(spectral_entropy, 0.0, 1.0)),
        effective_rank=effective_rank,
        antagonistic_mass=antagonistic_mass,
        severe_antagonistic_mass=severe_antagonistic_mass,
    )
