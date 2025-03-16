import yaml
from pathlib import Path


def load_yaml_data(filepath: str):
    # Correctly resolve absolute path to the project root
    base_path = Path(__file__).resolve().parent.parent
    full_path = (base_path / filepath).resolve()
    with open(full_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
