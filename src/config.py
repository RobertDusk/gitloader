import configparser
from pathlib import Path


config = configparser.ConfigParser()


def get_config_path() -> Path:
    return Path(Path.home(), ".config/gitloader/config.ini")

    
def ensure_exists() -> None:
    config_file = get_config_path()
    if not config_file.exists():
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.touch()


def load() -> dict:
    config_file = get_config_path()
    config.read(config_file)
    return config

    
def save() -> None:
    config_file = get_config_path()
    with open(config_file, "w") as f:
        print(f"Saving config to {config_file}")
        config.write(f)


ensure_exists()
load()