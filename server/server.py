
from dotenv import load_dotenv
load_dotenv()

from typing import Dict
class MessageSession:
    def __init__(self):
        self.session_id = ""
        self.create_timestamp = ""
        self.memory_count = 0
        
        self.llm = ""
        self.memory = ""
        self.agent = ""
MESSAGE_SESSION_MAP: Dict[str, MessageSession] = {}


from flask import Flask, request, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/message', methods=['POST'])
def message():
    human_message = request.form.get('humanMessage')
    tab_id = session.get('tab_id')
    if not tab_id:
        tab_id = os.urandom(24).hex()
        session['tab_id'] = tab_id
    return {'humanMessage': human_message, 'tabId': tab_id}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
