import json
from utils.config_manager import load_environment_config

class AuthAPI:
    def __init__(self, request_context, env_name="dev"):
        self.request = request_context
        env_config = load_environment_config(env_name)
        self.base_url = env_config["api_url"]
        self.ui_base_url = env_config["base_url"]

    def check_token(self, token: str):
        payload = {"token": token}
        response = self.request.post(
            f"{self.base_url}/check",
            data=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "Origin": self.ui_base_url,
                "Referer": self.ui_base_url
            }
        )
        if response.status != 200:
            raise Exception(
                f" Token check failed (HTTP {response.status}): {response.text()}"
            )
        return response.json()