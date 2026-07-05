# TravelUAV History Transformer Action-Chunk BC Report

## Result

- Status: `BC_HISTORY_TRANSFORMER_ACTION_CHUNK_PASS`
- Model type: non-large-model Transformer behavior cloning baseline
- Input: history of `[state(4), previous_action(4)]`
- History length: `16`
- Output: `action_chunk = [8, 4]`
- Train samples: `298304`
- Val samples: `31898`
- Epochs: `80`
- Batch size: `2048`
- Device: `cuda`

## Safety Boundary

- OpenVLA training started: `False`
- LoRA/OFT training started: `False`
- Diffusion Policy training started: `False`
- Real AirSim rollout: `False`

## Final Metrics

- Final epoch: `80`
- Final train MSE norm: `0.2667680684588186`
- Final val MSE norm: `0.5340721028446367`
- Final elapsed sec: `531.77`

## Best Validation

- Best epoch: `9`
- Best val MSE norm: `0.4650172699980694`

## Best Horizon MAE

```json
[
  [
    0.23962070047855377,
    0.24517999589443207,
    0.20867836475372314,
    0.07528021931648254
  ],
  [
    0.3227323591709137,
    0.33464986085891724,
    0.27501264214515686,
    0.05611743777990341
  ],
  [
    0.3924584984779358,
    0.4077671468257904,
    0.32105517387390137,
    0.061141323298215866
  ],
  [
    0.46055132150650024,
    0.4736316204071045,
    0.34649986028671265,
    0.06600876152515411
  ],
  [
    0.5184364318847656,
    0.530489444732666,
    0.360030859708786,
    0.0704350471496582
  ],
  [
    0.5662356019020081,
    0.5792429447174072,
    0.3689669072628021,
    0.0750374123454094
  ],
  [
    0.6139986515045166,
    0.6233264207839966,
    0.37573879957199097,
    0.07949910312891006
  ],
  [
    0.6553974747657776,
    0.6628907322883606,
    0.3834737539291382,
    0.08531103283166885
  ]
]
```

## Final Horizon MAE

```json
[
  [
    0.23770955204963684,
    0.2291455864906311,
    0.1929916888475418,
    0.07931306213140488
  ],
  [
    0.3245708644390106,
    0.31922149658203125,
    0.2786218225955963,
    0.06653404980897903
  ],
  [
    0.40390822291374207,
    0.39996784925460815,
    0.3417571783065796,
    0.07163063436746597
  ],
  [
    0.47489675879478455,
    0.47206881642341614,
    0.377295583486557,
    0.07680895924568176
  ],
  [
    0.5337874293327332,
    0.5312739610671997,
    0.394538015127182,
    0.08250126987695694
  ],
  [
    0.5856144428253174,
    0.5813547372817993,
    0.4050908386707306,
    0.08992160111665726
  ],
  [
    0.6315330266952515,
    0.6258898377418518,
    0.41167357563972473,
    0.09757877886295319
  ],
  [
    0.6716068387031555,
    0.663486897945404,
    0.4165087044239044,
    0.10457511991262436
  ]
]
```

## Artifact

The checkpoint is intentionally not committed to git.

- Best checkpoint: `checkpoints/bc/traveluav_history_transformer_action_chunk_full_best.pt`
- Size bytes: `19825531`
- SHA256: `9bf8781ed9a82bd116f10872f4eb6798effefcb4b73431e8fc22ffaa4d2a26dc`

## Conclusion

This is a full-split offline supervised sequence baseline over existing TravelUAV trajectories. It is not a real AirSim rollout and not a large-model training run.
