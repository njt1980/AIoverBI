import re
import os
import gradio as gr
from langchain_community.utilities import SQLDatabase
# db = SQLDatabase.from_uri(os.getenv('db'))
def get_schema(_):
  print("Table Info :", SQLDatabase.from_uri(os.getenv('db')).get_table_info());
  return SQLDatabase.from_uri(os.getenv('db')).get_table_info();
  # return os.get

def get_db_openaikey(database,openai_key,databasename):
  os.environ['db'] = database;
  os.environ['OPENAI_API_KEY'] = openai_key;
  return [gr.Textbox(visible=False),
          gr.Textbox(visible=False),
          gr.Textbox(visible=False),
          gr.Button(visible=False),
          gr.Row(visible=True),
          gr.Textbox(value="Connected to " + databasename,
                     interactive=False,
                     visible=True)]