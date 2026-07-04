# OpenVLA-OFT UAV Minimal Integration Notes v2

## Scope

Static code scan only. No OpenVLA/openvla-7b checkpoint loading, no LoRA/OFT, no training.

## Current UAV Target Schema

- image: path to TravelUAV camera frame
- instruction: natural language command
- state: `[x, y, z, yaw]`
- action: `[vx, vy, vz, yaw_rate]`
- action_chunk: `[8, 4]`
- preferred train split: `data/processed/clean_train_timestamp_maps.jsonl`
- preferred val split: `data/processed/clean_val_timestamp_maps.jsonl`

## Top Candidate Files

### `vla-scripts/finetune.py`

- score: `480`
- groups: `action_head, config, dataset_collator, normalization, proprio_state, training_entrypoint`
- hits: `346`

  - line 2, training_entrypoint, `finetune`: `finetune.py`
  - line 4, config, `lora`: `Fine-tunes OpenVLA via LoRA.`
  - line 19, training_entrypoint, `accelerate`: `from accelerate import PartialState`
  - line 21, config, `lora`: `from peft import LoraConfig, PeftModel, get_peft_model`
  - line 25, dataset_collator, `dataloader`: `from torch.utils.data import DataLoader`
  - line 29, config, `wandb`: `import wandb`
  - line 40, action_head, `action_head`: `from prismatic.models.action_heads import DiffusionActionHead, L1RegressionActionHead`
  - line 40, action_head, `ActionHead`: `from prismatic.models.action_heads import DiffusionActionHead, L1RegressionActionHead`
  - line 45, proprio_state, `proprio`: `ProprioProjector,`
  - line 47, training_entrypoint, `train_`: `from prismatic.training.train_utils import (`
  - line 53, dataset_collator, `collator`: `from prismatic.util.data_utils import PaddedCollatorForActionPrediction`
  - line 54, action_head, `action_token`: `from prismatic.vla.action_tokenizer import ActionTokenizer`
  - ... 334 more hits in JSON index

### `experiments/robot/openvla_utils.py`

- score: `470`
- groups: `action_head, config, dataset_collator, normalization, proprio_state, training_entrypoint`
- hits: `309`

  - line 27, action_head, `action_head`: `from prismatic.models.action_heads import DiffusionActionHead, L1RegressionActionHead`
  - line 27, action_head, `ActionHead`: `from prismatic.models.action_heads import DiffusionActionHead, L1RegressionActionHead`
  - line 29, proprio_state, `proprio`: `from prismatic.models.projectors import NoisyActionProjector, ProprioProjector`
  - line 31, action_head, `action_dim`: `ACTION_DIM,`
  - line 32, proprio_state, `proprio`: `ACTION_PROPRIO_NORMALIZATION_TYPE,`
  - line 32, normalization, `normalization`: `ACTION_PROPRIO_NORMALIZATION_TYPE,`
  - line 34, dataset_collator, `dataset`: `from prismatic.vla.datasets.rlds.utils.data_utils import NormalizationType`
  - line 34, dataset_collator, `datasets`: `from prismatic.vla.datasets.rlds.utils.data_utils import NormalizationType`
  - line 34, dataset_collator, `RLDS`: `from prismatic.vla.datasets.rlds.utils.data_utils import NormalizationType`
  - line 34, normalization, `normalization`: `from prismatic.vla.datasets.rlds.utils.data_utils import NormalizationType`
  - line 46, config, `model_path`: `def model_is_on_hf_hub(model_path: str) -> bool:`
  - line 50, config, `model_path`: `HfApi().model_info(model_path)`
  - ... 297 more hits in JSON index

### `prismatic/extern/hf/modeling_prismatic.py`

- score: `460`
- groups: `action_head, config, dataset_collator, normalization, proprio_state, training_entrypoint`
- hits: `187`

  - line 5, normalization, `mean`: `Inherits from the default `transformers.PretrainedModel`. Meant to be standalone and self-contained,`
  - line 24, training_entrypoint, `train_`: `from prismatic.training.train_utils import (`
  - line 29, action_head, `action_dim`: `ACTION_DIM,`
  - line 30, proprio_state, `proprio`: `ACTION_PROPRIO_NORMALIZATION_TYPE,`
  - line 30, normalization, `normalization`: `ACTION_PROPRIO_NORMALIZATION_TYPE,`
  - line 31, action_head, `action_token`: `ACTION_TOKEN_BEGIN_IDX,`
  - line 35, normalization, `normalization`: `NormalizationType,`
  - line 283, config, `checkpoint`: `supports_gradient_checkpointing: bool = True`
  - line 290, normalization, `mean`: `# Important :: this HF ported version is *not* meant for training from scratch; only inference and fine-tuning!`
  - line 293, normalization, `std`: `std = (`
  - line 300, normalization, `mean`: `module.class_embedding.data.normal_(mean=0.0, std=std)`
  - line 300, normalization, `std`: `module.class_embedding.data.normal_(mean=0.0, std=std)`
  - ... 175 more hits in JSON index

### `experiments/robot/libero/run_libero_eval.py`

- score: `450`
- groups: `action_head, config, dataset_collator, normalization, proprio_state`
- hits: `117`

  - line 2, dataset_collator, `LIBERO`: `run_libero_eval.py`
  - line 4, dataset_collator, `LIBERO`: `Evaluates a trained policy in a LIBERO simulation benchmark task suite.`
  - line 20, dataset_collator, `LIBERO`: `from libero.libero import benchmark`
  - line 22, config, `wandb`: `import wandb`
  - line 26, dataset_collator, `LIBERO`: `from experiments.robot.libero.libero_utils import (`
  - line 27, dataset_collator, `LIBERO`: `get_libero_dummy_action,`
  - line 28, dataset_collator, `LIBERO`: `get_libero_env,`
  - line 29, dataset_collator, `LIBERO`: `get_libero_image,`
  - line 30, dataset_collator, `LIBERO`: `get_libero_wrist_image,`
  - line 35, action_head, `action_head`: `get_action_head,`
  - line 38, proprio_state, `proprio`: `get_proprio_projector,`
  - line 38, proprio_state, `proprio_projector`: `get_proprio_projector,`
  - ... 105 more hits in JSON index

### `prismatic/training/strategies/base_strategy.py`

