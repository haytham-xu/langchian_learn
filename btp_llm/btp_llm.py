   
    
import json
import requests
from typing import Any, List, Mapping, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

# from dotenv import load_dotenv
# load_dotenv()

from typing import Dict
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.memory import ConversationSummaryBufferMemory
from langchain.memory import ConversationSummaryMemory
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os, json
from langchain_core.output_parsers import StrOutputParser

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
            "messages": [
                {"role": "user", "content": prompt}
            ],
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
        print(response.json())
        return response.json()

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}
    
llm = CustomLLM(n=10)
print(llm._call("hi"))
# llm.invoke("Hello.")


# llm = ChatOpenAI(temperature=0)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template("You are a nice chatbot having a conversation with a human."),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)
conversation.invoke({"question": "Hello"})
        