import numpy as np
from active_stability import compute_gradient_geometry


def test_identical_gradients_are_rank_one_and_low_entropy():
    g = np.tile(np.array([[1.0, 2.0, 3.0]]), (4, 1))
    m = compute_gradient_geometry(g)
    assert m.mean_alignment > 0.999
    assert m.alignment_incoherence < 1e-8
    assert m.spectral_entropy < 1e-8
    assert abs(m.effective_rank - 1.0) < 1e-8


def test_orthogonal_gradients_have_high_entropy():
    g = np.eye(4)
    m = compute_gradient_geometry(g)
    assert m.spectral_entropy > 0.99
    assert abs(m.effective_rank - 4.0) < 1e-8


def test_opposing_gradient_creates_antagonistic_mass():
    g = np.array([[1.0, 0.0], [1.0, 0.0], [-0.5, 0.0]])
    m = compute_gradient_geometry(g)
    assert m.antagonistic_mass > 0.0
    assert m.severe_antagonistic_mass > 0.0