- score: `410`
- groups: `action_head, config, dataset_collator, normalization, training_entrypoint`
- hits: `114`

  - line 18, dataset_collator, `dataset`: `from torch.utils.data import DataLoader, Dataset, DistributedSampler, IterableDataset`
  - line 18, dataset_collator, `dataloader`: `from torch.utils.data import DataLoader, Dataset, DistributedSampler, IterableDataset`
  - line 25, training_entrypoint, `train_`: `from prismatic.training.train_utils import (`
  - line 32, dataset_collator, `batch`: `from prismatic.util.batching_utils import SplitModalitySampler`
  - line 33, dataset_collator, `collator`: `from prismatic.util.data_utils import PaddedCollatorForActionPrediction, PaddedCollatorForLanguageModeling`
  - line 34, action_head, `action_token`: `from prismatic.vla.action_tokenizer import ActionTokenizer`
  - line 37, action_head, `action_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, NUM_ACTIONS_CHUNK, IGNORE_INDEX`
  - line 37, action_head, `action_token`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, NUM_ACTIONS_CHUNK, IGNORE_INDEX`
  - line 54, dataset_collator, `batch`: `global_batch_size: int,`
  - line 55, dataset_collator, `batch`: `per_device_batch_size: int,`
  - line 61, config, `checkpoint`: `enable_gradient_checkpointing: bool = True,`
  - line 76, dataset_collator, `batch`: `self.global_batch_size, self.per_device_batch_size = global_batch_size, per_device_batch_size`
  - ... 102 more hits in JSON index

### `prismatic/vla/datasets/datasets.py`

- score: `410`
- groups: `action_head, config, dataset_collator, normalization, proprio_state`
- hits: `120`

  - line 2, dataset_collator, `dataset`: `datasets.py`
  - line 2, dataset_collator, `datasets`: `datasets.py`
  - line 4, dataset_collator, `dataset`: `Lightweight PyTorch Dataset Definition for wrapping RLDS TFDS Pipeline; just defines transform from RLDS default`
  - line 4, dataset_collator, `RLDS`: `Lightweight PyTorch Dataset Definition for wrapping RLDS TFDS Pipeline; just defines transform from RLDS default`
  - line 5, dataset_collator, `dataset`: `format to OpenVLA, IterableDataset shim.`
  - line 15, dataset_collator, `dataset`: `from torch.utils.data import Dataset, IterableDataset`
  - line 21, action_head, `action_token`: `from prismatic.vla.action_tokenizer import ActionTokenizer`
  - line 22, action_head, `action_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 22, action_head, `action_token`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 22, proprio_state, `proprio`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 22, proprio_state, `proprio_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 22, normalization, `normalization`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - ... 108 more hits in JSON index

### `prismatic/vla/datasets/rlds/dataset.py`

- score: `410`
- groups: `action_head, config, dataset_collator, normalization, proprio_state`
- hits: `226`

  - line 2, dataset_collator, `dataset`: `dataset.py`
  - line 4, dataset_collator, `dataset`: `Core interface script for configuring and initializing RLDS datasets.`
  - line 4, dataset_collator, `datasets`: `Core interface script for configuring and initializing RLDS datasets.`
  - line 4, dataset_collator, `RLDS`: `Core interface script for configuring and initializing RLDS datasets.`
  - line 16, dataset_collator, `dataset`: `import tensorflow_datasets as tfds`
  - line 16, dataset_collator, `datasets`: `import tensorflow_datasets as tfds`
  - line 19, action_head, `action_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 19, action_head, `action_token`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 19, proprio_state, `proprio`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 19, proprio_state, `proprio_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 19, normalization, `normalization`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 20, dataset_collator, `dataset`: `from prismatic.vla.datasets.rlds import obs_transforms, traj_transforms`
  - ... 214 more hits in JSON index

### `prismatic/vla/datasets/rlds/oxe/materialize.py`

- score: `410`
- groups: `action_head, config, dataset_collator, normalization, proprio_state`
- hits: `90`

  - line 4, dataset_collator, `dataset`: `Factory class for initializing Open-X Embodiment dataset kwargs and other parameters; provides and exports functions for`
  - line 13, action_head, `action_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 13, action_head, `action_token`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 13, proprio_state, `proprio`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 13, proprio_state, `proprio_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 13, normalization, `normalization`: `from prismatic.vla.constants import ACTION_DIM, ACTION_PROPRIO_NORMALIZATION_TYPE, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 14, dataset_collator, `dataset`: `from prismatic.vla.datasets.rlds.oxe.configs import OXE_DATASET_CONFIGS, ActionEncoding`
  - line 14, dataset_collator, `datasets`: `from prismatic.vla.datasets.rlds.oxe.configs import OXE_DATASET_CONFIGS, ActionEncoding`
  - line 14, dataset_collator, `RLDS`: `from prismatic.vla.datasets.rlds.oxe.configs import OXE_DATASET_CONFIGS, ActionEncoding`
  - line 15, dataset_collator, `dataset`: `from prismatic.vla.datasets.rlds.oxe.transforms import OXE_STANDARDIZATION_TRANSFORMS`
  - line 15, dataset_collator, `datasets`: `from prismatic.vla.datasets.rlds.oxe.transforms import OXE_STANDARDIZATION_TRANSFORMS`
  - line 15, dataset_collator, `RLDS`: `from prismatic.vla.datasets.rlds.oxe.transforms import OXE_STANDARDIZATION_TRANSFORMS`
  - ... 78 more hits in JSON index

### `experiments/robot/aloha/preprocess_split_aloha_data.py`

- score: `400`
- groups: `config, dataset_collator, normalization, proprio_state, training_entrypoint`
- hits: `60`

  - line 2, dataset_collator, `dataset`: `Preprocesses ALOHA dataset(s) and splits them into train/val sets.`
  - line 5, normalization, `mean`: `Splits happen at the episode level (not step level), which means that`
  - line 10, dataset_collator, `dataset`: `/PATH/TO/DATASET/dataset_name/`
  - line 10, config, `dataset_name`: `/PATH/TO/DATASET/dataset_name/`
  - line 17, dataset_collator, `dataset`: `/PATH/TO/PREPROCESSED_DATASETS/dataset_name/`
  - line 17, dataset_collator, `datasets`: `/PATH/TO/PREPROCESSED_DATASETS/dataset_name/`
  - line 17, config, `dataset_name`: `/PATH/TO/PREPROCESSED_DATASETS/dataset_name/`
  - line 34, dataset_collator, `dataset`: `--dataset_path /scr/moojink/data/aloha1_raw/put_green_pepper_into_pot/ \`
  - line 38, dataset_collator, `dataset`: `--dataset_path /scr/moojink/data/aloha1_raw/put_red_pepper_into_pot/ \`
  - line 42, dataset_collator, `dataset`: `--dataset_path /scr/moojink/data/aloha1_raw/put_yellow_corn_into_pot/ \`
  - line 61, dataset_collator, `dataset`: `print(f"Dataset does not exist at \n{demo_path}\n")`
  - line 67, proprio_state, `qpos`: `qpos = root["/observations/qpos"][()]`
  - ... 48 more hits in JSON index

### `prismatic/models/action_heads.py`

- score: `385`
- groups: `action_head, dataset_collator, normalization, proprio_state, training_entrypoint`
- hits: `55`

  - line 9, action_head, `action_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 9, action_head, `action_token`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 9, proprio_state, `proprio`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 9, proprio_state, `proprio_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 14, dataset_collator, `batch`: `Sine- and cosine-based positional encoding that produces embeddings of a batch of timesteps.`
  - line 16, dataset_collator, `batch`: `For example, at train time, the input might be a batch of 32 randomly sampled diffusion timesteps -> shape (32,)`
  - line 17, dataset_collator, `batch`: `Then the output would be a batch of 32 timestep embeddings -> shape (32, D)`
  - line 27, dataset_collator, `batch`: `# x: (batch_size,)`
  - line 33, dataset_collator, `batch`: `emb = x[:, None] * emb[None, :]  # shape: (batch_size, 1) * (1, D/2) -> (batch_size, D/2)`
  - line 34, dataset_collator, `batch`: `emb = torch.cat((emb.sin(), emb.cos()), dim=-1)  # shape: (batch_size, D)`
  - line 50, dataset_collator, `batch`: `# x: (batch_size, hidden_dim)`
  - line 51, normalization, `normalization`: `# We follow the module ordering of "Pre-Layer Normalization" feedforward networks in Transformers as`
  - ... 43 more hits in JSON index

### `prismatic/models/vlms/prismatic.py`

- score: `383`
- groups: `action_head, config, dataset_collator, normalization, training_entrypoint`
- hits: `53`

  - line 73, config, `checkpoint`: `# Set Module Keys =>> used in Checkpoint Saving / Model Loading`
  - line 88, config, `checkpoint`: `pretrained_checkpoint: Path,`
  - line 94, config, `freeze`: `freeze_weights: bool = True,`
  - line 97, config, `checkpoint`: `"""Initialize a PrismaticVLM from a pretrained checkpoint, freezing all weights, tailored for inference."""`
  - line 107, config, `checkpoint`: `# Load from Checkpoint (Custom --> should load both *projector* and *llm* weights)`
  - line 108, config, `checkpoint`: `model_state_dict = torch.load(pretrained_checkpoint, map_location="cpu")["model"]`
  - line 111, config, `checkpoint`: `), "PrismaticVLM `from_pretrained` expects checkpoint with keys for `projector` AND `llm_backbone`!"`
  - line 118, config, `freeze`: `# Freeze Weights`
  - line 119, config, `freeze`: `if freeze_weights:`
  - line 129, config, `freeze`: `def freeze_backbones(self, stage: str) -> None:`
  - line 133, training_entrypoint, `finetune`: `We support two separate stages --> "align" and "finetune".`
  - line 135, training_entrypoint, `finetune`: `=> "finetune" --> vision_backbone* is frozen; both `projector` and `llm_backbone` are trained.`
  - ... 41 more hits in JSON index

### `README.md`

