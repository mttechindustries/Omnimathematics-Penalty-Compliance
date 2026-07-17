import numpy as np
from active_stability import ActiveStabilityController, ControllerConfig, Observation, compute_gradient_geometry

rng = np.random.default_rng(7)
controller = ActiveStabilityController(ControllerConfig(calibration_steps=20))

for step in range(60):
    center = np.ones(32)
    noise = 0.03 if step < 35 else 0.8
    gradients = center + rng.normal(0, noise, size=(8, 32))
    if step >= 45:
        gradients[-2:] *= -2.0

    geometry = compute_gradient_geometry(gradients)
    decision = controller.observe(Observation(geometry=geometry))
    print(
        f"step={step:02d} mode={decision.mode.value:11s} "
        f"score={decision.instability_score:6.2f} "
        f"lr_scale={decision.lr_scale:.3f} "
        f"H={geometry.spectral_entropy:.3f} "
        f"M-={geometry.severe_antagonistic_mass:.3f}"
    )
