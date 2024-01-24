from langchain.agents import AgentType, initialize_agent
from agent_toolkits.coupon.toolkit import SAPToolkit
from utilities.coupon import SAPAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv("./secret/.env")

llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, temperature=0)

sap = SAPAPIWrapper()
toolkit = SAPToolkit.from_sap_api_wrapper(sap)
tools = toolkit.get_tools()

for tool in tools:
    print(tool.name)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)


output = agent.run("""Spring Festival is coming, create a coupon for the pants, valid from 9th Feb to 18th Feb 2024""")