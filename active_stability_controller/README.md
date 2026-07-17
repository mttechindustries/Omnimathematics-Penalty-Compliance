# Active Stability Controller

A minimal closed-loop supervisory controller for model training. It monitors microbatch gradient geometry and regulates optimizer gain when training leaves its calibrated operating region.

## Implemented

- Mean gradient alignment and alignment incoherence
- Spectral gradient entropy and effective gradient rank
- Gradient variance
- Antagonistic and severity-weighted antagonistic mass
- Robust online baselines and normalized residuals
- Calibration, normal, damped, recovery, and cooldown modes
- Hysteresis and persistence counters
- Learning-rate and momentum gain scheduling
- Stable checkpoint admission and rollback support
- Optional PyTorch adapter

## Install

```bash
pip install -e .
```

For PyTorch integration:

```bash
pip install -e '.[torch]'
```

## Run the demonstration

```bash
python examples/numpy_demo.py
```

## Training-loop integration

1. Split each batch into 4–8 microbatches.
2. Compute one flattened gradient vector per microbatch.
3. Pass those vectors to `TorchSupervisor.evaluate(...)`.
4. Apply returned learning-rate and momentum scales before the accepted optimizer step.
5. Reject and roll back when `decision.rollback` is true.
6. Save checkpoints only when `decision.admit_checkpoint` is true.

The controller does not classify disturbances as malicious. It responds only to measured instability.
