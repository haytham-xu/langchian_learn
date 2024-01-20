
from dotenv import load_dotenv
load_dotenv()

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
import os, json
from langchain_core.output_parsers import StrOutputParser
class MessageSession:
    def __init__(self, tab_id):
        self.tab_id = tab_id
        self.create_timestamp = ""
        self.memory_count = 0
        
        self.llm = ChatOpenAI(temperature=0)
        self.prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template("You are a nice chatbot having a conversation with a human."),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.conversation = LLMChain(llm=self.llm, prompt=self.prompt, verbose=True, memory=self.memory)

    def involve(self, human_message):
        # print(self.conversation.invoke({"question": human_message}))
        return self.conversation.invoke({"question": human_message})
    
MESSAGE_SESSION_MAP: Dict[str, MessageSession] = {}



# app = Flask(__name__)
app = Flask(__name__, static_folder='')
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'ui.html')

@app.route('/message', methods=['POST'])
def message():
    human_message = request.form.get('humanMessage')
    tab_id = str(request.cookies.get('tab_id'))
    
    global MESSAGE_SESSION_MAP
    if tab_id not in MESSAGE_SESSION_MAP:
        tab_id = str(os.urandom(24).hex())
        print(tab_id)
        message_session = MessageSession(tab_id)
        MESSAGE_SESSION_MAP[tab_id] = message_session
    else:
        message_session = MESSAGE_SESSION_MAP[tab_id]
    res = message_session.involve(human_message)
    # print(res, type(res))
    return json.dumps(str(res['text']))
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

# curl -b "tab_id=value" -X POST -d "humanMessage=Hello" http://127.0.0.1:5001/message
# curl -b "tab_id=" -X POST -d "humanMessage=tell me a joke" http://127.0.0.1:5001/message

'''
{
    'question': 'tell me a joke', 
    'chat_history': [
        HumanMessage(content='Hello'), 
        AIMessage(content='Hello! How can I assist you today?'), 
        HumanMessage(content='tell me a joke'), 
        AIMessage(content="Sure, here's a classic one for you:\n\nWhy don't scientists trust atoms?\n\nBecause they make up everything!")
    ], 
    'text': "Sure, here's a classic one for you:\n\nWhy don't scientists trust atoms?\n\nBecause they make up everything!"
}
'''
