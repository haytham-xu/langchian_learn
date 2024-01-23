
# from dotenv import load_dotenv
# load_dotenv()

# from typing import Dict
# from langchain.chains import LLMChain
# from langchain.prompts import (ChatPromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder,SystemMessagePromptTemplate,)
# from langchain_openai import ChatOpenAI
# from langchain.memory import ConversationBufferMemory

# from flask import Flask, request
# from flask_cors import CORS
# import os, json

# class MessageSession:
#     def __init__(self, tab_id):
#         self.tab_id = tab_id
#         self.create_timestamp = ""
#         self.memory_count = 0
        
#         self.llm = ChatOpenAI(temperature=0)
#         self.prompt = ChatPromptTemplate(
#             messages=[
#                 SystemMessagePromptTemplate.from_template("You are a nice chatbot having a conversation with a human."),
#                 MessagesPlaceholder(variable_name="chat_history"),
#                 HumanMessagePromptTemplate.from_template("{question}"),
#             ]
#         )
#         self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
#         self.conversation = LLMChain(llm=self.llm, prompt=self.prompt, verbose=True, memory=self.memory)

#     def involve(self, human_message):
#         return self.conversation.invoke({"question": human_message})
    
# MESSAGE_SESSION_MAP: Dict[str, MessageSession] = {}



# app = Flask(__name__, static_folder='')
# app.secret_key = os.urandom(24)
# CORS(app)

# @app.route('/message', methods=['POST'])
# def message():
#     human_message = request.json.get('humanMessage')
#     tab_id = request.json.get('tabId')
    
#     global MESSAGE_SESSION_MAP
#     if tab_id not in MESSAGE_SESSION_MAP:
#         tab_id = str(os.urandom(24).hex())
#         message_session = MessageSession(tab_id)
#         MESSAGE_SESSION_MAP[tab_id] = message_session
#     else:
#         print("existing tab: ", tab_id)
#         message_session = MESSAGE_SESSION_MAP[tab_id]
#     res = message_session.involve(human_message)
#     return json.dumps({
#         "tabId": tab_id,
#         "text": res['text']})
    
    
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)

from dotenv import load_dotenv
load_dotenv()

import os

from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from langchain_openai import ChatOpenAI

os.environ["GITHUB_APP_ID"] = "804272"
os.environ["GITHUB_APP_PRIVATE_KEY"] = "server/for-langchian-learn.2024-01-22.private-key.pem"
os.environ["GITHUB_REPOSITORY"] = "haytham-xu/book-management-system"
os.environ["GITHUB_BRANCH"] = "bot-branch-name"
os.environ["GITHUB_BASE_BRANCH"] = "main"

print(os.path.exists("server/for-langchian-learn.2024-01-22.private-key.pem"))

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
github = GitHubAPIWrapper()
toolkit = GitHubToolkit.from_github_api_wrapper(github)
tools = toolkit.get_tools()

# STRUCTURED_CHAT includes args_schema for each tool, helps tool args parsing errors.
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
print("Available tools:")
for tool in tools:
    print("\t" + tool.name)