from langchain_community.utilities import SQLDatabase
db = SQLDatabase.from_uri("sqlite:///./Chinook.db")
def get_schema(_):
  return db.get_table_info();

