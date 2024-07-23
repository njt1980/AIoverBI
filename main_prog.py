import os;
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from questionmodel import QuestionModel

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
from langchain_community.utilities import SQLDatabase
db = SQLDatabase.from_uri("sqlite:///./Chinook.db")

def get_schema(_):
    return db.get_table_info()

def run_query(query):
    return db.run(query)

def getsqlresponse(question : str):
    question = question
    template = """"Based on the table below, write a SQL query that would answer the user's question:
    {schema}
    Question: {question}
    SQL Query:
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI()

    sql_response = (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | model.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )

    template_ = """Based on the table schema below, question, sql query, and sql reponse, provide a natural language response
    {schema}
    Question: {question}
    SQL Query: {query}
    SQL Response: {response}
    """
    prompt_response = ChatPromptTemplate.from_template(template_)

    full_chain = (
        RunnablePassthrough.assign(query=sql_response).assign(
            schema=get_schema,
            response=lambda x: db.run(x["query"])
        )
        | prompt_response
        | model
    )

    response = full_chain.invoke({"question":question});
    print(response)
    return response

# q = QuestionModel(question='How many albums are there?')

# getsqlresponse(q)