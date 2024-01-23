
from dotenv import load_dotenv
load_dotenv()

from typing import Dict
from langchain.chains import LLMChain
from langchain.prompts import (ChatPromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder,SystemMessagePromptTemplate,)
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from flask import Flask, request
from flask_cors import CORS
import os, json

from dotenv import load_dotenv
load_dotenv()


from langchain.agents import AgentType, initialize_agent, create_react_agent, create_json_agent, create_structured_chat_agent
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from langchain_openai import ChatOpenAI

class MessageSession:
    def __init__(self, tab_id):
        self.tab_id = tab_id
        self.create_timestamp = ""
        self.memory_count = 0
        
        # llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        # github = GitHubAPIWrapper()
        # toolkit = GitHubToolkit.from_github_api_wrapper(github)
        # tools = toolkit.get_tools()

        # agent = initialize_agent(
        #     tools,
        #     llm,
        #     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        #     verbose=True,
        # )
    
        # agent.run(
        #     "How many issues do we have?"
        # )
        
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template("You are a nice chatbot having a conversation with a human."),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )
        self.chat_history = MessagesPlaceholder(variable_name="chat_history")
        github = GitHubAPIWrapper()
        toolkit = GitHubToolkit.from_github_api_wrapper(github)
        self.tools = toolkit.get_tools()

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.conversation = LLMChain(llm=self.llm, prompt=self.prompt, verbose=True, memory=self.memory)
        # create_react_agent(tools=self.tools, llm=self.llm, agent_kwargs={})
        # create_json_agent()
        # create_structured_chat_agent()
        # create_react_agent, create_json_agent, create_structured_chat_agent
        self.agent = initialize_agent(
            tools=self.tools, 
            llm=self.llm, 
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
            verbose=True, 
            memoty=self.memory, 
            # prompt=self.prompt,
            # agent_kwargs={
            #     "memory_prompts": [self.chat_history],
            #     "input_variables": ["input", "agent_scratchpad", "chat_history"],
            #     "prefix": self.prompt,
            # },
        )

    def involve(self, human_message):
        # return self.conversation.invoke({"question": human_message})
        return self.agent.invoke(human_message)
    
MESSAGE_SESSION_MAP: Dict[str, MessageSession] = {}



app = Flask(__name__, static_folder='')
app.secret_key = os.urandom(24)
CORS(app)

@app.route('/message', methods=['POST'])
def message():
    human_message = request.json.get('humanMessage')
    tab_id = request.json.get('tabId')
    
    global MESSAGE_SESSION_MAP
    if tab_id not in MESSAGE_SESSION_MAP:
        tab_id = str(os.urandom(24).hex())
        message_session = MessageSession(tab_id)
        MESSAGE_SESSION_MAP[tab_id] = message_session
    else:
        print("existing tab: ", tab_id)
        message_session = MESSAGE_SESSION_MAP[tab_id]
    res = message_session.involve(human_message)
    print(res)
    return json.dumps({
        "tabId": tab_id,
        "text": res["output"]})
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


