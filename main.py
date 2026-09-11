import json
from pathlib import Path
from src.generator import WalmartConnectDataGenerator

if __name__ == "__main__":
    config_path = Path("config/config.json")
    
    if not config_path.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config_dict = json.load(f)

    default_config = config_dict.get("DEFAULT_CONFIG", {})
    campaigns = config_dict.get("WALMART_CAMPAIGNS_CONFIG", [])
    output_path = Path(default_config.get("output_csv_path", "data/output/walmart_connect_campaigns_configurable.csv"))

    generator = WalmartConnectDataGenerator(config=default_config, campaigns=campaigns)
    df_generator = generator.generate_dataset()
    