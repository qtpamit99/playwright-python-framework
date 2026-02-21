import os
import yaml


def load_environment_config(env_name: str):
    """
    Load environment-specific configuration from environments.yaml
    """

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, "config", "environments.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(" environments.yaml not found")

    with open(config_path, "r") as file:
        configs = yaml.safe_load(file)

    env_config = configs.get(env_name)

    if not env_config:
        raise ValueError(f" Environment '{env_name}' not defined")

    return env_config


#  NEW – Credential Helper (Safe Upgrade)
def get_credentials(env_name: str):
    """
    Fetch credentials from environment config
    """

    env_config = load_environment_config(env_name)

    credentials = env_config.get("credentials")

    if not credentials:
        raise ValueError(f" No credentials defined for environment '{env_name}'")

    username = credentials.get("username")
    password = credentials.get("password")

    if not username or not password:
        raise ValueError(f" Incomplete credentials for environment '{env_name}'")

    return username, password
