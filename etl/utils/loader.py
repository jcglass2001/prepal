import yaml
import argparse

def load_yaml_config(filepath: str):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="Path to config.yaml")
    args,_ = parser.parse_known_args()
    return args.config 

def get_config_path():
    cli_config_path = parse_args()
    return cli_config_path

