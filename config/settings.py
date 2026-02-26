from utils.config_manager import load_environment_config
import os


class Settings:

    def __init__(self):

        env_name = os.getenv("TEST_ENV", "dev")

        env_config = load_environment_config(env_name)

        self.ENV = env_name
        self.BASE_URL = env_config.get("base_url")
        self.API_URL = env_config.get("api_url")
        self.CREDENTIALS = env_config.get("credentials")


settings = Settings()