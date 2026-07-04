# Model Stage Smoke Summary

## Status

- MODEL_STAGE_CONFIRMED_BY_USER
- OPENVLA_PROCESSOR_SMOKE_PASS
- OPENVLA_REAL_PROCESSOR_COLLATOR_SMOKE_PASS
- OPENVLA_ONE_BATCH_FORWARD_SMOKE_PASS
- TRAINING_NOT_STARTED
- LORA_OFT_NOT_STARTED
- CLOSED_LOOP_EVAL_NOT_STARTED

## One-Batch Forward Result

Input shapes:

- input_ids: [1, 102]
- attention_mask: [1, 102]
- pixel_values: [1, 6, 224, 224]

Output:

- generate_shape: [1, 103]
- forward_mode: generate_max_new_tokens_1
- max CUDA memory: about 14.348 GB

## Meaning

The RTX 5090 environment can load OpenVLA/openvla-7b and run a one-sample TravelUAV prompt/image forward smoke.

This confirms that the base VLA model and real TravelUAV image/instruction preprocessing path are operational.

## Important Notes

This does not train UAV action head.

This does not validate UAV action prediction quality.

This does not run LoRA/OFT.

This does not run closed-loop UAV navigation evaluation.

## Next Technical Step

Before any training, implement an OpenVLA-OFT UAV training dataset path that provides:

- real OpenVLA processor outputs
- actions: [B, 8, 4]
- proprio: [B, 4]
- dataset_names: TravelUAV

Then run a tiny loss-only training smoke on a very small clean timestamp subset.

## Recommended Guardrail

Before optimizer-step training, explicitly confirm:

TINY_UAV_TRAINING_SMOKE_CONFIRMED