- score: `372`
- groups: `action_head, config, dataset_collator, normalization, proprio_state, training_entrypoint`
- hits: `32`

  - line 3, config, `oft`: `**Project website: https://openvla-oft.github.io/**`
  - line 12, dataset_collator, `LIBERO`: `* 1 GPU with ~16 GB VRAM for LIBERO sim benchmark tasks`
  - line 16, config, `oft`: `* Between 1-8 GPUs with 27-80 GB, depending on the desired training setup (with default bfloat16 data type). See [this FAQ on our project website](https://openvla-oft.github.io/#train-compute) for details.`
  - line 22, config, `oft`: `Then, run the Python script below to download a pretrained OpenVLA-OFT checkpoint and run inference to generate an action chunk:`
  - line 22, config, `checkpoint`: `Then, run the Python script below to download a pretrained OpenVLA-OFT checkpoint and run inference to generate an action chunk:`
  - line 26, dataset_collator, `LIBERO`: `from experiments.robot.libero.run_libero_eval import GenerateConfig`
  - line 27, action_head, `action_head`: `from experiments.robot.openvla_utils import get_action_head, get_processor, get_proprio_projector, get_vla, get_vla_action`
  - line 27, proprio_state, `proprio`: `from experiments.robot.openvla_utils import get_action_head, get_processor, get_proprio_projector, get_vla, get_vla_action`
  - line 27, proprio_state, `proprio_projector`: `from experiments.robot.openvla_utils import get_action_head, get_processor, get_proprio_projector, get_vla, get_vla_action`
  - line 28, proprio_state, `proprio`: `from prismatic.vla.constants import NUM_ACTIONS_CHUNK, PROPRIO_DIM`
  - line 28, proprio_state, `proprio_dim`: `from prismatic.vla.constants import NUM_ACTIONS_CHUNK, PROPRIO_DIM`
  - line 30, dataset_collator, `LIBERO`: `# Instantiate config (see class GenerateConfig in experiments/robot/libero/run_libero_eval.py for definitions)`
  - ... 20 more hits in JSON index

### `prismatic/util/batching_utils.py`

- score: `360`
- groups: `config, dataset_collator, normalization, training_entrypoint`
- hits: `81`

  - line 2, dataset_collator, `batch`: `batching_utils.py`
  - line 5, dataset_collator, `batch`: `"split-modality" batches as described in the LLaVa paper; this makes sure that a given device/batch is either entirely`
  - line 15, dataset_collator, `dataset`: `from torch.utils.data import Dataset, Sampler`
  - line 19, training_entrypoint, `accelerate`: `#   the default batching behavior of HF's Trainer Class --> derived from `accelerate`).`
  - line 19, dataset_collator, `batch`: `#   the default batching behavior of HF's Trainer Class --> derived from `accelerate`).`
  - line 26, dataset_collator, `dataset`: `dataset: Dataset,`
  - line 28, dataset_collator, `batch`: `global_batch_size: int,`
  - line 40, dataset_collator, `dataset`: `self.dataset, self.modality_lengths, self.drop_last = dataset, modality_lengths, drop_last`
  - line 41, dataset_collator, `batch`: `self.global_batch_size = global_batch_size`
  - line 45, dataset_collator, `dataset`: `self.total_size = math.ceil(len(self.dataset) / self.global_batch_size) * self.global_batch_size`
  - line 45, dataset_collator, `batch`: `self.total_size = math.ceil(len(self.dataset) / self.global_batch_size) * self.global_batch_size`
  - line 49, dataset_collator, `batch`: `def reindex_batch(batch_idxs: List[int], idx2lengths: List[int], n_buckets: int) -> List[List[int]]:`
  - ... 69 more hits in JSON index

### `ALOHA.md`

