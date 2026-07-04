# JSONL Validation Report

## Checked File

- Candidate missing: `data/debug/traveluav_real_debug.jsonl`.
- Selected `data/debug/traveluav_BrushifyCountryRoads_debug.jsonl`.
- Checked JSONL: `data/debug/traveluav_BrushifyCountryRoads_debug.jsonl`

## Summary

- Total samples: `60`
- Parsed valid samples for episode/action checks: `60`
- Episodes: `3`
- Image path exists: `60/60` (100.00%)
- Missing instruction count: `0`
- State format errors: `0`
- Action format errors: `0`
- Action chunk format errors: `0`
- Required field missing counts: `{}`
- Other issue counts: `{}`

## Toy Data Check

- Toy data detected: `False`
- Evidence: rows point to local `data/raw/TravelUAV`, raw source files or episode directories exist, and image files exist.

## Action Recompute Check

Actions were recomputed from adjacent rows inside each `episode_id`, sorted by `step_id`:

```text
vx = (x_next - x) / dt
vy = (y_next - y) / dt
vz = (z_next - z) / dt
yaw_rate = wrap_angle(yaw_next - yaw) / dt
```

- Recomputed adjacent rows: `57`
- Rows failing tolerance `1e-06`: `0`
- Terminal/truncated rows without next state in this JSONL: `3`

| Dimension | Error |
| --- | --- |
| vx | max=0, mean=0 |
| vy | max=0, mean=0 |
| vz | max=0, mean=0 |
| yaw_rate | max=0, mean=0 |

## Action Numeric Range

| Dimension | min/max/mean |
| --- | --- |
| vx | min=-0.762923177, max=0.036389789, mean=-0.234704948 |
| vy | min=-0.834129341, max=0.986713976, mean=0.102715529 |
| vz | min=-0.991800131, max=0.000989738, mean=-0.353610973 |
| yaw_rate | min=-0.442087447, max=0.105517476, mean=-0.007089474 |

Extreme action heuristic:

- Rows with any `|vx|`, `|vy|`, or `|vz|` > 20.0: `0`
- Rows with `|yaw_rate|` > pi: `0`

## Zero-Vector Check

- All-zero state rows: `0`
- All-zero action rows: `0`
- All-zero action_chunk rows: `0`

## Episode And Chunk Checks

- Step continuity gaps inside episode: `0`
- Duplicate step ids inside episode: `0`
- action_chunk first action mismatches current action: `0`
- action_chunk known same-episode comparisons: `396`
- action_chunk known same-episode mismatches: `0`
- action_chunk future items beyond this debug JSONL: `84`
- Detected cross-episode action_chunk evidence: `0`

Note: because debug JSONL files are truncated, some future `action_chunk` entries near the end of an episode cannot be fully verified from the JSONL alone. Available same-episode positions are checked exactly, and no cross-episode evidence is accepted as a pass condition.

## Training Usability

- Can be used as real data-path validation: `yes`, if `FORMAT_PASS` and `ACTION_PASS` are both reported.
- Can be used directly for final OpenVLA-OFT migration training: `no`.
- Reason: this is a small debug subset, not a full train/val split; full normalization, full dataset coverage, OpenVLA-OFT dataset adapter integration, model loading, and training must still be done later.

## Final Status

- `FORMAT_PASS`
- `ACTION_PASS`
- `NOT_TRAINING_READY`

## Next Work

- Keep this JSONL as a real TravelUAV data-path validation artifact.
- Expand validation to the intended train/val split before training.
- Recompute normalization statistics on the actual training split.
- Implement the OpenVLA-OFT UAV dataset adapter/collator without loading weights first.
- Move model loading, LoRA/OFT, action-head training, closed-loop evaluation, Diffusion Policy training, and RL expert generation to the 5090 stage.
