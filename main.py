import hydra
from omegaconf import DictConfig, OmegaConf
import wandb
import logging
from src.data_ingestion import run_ingestion

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
    
    log.info(f"Run ingestion for dataset: {cfg.data.dataset_name})")
    df = run_ingestion(
        dataset_name = cfg.data.dataset_name,
        subset = cfg.data.subset,
        target_count = cfg.data.max_samples
        )
    if not df.empty:
        log.info(f"Dataset loaded with {len(df)} samples.")
        table = wandb.Table(dataframe=df)
        wandb.log({"raw_data_table": table})
    else:
        log.error("No data sampled")
    
    wandb.finish()

if __name__ == "__main__":
    main()