- score: `353`
- groups: `action_head, config, dataset_collator, normalization, proprio_state, training_entrypoint`
- hits: `53`

  - line 1, config, `oft`: `# OpenVLA-OFT+ in Real-World ALOHA Robot Tasks`
  - line 18, dataset_collator, `LIBERO`: `Note: Unlike the LIBERO evaluation setup, we use a server-client interface here. This is particularly useful if the user's machine which commands the robot does not have access to a local GPU with sufficient specs to run`
  - line 23, training_entrypoint, `finetune`: `* `vla-scripts/finetune.py`: VLA fine-tuning script`
  - line 33, dataset_collator, `dataset`: `First, use our `preprocess_split_aloha_data.py` script to preprocess the raw ALOHA dataset: downsize images from 480x640 to 256x256 and split into training and validation sets. Below are examples for the `put X into pot``
  - line 37, dataset_collator, `dataset`: `--dataset_path /scr/moojink/data/aloha1_raw/put_green_pepper_into_pot/ \`
  - line 41, dataset_collator, `dataset`: `--dataset_path /scr/moojink/data/aloha1_raw/put_red_pepper_into_pot/ \`
  - line 45, dataset_collator, `dataset`: `--dataset_path /scr/moojink/data/aloha1_raw/put_yellow_corn_into_pot/ \`
  - line 50, dataset_collator, `dataset`: `Then, convert the preprocessed ALOHA datasets into a single RLDS dataset that is compatible with OpenVLA fine-tuning. This process is the same as in the original OpenVLA repo. See instructions for converting to RLDS [her`
  - line 50, dataset_collator, `datasets`: `Then, convert the preprocessed ALOHA datasets into a single RLDS dataset that is compatible with OpenVLA fine-tuning. This process is the same as in the original OpenVLA repo. See instructions for converting to RLDS [her`
  - line 50, dataset_collator, `RLDS`: `Then, convert the preprocessed ALOHA datasets into a single RLDS dataset that is compatible with OpenVLA fine-tuning. This process is the same as in the original OpenVLA repo. See instructions for converting to RLDS [her`
  - line 52, dataset_collator, `dataset`: `After converting to RLDS, register the dataset (which, for the example task above, would be called `aloha1_put_X_into_pot_300_demos`) with our dataloader by adding an entry for it in `configs.py` ([here](prismatic/vla/da`
  - line 52, dataset_collator, `datasets`: `After converting to RLDS, register the dataset (which, for the example task above, would be called `aloha1_put_X_into_pot_300_demos`) with our dataloader by adding an entry for it in `configs.py` ([here](prismatic/vla/da`
  - ... 41 more hits in JSON index

### `experiments/robot/libero/regenerate_libero_dataset.py`

- score: `342`
- groups: `dataset_collator, proprio_state, training_entrypoint`
- hits: `72`

  - line 2, dataset_collator, `dataset`: `Regenerates a LIBERO dataset (HDF5 files) by replaying demonstrations in the environments.`
  - line 2, dataset_collator, `LIBERO`: `Regenerates a LIBERO dataset (HDF5 files) by replaying demonstrations in the environments.`
  - line 8, dataset_collator, `RLDS`: `- In the LIBERO HDF5 data -> RLDS data conversion (not shown here), we rotate the images by`
  - line 8, dataset_collator, `LIBERO`: `- In the LIBERO HDF5 data -> RLDS data conversion (not shown here), we rotate the images by`
  - line 13, dataset_collator, `dataset`: `python experiments/robot/libero/regenerate_libero_dataset.py \`
  - line 13, dataset_collator, `LIBERO`: `python experiments/robot/libero/regenerate_libero_dataset.py \`
  - line 14, dataset_collator, `LIBERO`: `--libero_task_suite [ libero_spatial | libero_object | libero_goal | libero_10 ] \`
  - line 15, dataset_collator, `dataset`: `--libero_raw_data_dir <PATH TO RAW HDF5 DATASET DIR> \`
  - line 15, dataset_collator, `LIBERO`: `--libero_raw_data_dir <PATH TO RAW HDF5 DATASET DIR> \`
  - line 16, dataset_collator, `LIBERO`: `--libero_target_dir <PATH TO TARGET DIR>`
  - line 18, dataset_collator, `LIBERO`: `Example (LIBERO-Spatial):`
  - line 19, dataset_collator, `dataset`: `python experiments/robot/libero/regenerate_libero_dataset.py \`
  - ... 60 more hits in JSON index

### `experiments/robot/aloha/constants.py`

- score: `340`
- groups: `action_head, dataset_collator, normalization, proprio_state`
- hits: `50`

  - line 7, dataset_collator, `dataset`: `'dataset_dir': DATA_DIR + '/fold_shorts',`
  - line 14, dataset_collator, `dataset`: `'dataset_dir': DATA_DIR + '/fold_shirt',`
  - line 21, dataset_collator, `dataset`: `'dataset_dir': DATA_DIR + '/scoop_raisins_into_bowl',`
  - line 27, dataset_collator, `dataset`: `'dataset_dir': DATA_DIR + '/scoop_almonds_and_green_M&Ms_into_bowl',`
  - line 33, dataset_collator, `dataset`: `'dataset_dir': DATA_DIR + '/scoop_pretzels_into_bowl',`
  - line 40, dataset_collator, `dataset`: `'dataset_dir': DATA_DIR + '/put_red_pepper_into_pot',`
  - line 46, dataset_collator, `dataset`: `'dataset_dir': DATA_DIR + '/put_yellow_corn_into_pot',`
  - line 52, dataset_collator, `dataset`: `'dataset_dir': DATA_DIR + '/put_green_pepper_into_pot',`
  - line 64, proprio_state, `qpos`: `# Left finger position limits (qpos[7]), right_finger = -1 * left_finger`
  - line 70, proprio_state, `qpos`: `# Gripper joint limits (qpos[6])`
  - line 80, normalization, `normalize`: `MASTER_GRIPPER_POSITION_NORMALIZE_FN = lambda x: (x - MASTER_GRIPPER_POSITION_CLOSE) / (MASTER_GRIPPER_POSITION_OPEN - MASTER_GRIPPER_POSITION_CLOSE)`
  - line 81, normalization, `normalize`: `PUPPET_GRIPPER_POSITION_NORMALIZE_FN = lambda x: (x - PUPPET_GRIPPER_POSITION_CLOSE) / (PUPPET_GRIPPER_POSITION_OPEN - PUPPET_GRIPPER_POSITION_CLOSE)`
  - ... 38 more hits in JSON index

### `vla-scripts/deploy.py`

- score: `329`
- groups: `action_head, config, normalization, proprio_state`
- hits: `29`

  - line 32, action_head, `action_head`: `get_action_head,`
  - line 34, proprio_state, `proprio`: `get_proprio_projector,`
  - line 34, proprio_state, `proprio_projector`: `get_proprio_projector,`
  - line 39, action_head, `action_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 39, action_head, `action_token`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 39, proprio_state, `proprio`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 39, proprio_state, `proprio_dim`: `from prismatic.vla.constants import ACTION_DIM, ACTION_TOKEN_BEGIN_IDX, IGNORE_INDEX, NUM_ACTIONS_CHUNK, PROPRIO_DIM, STOP_INDEX`
  - line 57, proprio_state, `proprio`: `# Load proprio projector`
  - line 58, proprio_state, `proprio`: `self.proprio_projector = None`
  - line 58, proprio_state, `proprio_projector`: `self.proprio_projector = None`
  - line 59, proprio_state, `proprio`: `if cfg.use_proprio:`
  - line 60, proprio_state, `proprio`: `self.proprio_projector = get_proprio_projector(cfg, self.vla.llm_dim, PROPRIO_DIM)`
  - ... 17 more hits in JSON index

### `prismatic/training/strategies/fsdp.py`

- score: `323`
- groups: `config, dataset_collator, normalization, training_entrypoint`
- hits: `43`

  - line 17, config, `checkpoint`: `from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import (`
  - line 18, config, `checkpoint`: `CheckpointImpl,`
  - line 19, config, `checkpoint`: `apply_activation_checkpointing,`
  - line 20, config, `checkpoint`: `checkpoint_wrapper,`
  - line 48, dataset_collator, `batch`: `global_batch_size: int,`
  - line 49, dataset_collator, `batch`: `per_device_batch_size: int,`
  - line 55, config, `checkpoint`: `enable_gradient_checkpointing: bool = True,`
  - line 69, dataset_collator, `batch`: `global_batch_size=global_batch_size,`
  - line 70, dataset_collator, `batch`: `per_device_batch_size=per_device_batch_size,`
  - line 76, config, `checkpoint`: `enable_gradient_checkpointing=enable_gradient_checkpointing,`
  - line 95, config, `checkpoint`: `def save_checkpoint(`
  - line 100, training_entrypoint, `train_`: `train_loss: Optional[float] = None,`
  - ... 31 more hits in JSON index

### `prismatic/vla/constants.py`

- score: `323`
- groups: `action_head, dataset_collator, normalization, proprio_state`
- hits: `43`

  - line 5, dataset_collator, `LIBERO`: `training or evaluation. If it is unclear, defaults to using the LIBERO simulation benchmark constants.`
  - line 12, action_head, `action_token`: `ACTION_TOKEN_BEGIN_IDX = 31743`
  - line 16, proprio_state, `proprio`: `# Defines supported normalization schemes for action and proprioceptive state.`
  - line 16, normalization, `normalization`: `# Defines supported normalization schemes for action and proprioceptive state.`
  - line 17, normalization, `normalization`: `class NormalizationType(str, Enum):`
  - line 19, normalization, `normalize`: `NORMAL = "normal"               # Normalize to Mean = 0, Stdev = 1`
  - line 19, normalization, `mean`: `NORMAL = "normal"               # Normalize to Mean = 0, Stdev = 1`
  - line 19, normalization, `std`: `NORMAL = "normal"               # Normalize to Mean = 0, Stdev = 1`
  - line 20, normalization, `normalize`: `BOUNDS = "bounds"               # Normalize to Interval = [-1, 1]`
  - line 21, normalization, `normalize`: `BOUNDS_Q99 = "bounds_q99"       # Normalize [quantile_01, ..., quantile_99] --> [-1, ..., 1]`
  - line 21, normalization, `quantile`: `BOUNDS_Q99 = "bounds_q99"       # Normalize [quantile_01, ..., quantile_99] --> [-1, ..., 1]`
  - line 26, dataset_collator, `LIBERO`: `LIBERO_CONSTANTS = {`
  - ... 31 more hits in JSON index

### `prismatic/models/load.py`

- score: `318`
- groups: `action_head, config, dataset_collator, normalization`
- hits: `38`

  - line 21, action_head, `action_token`: `from prismatic.vla.action_tokenizer import ActionTokenizer`
  - line 62, config, `checkpoint`: `# Get paths for `config.json` and pretrained checkpoint`
  - line 63, config, `checkpoint`: `config_json, checkpoint_pt = run_dir / "config.json", run_dir / "checkpoints" / "latest-checkpoint.pt"`
  - line 65, config, `checkpoint`: `assert checkpoint_pt.exists(), f"Missing checkpoint for `{run_dir = }`"`
  - line 73, config, `checkpoint`: `checkpoint_pt = hf_hub_download(`
  - line 74, config, `checkpoint`: `repo_id=HF_HUB_REPO, filename=f"{model_id}/checkpoints/latest-checkpoint.pt", cache_dir=cache_dir`
  - line 88, config, `checkpoint`: `f"             Checkpoint Path =>> [underline]`{checkpoint_pt}`[/]"`
  - line 108, config, `checkpoint`: `overwatch.info(f"Loading VLM [bold blue]{model_cfg['model_id']}[/] from Checkpoint")`
  - line 110, config, `checkpoint`: `checkpoint_pt,`
  - line 115, config, `freeze`: `freeze_weights=not load_for_training,`
  - line 133, config, `checkpoint`: `#   checkpoint `.pt` file, rather than the top-level run directory!`
  - line 135, config, `checkpoint`: `overwatch.info(f"Loading from local checkpoint path `{(checkpoint_pt := Path(model_id_or_path))}`")`
  - ... 26 more hits in JSON index

### `experiments/robot/robot_utils.py`

- score: `313`
- groups: `action_head, dataset_collator, normalization, proprio_state`
- hits: `23`

  - line 17, action_head, `action_dim`: `ACTION_DIM = 7`
  - line 105, action_head, `action_head`: `action_head: Optional[torch.nn.Module] = None,`
  - line 106, proprio_state, `proprio`: `proprio_projector: Optional[torch.nn.Module] = None,`
  - line 106, proprio_state, `proprio_projector`: `proprio_projector: Optional[torch.nn.Module] = None,`
  - line 119, action_head, `action_head`: `action_head: Optional action head for continuous actions`
  - line 120, proprio_state, `proprio`: `proprio_projector: Optional proprioception projector`
  - line 120, proprio_state, `proprio_projector`: `proprio_projector: Optional proprioception projector`
  - line 138, action_head, `action_head`: `action_head=action_head,`
  - line 139, proprio_state, `proprio`: `proprio_projector=proprio_projector,`
  - line 139, proprio_state, `proprio_projector`: `proprio_projector=proprio_projector,`
  - line 149, normalization, `normalize`: `def normalize_gripper_action(action: np.ndarray, binarize: bool = True) -> np.ndarray:`
  - line 151, normalization, `normalize`: `Normalize gripper action from [0,1] to [-1,+1] range.`
  - ... 11 more hits in JSON index

### `LIBERO.md`

- score: `310`
- groups: `config, dataset_collator, proprio_state, training_entrypoint`
- hits: `126`

  - line 1, dataset_collator, `LIBERO`: `# OpenVLA-OFT in the LIBERO Simulation Benchmark`
  - line 1, config, `oft`: `# OpenVLA-OFT in the LIBERO Simulation Benchmark`
  - line 6, dataset_collator, `LIBERO`: `* `experiments/robot/libero/`: LIBERO eval files`
  - line 7, dataset_collator, `LIBERO`: `* `run_libero_eval.py`: LIBERO eval script`
  - line 8, dataset_collator, `LIBERO`: `* `libero_utils.py`: LIBERO eval utils`
  - line 14, training_entrypoint, `finetune`: `* `vla-scripts/finetune.py`: VLA fine-tuning script`
  - line 21, dataset_collator, `LIBERO`: `Clone and install the [LIBERO repo](https://github.com/Lifelong-Robot-Learning/LIBERO) and required packages:`
  - line 24, dataset_collator, `LIBERO`: `git clone https://github.com/Lifelong-Robot-Learning/LIBERO.git`
  - line 25, dataset_collator, `LIBERO`: `pip install -e LIBERO`
  - line 26, dataset_collator, `LIBERO`: `pip install -r experiments/robot/libero/libero_requirements.txt  # From openvla-oft base dir`
  - line 26, config, `oft`: `pip install -r experiments/robot/libero/libero_requirements.txt  # From openvla-oft base dir`
  - line 29, dataset_collator, `dataset`: `(Optional, if you plan to launch training) To download the [LIBERO datasets](https://huggingface.co/datasets/openvla/modified_libero_rlds) that we used in our fine-tuning`
  - ... 114 more hits in JSON index

### `prismatic/vla/datasets/rlds/oxe/transforms.py`

- score: `310`
- groups: `config, dataset_collator, proprio_state`
- hits: `199`

  - line 4, dataset_collator, `dataset`: `Defines a registry of per-dataset standardization transforms for each dataset in Open-X Embodiment.`
  - line 7, dataset_collator, `batch`: `Input: Dictionary of *batched* features (i.e., has leading time dimension)`
  - line 22, dataset_collator, `dataset`: `from prismatic.vla.datasets.rlds.oxe.utils.droid_utils import droid_baseact_transform, droid_finetuning_transform`
  - line 22, dataset_collator, `datasets`: `from prismatic.vla.datasets.rlds.oxe.utils.droid_utils import droid_baseact_transform, droid_finetuning_transform`
  - line 22, dataset_collator, `RLDS`: `from prismatic.vla.datasets.rlds.oxe.utils.droid_utils import droid_baseact_transform, droid_finetuning_transform`
  - line 23, dataset_collator, `dataset`: `from prismatic.vla.datasets.rlds.utils.data_utils import (`
  - line 23, dataset_collator, `datasets`: `from prismatic.vla.datasets.rlds.utils.data_utils import (`
  - line 23, dataset_collator, `RLDS`: `from prismatic.vla.datasets.rlds.utils.data_utils import (`
  - line 31, dataset_collator, `dataset`: `def bridge_oxe_dataset_transform(trajectory: Dict[str, Any]) -> Dict[str, Any]:`
  - line 35, dataset_collator, `dataset`: `Note =>> In original Bridge V2 dataset, the first timestep has an all-zero action, so we remove it!`
  - line 61, dataset_collator, `dataset`: `def bridge_orig_dataset_transform(trajectory: Dict[str, Any]) -> Dict[str, Any]:`
  - line 65, dataset_collator, `dataset`: `Note =>> In original Bridge V2 dataset, the first timestep has an all-zero action, so we remove it!`
  - ... 187 more hits in JSON index

### `prismatic/vla/datasets/rlds/utils/data_utils.py`

- score: `310`
- groups: `dataset_collator, normalization, proprio_state`
- hits: `80`

  - line 4, dataset_collator, `RLDS`: `Additional RLDS-specific data utilities.`
  - line 18, normalization, `normalization`: `from prismatic.vla.constants import NormalizationType`
  - line 52, proprio_state, `proprio`: `def normalize_action_and_proprio(traj: Dict, metadata: Dict, normalization_type: NormalizationType):`
  - line 52, normalization, `normalization`: `def normalize_action_and_proprio(traj: Dict, metadata: Dict, normalization_type: NormalizationType):`
  - line 52, normalization, `normalize`: `def normalize_action_and_proprio(traj: Dict, metadata: Dict, normalization_type: NormalizationType):`
  - line 53, proprio_state, `proprio`: `"""Normalizes the action and proprio fields of a trajectory using the given metadata."""`
  - line 53, normalization, `normalize`: `"""Normalizes the action and proprio fields of a trajectory using the given metadata."""`
  - line 54, proprio_state, `proprio`: `keys_to_normalize = {"action": "action", "proprio": "observation/proprio"}`
  - line 54, normalization, `normalize`: `keys_to_normalize = {"action": "action", "proprio": "observation/proprio"}`
  - line 56, normalization, `normalization`: `if normalization_type == NormalizationType.NORMAL:`
  - line 57, normalization, `normalize`: `for key, traj_key in keys_to_normalize.items():`
  - line 58, normalization, `mean`: `mask = metadata[key].get("mask", tf.ones_like(metadata[key]["mean"], dtype=tf.bool))`
  - ... 68 more hits in JSON index

### `prismatic/vla/datasets/rlds/oxe/configs.py`

- score: `303`
- groups: `config, dataset_collator, proprio_state`
- hits: `73`

  - line 4, dataset_collator, `dataset`: `Defines per-dataset configuration (kwargs) for each dataset in Open-X Embodiment.`
  - line 29, dataset_collator, `dataset`: `from prismatic.vla.datasets.rlds.oxe.utils.droid_utils import zero_action_filter`
  - line 29, dataset_collator, `datasets`: `from prismatic.vla.datasets.rlds.oxe.utils.droid_utils import zero_action_filter`
  - line 29, dataset_collator, `RLDS`: `from prismatic.vla.datasets.rlds.oxe.utils.droid_utils import zero_action_filter`
  - line 32, proprio_state, `proprio`: `# Defines Proprioceptive State Encoding Schemes`
  - line 35, proprio_state, `proprio`: `NONE = -1               # No Proprioceptive State`
  - line 53, dataset_collator, `dataset`: `# === Individual Dataset Configs ===`
  - line 54, dataset_collator, `dataset`: `OXE_DATASET_CONFIGS = {`
  - line 86, dataset_collator, `dataset`: `"bridge_dataset": {  # Original version of Bridge V2 from project website`
  - line 126, proprio_state, `robot_state`: `"state_obs_keys": ["robot_state", None],`
  - line 187, proprio_state, `robot_state`: `"state_obs_keys": ["robot_state", None, None, None, None, None, None],`
  - line 191, dataset_collator, `dataset`: `"stanford_kuka_multimodal_dataset_converted_externally_to_rlds": {`
  - ... 61 more hits in JSON index

### `prismatic/models/vlas/openvla.py`

- score: `301`
- groups: `action_head, dataset_collator, normalization`
- hits: `71`

  - line 17, action_head, `action_token`: `from prismatic.vla.action_tokenizer import ActionTokenizer`
  - line 27, normalization, `norm_stats`: `norm_stats: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],`
  - line 28, action_head, `action_token`: `action_tokenizer: ActionTokenizer,`
  - line 32, normalization, `norm_stats`: `self.norm_stats = norm_stats`
  - line 33, action_head, `action_token`: `self.action_tokenizer = action_tokenizer`
  - line 37, action_head, `unnorm`: `self, image: Image, instruction: str, unnorm_key: Optional[str] = None, **kwargs: str`
  - line 37, normalization, `unnorm`: `self, image: Image, instruction: str, unnorm_key: Optional[str] = None, **kwargs: str`
  - line 44, dataset_collator, `dataset`: `@param unnorm_key: Optional dataset name for retrieving un-normalizing statistics; if None, checks that model`
  - line 44, action_head, `unnorm`: `@param unnorm_key: Optional dataset name for retrieving un-normalizing statistics; if None, checks that model`
  - line 44, normalization, `unnorm`: `@param unnorm_key: Optional dataset name for retrieving un-normalizing statistics; if None, checks that model`
  - line 45, dataset_collator, `dataset`: `was trained only on a single dataset, and retrieves those statistics.`
  - line 47, action_head, `unnorm`: `@return Unnormalized (continuous) action vector --> end-effector deltas.`
  - ... 59 more hits in JSON index

### `prismatic/conf/models.py`

- score: `294`
- groups: `config, dataset_collator, training_entrypoint`
- hits: `64`

  - line 9, training_entrypoint, `finetune`: `- Stage 2 (`finetune`) Optimization Hyperparameters`
  - line 39, dataset_collator, `batch`: `align_global_batch_size: int                            # Global Batch Size (divided across processes)`
  - line 40, dataset_collator, `batch`: `align_per_device_batch_size: int                        # Per-Device Batch Size (per-process)`
  - line 49, training_entrypoint, `train_`: `align_train_strategy: str                               # Align Train Strategy (default: "fsdp-shard-grad-op")`
  - line 51, training_entrypoint, `finetune`: `# Finetune Stage Optimization Parameters`
  - line 52, training_entrypoint, `finetune`: `finetune_epochs: int                                    # Epochs to Run (in case `max_steps` is not specified)`
  - line 53, training_entrypoint, `finetune`: `finetune_max_steps: Optional[int]                       # [Optional] Max Gradient Steps (overrides epochs)`
  - line 54, training_entrypoint, `finetune`: `finetune_global_batch_size: int                         # Global Batch Size (divided across processes)`
  - line 54, dataset_collator, `batch`: `finetune_global_batch_size: int                         # Global Batch Size (divided across processes)`
  - line 55, training_entrypoint, `finetune`: `finetune_per_device_batch_size: int                     # Per-Device Batch Size (per-process)`
  - line 55, dataset_collator, `batch`: `finetune_per_device_batch_size: int                     # Per-Device Batch Size (per-process)`
  - line 58, training_entrypoint, `finetune`: `finetune_learning_rate: float                           # Peak Learning Rate (lr_scheduler sets warmup/decay)`
  - ... 52 more hits in JSON index

### `prismatic/models/backbones/llm/base_llm.py`

- score: `292`
- groups: `config, dataset_collator, normalization, training_entrypoint`
- hits: `12`

  - line 53, config, `checkpoint`: `def enable_gradient_checkpointing(self) -> None: ...`
  - line 89, training_entrypoint, `finetune`: `def last_layer_finetune_modules(self) -> Sequence[nn.Module]: ...`
  - line 132, normalization, `mean`: `# [Contract] `inference_mode` means we're loading from a pretrained checkpoint; no need to load base weights!`
  - line 132, config, `checkpoint`: `# [Contract] `inference_mode` means we're loading from a pretrained checkpoint; no need to load base weights!`
  - line 139, config, `checkpoint`: `#   => Set `decoder.use_cache = False` --> incompatible with gradient checkpointing (+ training in general)`
  - line 144, config, `checkpoint`: `#   => Turns out that when gradient checkpointing is on and the underlying LLM has no "trainable" parameters`
  - line 162, dataset_collator, `dataset`: `# override the `SPECIAL_CASES` set below, but make sure to make the appropriate changes in the `datasets.py``
  - line 162, dataset_collator, `datasets`: `# override the `SPECIAL_CASES` set below, but make sure to make the appropriate changes in the `datasets.py``
  - line 165, config, `oft`: `# Phi-2 Tokenizer doesn't add any BOS tokens by default, and sets BOS == EOS == "<|endoftext|>"`
  - line 190, config, `checkpoint`: `def enable_gradient_checkpointing(self) -> None:`
  - line 191, config, `checkpoint`: `"""Dispatch to underlying LLM instance's `gradient_checkpointing_enable`; defined for all `PretrainedModel`."""`
  - line 192, config, `checkpoint`: `self.llm.gradient_checkpointing_enable()`

### `vla-scripts/extern/convert_openvla_weights_to_hf.py`

- score: `289`
- groups: `config, dataset_collator, normalization`
- hits: `39`

  - line 13, config, `model_path`: `--openvla_model_path_or_id <PATH TO PRISMATIC TRAINING RUN DIR> \`
  - line 14, config, `checkpoint`: `--output_hf_model_local_path <OUTPUT DIR FOR CONVERTED CHECKPOINT>`
  - line 41, config, `model_path`: `openvla_model_path_or_id: Union[str, Path] = (                      # Path to Pretrained VLA (on disk or HF Hub)`
  - line 120, config, `model_path`: `print(f"[*] Converting OpenVLA Model `{cfg.openvla_model_path_or_id}` to HF Transformers Format")`
  - line 123, dataset_collator, `dataset`: `# Get `config.json`, 'dataset_statistics.json' and `checkpoint_pt` -- mirrors logic in `prismatic.models.load.py``
  - line 123, config, `checkpoint`: `# Get `config.json`, 'dataset_statistics.json' and `checkpoint_pt` -- mirrors logic in `prismatic.models.load.py``
  - line 124, config, `model_path`: `if os.path.isdir(cfg.openvla_model_path_or_id):`
  - line 125, config, `model_path`: `print(f"[*] Loading from Local Path `{(run_dir := Path(cfg.openvla_model_path_or_id))}`")`
  - line 126, config, `checkpoint`: `config_json, checkpoint_pt = run_dir / "config.json", run_dir / "checkpoints" / "latest-checkpoint.pt"`
  - line 127, dataset_collator, `dataset`: `dataset_statistics_json = run_dir / "dataset_statistics.json"`
  - line 130, config, `checkpoint`: `assert checkpoint_pt.exists(), f"Missing checkpoint for `{run_dir = }`"`
  - line 131, dataset_collator, `dataset`: `assert dataset_statistics_json.exists(), f"Missing `dataset_statistics.json` for `{run_dir = }`"`
  - ... 27 more hits in JSON index

### `prismatic/vla/datasets/rlds/traj_transforms.py`

- score: `287`
- groups: `action_head, config, dataset_collator, normalization`
- hits: `7`

  - line 5, normalization, `mean`: `that represents a single trajectory, meaning each tensor has the same leading dimension (the trajectory length).`
  - line 26, action_head, `action_dim`: `action_dim = traj["action"].shape[-1]`
  - line 32, action_head, `action_chunk`: `action_chunk_indices = tf.broadcast_to(`
  - line 44, action_head, `action_chunk`: `floored_action_chunk_indices = tf.minimum(tf.maximum(action_chunk_indices, 0), goal_timestep[:, None])`
  - line 47, action_head, `action_chunk`: `traj["action"] = tf.gather(traj["action"], floored_action_chunk_indices)`
  - line 54, dataset_collator, `dataset`: `traj["dataset_name"] = tf.gather(traj["dataset_name"], tf.range(effective_traj_len))`
  - line 54, config, `dataset_name`: `traj["dataset_name"] = tf.gather(traj["dataset_name"], tf.range(effective_traj_len))`

### `experiments/robot/aloha/real_env.py`

- score: `280`
- groups: `action_head, normalization, proprio_state`
- hits: `40`

  - line 7, action_head, `unnorm`: `from experiments.robot.aloha.constants import DT, START_ARM_POSE, MASTER_GRIPPER_JOINT_NORMALIZE_FN, PUPPET_GRIPPER_JOINT_UNNORMALIZE_FN`
  - line 7, normalization, `normalize`: `from experiments.robot.aloha.constants import DT, START_ARM_POSE, MASTER_GRIPPER_JOINT_NORMALIZE_FN, PUPPET_GRIPPER_JOINT_UNNORMALIZE_FN`
  - line 7, normalization, `unnormalize`: `from experiments.robot.aloha.constants import DT, START_ARM_POSE, MASTER_GRIPPER_JOINT_NORMALIZE_FN, PUPPET_GRIPPER_JOINT_UNNORMALIZE_FN`
  - line 7, normalization, `unnorm`: `from experiments.robot.aloha.constants import DT, START_ARM_POSE, MASTER_GRIPPER_JOINT_NORMALIZE_FN, PUPPET_GRIPPER_JOINT_UNNORMALIZE_FN`
  - line 8, normalization, `normalize`: `from experiments.robot.aloha.constants import PUPPET_GRIPPER_POSITION_NORMALIZE_FN, PUPPET_GRIPPER_VELOCITY_NORMALIZE_FN`
  - line 21, proprio_state, `qpos`: `Action space:      [left_arm_qpos (6),             # absolute joint position`
  - line 22, normalization, `normalize`: `left_gripper_positions (1),    # normalized gripper position (0: close, 1: open)`
  - line 23, proprio_state, `qpos`: `right_arm_qpos (6),            # absolute joint position`
  - line 24, normalization, `normalize`: `right_gripper_positions (1),]  # normalized gripper position (0: close, 1: open)`
  - line 26, proprio_state, `qpos`: `Observation space: {"qpos": Concat[ left_arm_qpos (6),          # absolute joint position`
  - line 27, normalization, `normalize`: `left_gripper_position (1),  # normalized gripper position (0: close, 1: open)`
  - line 28, proprio_state, `qpos`: `right_arm_qpos (6),         # absolute joint position`
  - ... 28 more hits in JSON index

### `prismatic/training/metrics.py`

- score: `267`
- groups: `config, dataset_collator, normalization`
- hits: `37`

  - line 16, config, `wandb`: `import wandb`
  - line 65, config, `wandb`: `self.project, self.entity, self.group, self.wandb_dir = project, entity, group, self.run_dir`
  - line 72, config, `wandb`: `wandb.init(`
  - line 74, config, `wandb`: `dir=self.wandb_dir,`
  - line 83, config, `wandb`: `wandb.config = self.hparams`
  - line 87, config, `wandb`: `wandb.log(metrics, step=global_step)`
  - line 92, config, `wandb`: `wandb.finish()`
  - line 109, config, `wandb`: `wandb_project: str = "prismatic",`
  - line 110, config, `wandb`: `wandb_entity: Optional[str] = None,`
  - line 121, config, `wandb`: `elif tracker_type == "wandb":`
  - line 123, config, `wandb`: `run_id, run_dir, hparams, project=wandb_project, entity=wandb_entity, group=self.stage`
  - line 184, normalization, `mean`: `loss_raw = torch.stack(list(self.state["loss_raw"])).mean().item()`
  - ... 25 more hits in JSON index

### `prismatic/conf/vla.py`

- score: `261`
- groups: `config, dataset_collator, training_entrypoint`
- hits: `31`

  - line 8, config, `freeze`: `- VLA Model Architecture / Parameters (e.g., freeze vision encoder, last layer finetuning)`
  - line 25, config, `freeze`: `freeze_vision_backbone: bool                    # Freeze Vision Backbone Parameters (akin to pretraining)`
  - line 26, config, `freeze`: `freeze_llm_backbone: bool                       # Freeze LLM Backbone parameters`
  - line 27, config, `freeze`: `unfreeze_last_llm_layer: bool                   # Unfreeze final layer of LLM (only takes effect if LLM is frozen)`
  - line 30, dataset_collator, `dataset`: `data_mix: str                                   # Open-X Embodiment Dataset =>> Unique Mixture ID (e.g., `bridge`)`
  - line 38, dataset_collator, `batch`: `global_batch_size: int                          # Global Batch Size (divided across processes / world size)`
  - line 39, dataset_collator, `batch`: `per_device_batch_size: int                      # Per-Device Batch Size (per-process / individual GPU)`
  - line 48, training_entrypoint, `train_`: `train_strategy: str                             # Train Strategy (default "fsdp-full-shard")`
  - line 50, config, `checkpoint`: `# Enable Gradient/Activation Checkpointing (for the LLM Backbone)`
  - line 51, config, `checkpoint`: `enable_gradient_checkpointing: bool = True      # Enable Gradient/Activation Checkpointing during Training`
  - line 69, config, `freeze`: `freeze_vision_backbone: bool = False`
  - line 70, config, `freeze`: `freeze_llm_backbone: bool = False`
  - ... 19 more hits in JSON index

### `prismatic/models/registry.py`

- score: `260`
- groups: `dataset_collator, training_entrypoint`
- hits: `153`

  - line 20, dataset_collator, `dataset`: `"datasets": ["LLaVa v1.5 Instruct"],`
  - line 20, dataset_collator, `datasets`: `"datasets": ["LLaVa v1.5 Instruct"],`
  - line 21, training_entrypoint, `train_`: `"train_epochs": 1,`
  - line 33, dataset_collator, `dataset`: `"datasets": ["LLaVa v1.5 Instruct"],`
  - line 33, dataset_collator, `datasets`: `"datasets": ["LLaVa v1.5 Instruct"],`
  - line 34, training_entrypoint, `train_`: `"train_epochs": 1,`
  - line 57, dataset_collator, `dataset`: `"datasets": ["LLaVa v1.5 Instruct"],`
  - line 57, dataset_collator, `datasets`: `"datasets": ["LLaVa v1.5 Instruct"],`
  - line 58, training_entrypoint, `train_`: `"train_epochs": 1,`
  - line 74, dataset_collator, `dataset`: `"datasets": ["LLaVa v1.5 Instruct"],`
  - line 74, dataset_collator, `datasets`: `"datasets": ["LLaVa v1.5 Instruct"],`
  - line 75, training_entrypoint, `train_`: `"train_epochs": 1,`
  - ... 141 more hits in JSON index

### `prismatic/training/strategies/ddp.py`

- score: `260`
- groups: `config, dataset_collator, training_entrypoint`
- hits: `30`

  - line 26, config, `checkpoint`: `def save_checkpoint(`
  - line 31, training_entrypoint, `train_`: `train_loss: Optional[float] = None,`
  - line 34, config, `checkpoint`: `"""Save a checkpoint to the `run_dir` only containing the state_dicts for trainable parameters by default."""`
  - line 35, config, `checkpoint`: `assert isinstance(self.vlm, DDP), "save_checkpoint assumes VLM is already wrapped in DDP!"`
  - line 44, config, `checkpoint`: `# Set Checkpoint Path =>> Embed *minimal* training statistics!`
  - line 45, config, `checkpoint`: `checkpoint_dir = run_dir / "checkpoints"`
  - line 46, training_entrypoint, `train_`: `if train_loss is None:`
  - line 47, config, `checkpoint`: `checkpoint_path = checkpoint_dir / f"step-{global_step:06d}-epoch-{epoch:02d}-loss=inf.pt"`
  - line 49, training_entrypoint, `train_`: `checkpoint_path = checkpoint_dir / f"step-{global_step:06d}-epoch-{epoch:02d}-loss={train_loss:.4f}.pt"`
  - line 49, config, `checkpoint`: `checkpoint_path = checkpoint_dir / f"step-{global_step:06d}-epoch-{epoch:02d}-loss={train_loss:.4f}.pt"`
  - line 51, config, `checkpoint`: `# Save Checkpoint & Copy Latest to `latest-checkpoint.pt``
  - line 52, config, `checkpoint`: `torch.save({"model": model_state_dicts, "optimizer": optimizer_state_dict}, checkpoint_path)`
  - ... 18 more hits in JSON index

### `prismatic/vla/datasets/rlds/oxe/mixtures.py`

- score: `260`
- groups: `config, dataset_collator`
- hits: `99`

  - line 4, dataset_collator, `dataset`: `Defines a registry of dataset mixtures and weights for the Open-X Embodiment Datasets. Each dataset is associated with`
  - line 4, dataset_collator, `datasets`: `Defines a registry of dataset mixtures and weights for the Open-X Embodiment Datasets. Each dataset is associated with`
  - line 12, dataset_collator, `dataset`: `# === Bridge V2 Dataset ===`
  - line 61, dataset_collator, `dataset`: `("stanford_hydra_dataset_converted_externally_to_rlds", 1.0),`
  - line 61, dataset_collator, `RLDS`: `("stanford_hydra_dataset_converted_externally_to_rlds", 1.0),`
  - line 62, dataset_collator, `dataset`: `("austin_buds_dataset_converted_externally_to_rlds", 3.0),`
  - line 62, dataset_collator, `RLDS`: `("austin_buds_dataset_converted_externally_to_rlds", 3.0),`
  - line 63, dataset_collator, `dataset`: `("nyu_franka_play_dataset_converted_externally_to_rlds", 3.0),`
  - line 63, dataset_collator, `RLDS`: `("nyu_franka_play_dataset_converted_externally_to_rlds", 3.0),`
  - line 64, dataset_collator, `dataset`: `("maniskill_dataset_converted_externally_to_rlds", 0.1),`
  - line 64, dataset_collator, `RLDS`: `("maniskill_dataset_converted_externally_to_rlds", 0.1),`
  - line 65, dataset_collator, `dataset`: `("furniture_bench_dataset_converted_externally_to_rlds", 0.1),`
  - ... 87 more hits in JSON index

### `vla-scripts/extern/verify_openvla.py`

- score: `259`
- groups: `action_head, config, normalization`
- hits: `9`

  - line 15, config, `model_path`: `MODEL_PATH = "openvla/openvla-7b"`
  - line 24, config, `model_path`: `if "v01" in MODEL_PATH:`
  - line 32, config, `model_path`: `print(f"[*] Verifying OpenVLAForActionPrediction using Model `{MODEL_PATH}`")`
  - line 37, config, `model_path`: `processor = AutoProcessor.from_pretrained(MODEL_PATH, trust_remote_code=True)`
  - line 42, config, `model_path`: `MODEL_PATH,`
  - line 52, config, `model_path`: `#     MODEL_PATH,`
  - line 63, config, `model_path`: `#     MODEL_PATH,`
  - line 84, action_head, `unnorm`: `action = vla.predict_action(**inputs, unnorm_key="bridge_orig", do_sample=False)`
  - line 84, normalization, `unnorm`: `action = vla.predict_action(**inputs, unnorm_key="bridge_orig", do_sample=False)`

### `prismatic/preprocessing/download.py`

- score: `258`
- groups: `action_head, dataset_collator, training_entrypoint`
- hits: `28`

  - line 4, dataset_collator, `dataset`: `Utility functions for downloading and extracting various datasets to (local) disk.`
  - line 4, dataset_collator, `datasets`: `Utility functions for downloading and extracting various datasets to (local) disk.`
  - line 24, dataset_collator, `dataset`: `# === Dataset Registry w/ Links ===`
  - line 26, dataset_collator, `dataset`: `DatasetComponent = TypedDict(`
  - line 27, dataset_collator, `dataset`: `"DatasetComponent",`
  - line 32, dataset_collator, `dataset`: `DATASET_REGISTRY: Dict[str, List[DatasetComponent]] = {`
  - line 33, dataset_collator, `dataset`: `# === LLaVa v1.5 Dataset(s) ===`
  - line 35, dataset_collator, `dataset`: `# Note =>> This is the full suite of datasets included in the LLaVa 1.5 "finetuning" stage; all the LLaVa v1.5`
  - line 35, dataset_collator, `datasets`: `# Note =>> This is the full suite of datasets included in the LLaVa 1.5 "finetuning" stage; all the LLaVa v1.5`
  - line 36, training_entrypoint, `finetune`: `#          models are finetuned on this split. We use this dataset for all experiments in our paper.`
  - line 36, dataset_collator, `dataset`: `#          models are finetuned on this split. We use this dataset for all experiments in our paper.`
  - line 41, dataset_collator, `dataset`: `"url": "https://huggingface.co/datasets/liuhaotian/LLaVA-Pretrain/resolve/main/blip_laion_cc_sbu_558k.json",`
  - ... 16 more hits in JSON index

### `prismatic/util/data_utils.py`

- score: `252`
- groups: `config, dataset_collator, proprio_state`
- hits: `22`

  - line 31, dataset_collator, `collator`: `class PaddedCollatorForLanguageModeling:`
  - line 47, dataset_collator, `batch`: `input_ids = pad_sequence(input_ids, batch_first=True, padding_value=self.pad_token_id)`
  - line 48, dataset_collator, `batch`: `labels = pad_sequence(labels, batch_first=True, padding_value=IGNORE_INDEX)`
  - line 96, dataset_collator, `collator`: `class PaddedCollatorForActionPrediction:`
  - line 105, dataset_collator, `dataset`: `if "dataset_name" in instances[0]:`
  - line 105, config, `dataset_name`: `if "dataset_name" in instances[0]:`
  - line 106, dataset_collator, `dataset`: `dataset_names = [instance["dataset_name"] for instance in instances]`
  - line 106, config, `dataset_name`: `dataset_names = [instance["dataset_name"] for instance in instances]`
  - line 108, dataset_collator, `dataset`: `dataset_names = None`
  - line 108, config, `dataset_name`: `dataset_names = None`
  - line 113, dataset_collator, `batch`: `input_ids = pad_sequence(input_ids, batch_first=True, padding_value=self.pad_token_id)`
  - line 114, dataset_collator, `batch`: `labels = pad_sequence(labels, batch_first=True, padding_value=IGNORE_INDEX)`
  - ... 10 more hits in JSON index

### `scripts/extern/convert_prismatic_weights_to_hf.py`

- score: `252`
- groups: `config, dataset_collator, normalization`
- hits: `22`

  - line 34, config, `model_path`: `prismatic_model_path_or_id: Union[str, Path] = (                    # Path to Pretrained VLM (on disk or HF Hub)`
  - line 106, config, `model_path`: `print(f"[*] Converting Prismatic Model `{cfg.prismatic_model_path_or_id}` to HF Transformers Format")`
  - line 109, config, `checkpoint`: `# Get `config.json` and `checkpoint_pt` -- mirrors logic in `prismatic.models.load.py``
  - line 110, config, `model_path`: `if os.path.isdir(cfg.prismatic_model_path_or_id):`
  - line 111, config, `model_path`: `print(f"[*] Loading from Local Path `{(run_dir := Path(cfg.prismatic_model_path_or_id))}`")`
  - line 112, config, `checkpoint`: `config_json, checkpoint_pt = run_dir / "config.json", run_dir / "checkpoints" / "latest-checkpoint.pt"`
  - line 115, config, `checkpoint`: `assert checkpoint_pt.exists(), f"Missing checkpoint for `{run_dir = }`"`
  - line 117, config, `checkpoint`: `print(f"[*] Downloading Prismatic Checkpoint from HF Hub :: `TRI-ML/{cfg.prismatic_model_path_or_id}`")`
  - line 117, config, `model_path`: `print(f"[*] Downloading Prismatic Checkpoint from HF Hub :: `TRI-ML/{cfg.prismatic_model_path_or_id}`")`
  - line 118, config, `model_path`: `config_json = hf_hub_download("TRI-ML/prismatic-vlms", f"{cfg.prismatic_model_path_or_id}/config.json")`
  - line 119, config, `checkpoint`: `checkpoint_pt = hf_hub_download(`
  - line 120, config, `checkpoint`: `"TRI-ML/prismatic-vlms", f"{cfg.prismatic_model_path_or_id}/checkpoints/latest-checkpoint.pt"`
  - ... 10 more hits in JSON index

## What To Confirm Manually Next

1. Exact training script to extend for UAV JSONL.
2. Exact dataset/collator path that creates image-language-action batches.
3. Whether OpenVLA-OFT already supports continuous action chunks and proprio.
4. Where action dimension and chunk size are configured.
5. Where normalization stats are loaded and applied.
6. Whether a UAV-specific dataset class can be added without touching core model code.

## Current Decision

- CODE_SCAN_PASS
- MODEL_NOT_LOADED
- TRAINING_NOT_STARTED
- MODEL_STAGE_CONFIRMATION_REQUIRED
