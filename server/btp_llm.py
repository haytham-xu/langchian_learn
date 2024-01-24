import json
import requests
from typing import Any, List, Mapping, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

class CustomLLM(LLM):
    n: int

    @property
    def _llm_type(self) -> str:
        return "btp_llm_proxy_gpt-4-turbo"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any,) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        # Add your code here
        KEY_FILE = "secret.json"

        with open(KEY_FILE, "r") as key_file:
            svc_key = json.load(key_file)

        svc_url = svc_key["url"]
        client_id = svc_key["uaa"]["clientid"]
        client_secret = svc_key["uaa"]["clientsecret"]
        uaa_url = svc_key["uaa"]["url"]

        params = {"grant_type": "client_credentials" }
        resp = requests.post(f"{uaa_url}/oauth/token",
                             auth=(client_id, client_secret),
                             params=params)

        token = resp.json()["access_token"]

        data = {
            "deployment_id": "gpt-4-turbo",
            "messages": prompt,
            "max_tokens": 800,
            "temperature": 0.7,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 0.95,
            "stop": "null"
        }

        headers = {
            "Authorization":  f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(f"{svc_url}/api/v1/completions",
                                 headers=headers,
                                 json=data)
        return response.json()

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}