import numpy as np
from active_stability import ActiveStabilityController, ControllerConfig, Observation, compute_gradient_geometry, Mode


def obs(g):
    return Observation(geometry=compute_gradient_geometry(np.asarray(g, dtype=float)))


def test_calibration_then_normal():
    c = ActiveStabilityController(ControllerConfig(calibration_steps=2))
    aligned = [[1, 0], [1, 0], [1, 0]]
    assert c.observe(obs(aligned)).mode == Mode.CALIBRATION
    assert c.observe(obs(aligned)).mode == Mode.NORMAL


def test_hard_violation_triggers_recovery():
    c = ActiveStabilityController(ControllerConfig(calibration_steps=1))
    aligned = [[1, 0], [1, 0], [1, 0]]
    c.observe(obs(aligned))
    o = Observation(geometry=compute_gradient_geometry(aligned), hard_violation=True)
    d = c.observe(o)
    assert d.mode == Mode.RECOVERY
    assert d.reject_update
    assert d.rollback


def test_recovery_transitions_to_cooldown_without_looping():
    c = ActiveStabilityController(ControllerConfig(calibration_steps=1, recovery_threshold=0.1))
    aligned = [[1, 0], [1, 0], [1, 0]]
    c.observe(obs(aligned))
    disturbed = [[1, 0], [-1, 0], [0, 1]]
    assert c.observe(obs(disturbed)).mode == Mode.RECOVERY
    assert c.observe(obs(disturbed)).mode == Mode.COOLDOWN
