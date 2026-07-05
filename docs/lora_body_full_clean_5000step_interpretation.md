# Body-Frame LoRA 5000-Step Interpretation

## Status

- body-frame action representation: `[v_forward, v_right, vz, yaw_rate]`
- training: LoRA + UAV action head, 5000 steps
- validation: full clean timestamp body-frame val set

## Metrics

```json
{
  "overall_mae": 0.33838364481925964,
  "overall_rmse": 0.603779137134552,
  "per_dim_mae": {
    "v_forward": 1.0318907499313354,
    "v_right": 0.13938698172569275,
    "vz": 0.11900318413972855,
    "yaw_rate": 0.06325327605009079
  },
  "per_dim_rmse": {
    "v_forward": 1.1623982191085815,
    "v_right": 0.2373243123292923,
    "vz": 0.19778616726398468,
    "yaw_rate": 0.10760116577148438
  }
}
```

## Interpretation

The body-frame model strongly improves lateral action representation (`v_right`), but the forward velocity (`v_forward`) error is high.

This suggests that ego-centric action representation is promising for lateral control, but requires either more stable forward-speed supervision, action clipping/normalization, or a separate treatment of longitudinal velocity.

This should be treated as a method exploration result, not yet the main result.
