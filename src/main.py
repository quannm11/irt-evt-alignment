import hydra
from omegaconf import DictConfig, OmegaConf
import wandb
import logging

log = logging.getLogger(__name__)

@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: DictConfig):
    
    run = wandb.init(
        project=cfg.project_name,
        config=OmegaConf.to_container(cfg, resolve=True),
        tags=cfg.wandb.tags,
        job_type="eval_run"
    )
    
    print(f"\n W&B Run Initialized: {run.name}")
    print("="*30)
    print("Experiment Configuration:")
    print(OmegaConf.to_yaml(cfg))
    print("="*30)

    log.info(f"Loading dataset: {cfg.data.dataset_name} ({cfg.data.subset})")
    log.info(f"Using Judge Model: {cfg.judge.model_name}")

    wandb.log({"status": "setup_complete", "sample_metric": 0.99})
    
    log.info("Run Complete. Finishing W&B run.")
    wandb.finish()

if __name__ == "__main__":
    main()
