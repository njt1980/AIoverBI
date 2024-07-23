import os;
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.tools.convert_to_openai import format_tool_to_openai_tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from helper_functions import get_schema
#-------------------------------------------------------------------------------------------------------
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
MEMORY_KEY = "chat_history"
db = SQLDatabase.from_uri("sqlite:///./Chinook.db")
system_message_ = 'You are an agent designed to interact with a SQL database.\nGiven an input question, create a syntactically correct sqlite query to run, then look at the results of the query and return the answer.\nUnless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results.\nYou can order the results by a relevant column to return the most interesting examples in the database.\nNever query for all the columns from a specific table, only ask for the relevant columns given the question.\nYou have access to tools for interacting with the database.\nOnly use the below tools. Only use the information returned by the below tools to construct your final answer.\nYou MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.\n\nDO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.\n\nIf the question does not seem related to the database, just return "I don\'t know" as the answer.\n\n\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of accessible tools\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\nThought: I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.\n'

system_message__ = 'You are an agent designed to interact with a SQL database.\nGiven an input question, create a syntactically correct sqlite query to run, then look at the results of the query and return the answer.\nUnless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results.\nYou can order the results by a relevant column to return the most interesting examples in the database.\nNever query for all the columns from a specific table, only ask for the relevant columns given the question.\nYou have access to tools for interacting with the database.\nOnly use the below tools. Only use the information returned by the below tools to construct your final answer.\n If you get an error while executing a query, rewrite the query and try again.\n\nDO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.\n\nIf the question does not seem related to the database, just return "I don\'t know" as the answer.\n\n\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of accessible tools\nAction Input: the input to the action\nObservation: the result of the action\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\nThought: I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.\n'

system_message = 'You are an agent designed to interact with a SQL database.\nGiven an input question, create a syntactically correct sqlite query to run, then look at the results of the query and return the answer.\n\nUse the following format:\n\nUnless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results.\nYou can order the results by a relevant column to return the most interesting examples in the database.\nNever query for all the columns from a specific table, only ask for the relevant columns given the question.\nYou have access to tools for interacting with the database.\nOnly use the below tools. Only use the information returned by the below tools to construct your final answer.\n If you get an error while executing a query, rewrite the query and try again.\n\nDO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.\n\nIf the question does not seem related to the database, just return "I don\'t know" as the answer.\n\n\n Consider the result of the first invocation as the final answer. \n\nBegin!\nThought: I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of accessible tools\nAction Input: the input to the action\nObservation: the result of the action\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question.'
chat_history = []
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         system_message),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user",
         "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        MessagesPlaceholder(variable_name="schema"),
    ]
)
schema = [SystemMessage(content=db.get_table_info())]
toolkit = SQLDatabaseToolkit(db=db,llm=ChatOpenAI(temperature=0))
tools = toolkit.get_tools()
llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
llm_with_tools = llm.bind(tools=[format_tool_to_openai_tool(tool) for tool in tools])
agent = (
    # RunnablePassthrough.assign(schema=get_schema)
    # |
    {
        "input": lambda x:x["input"],
        "agent_scratchpad":lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history":lambda x: x["chat_history"],
        "schema":lambda x:schema
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               verbose=True,
                               max_iterations=10,
                               max_execution_time=120)
# input1 = "How many albums are there?"
# result = agent_executor.invoke({"input":input1,
#                          "chat_history":chat_history})

def predict(query,history):
    chat_history = []
    if len(history) > 0:
        for item in history:
            chat_history.extend(
                [
                    HumanMessage(content=item[0]),
                    AIMessage(content=item[1])
                ])
    result = agent_executor.invoke({"input":query,
                                    "chat_history":chat_history})
    print("chat_history :",chat_history)
    print("result :", result)
    print(result['output'])
    return result["output"]


