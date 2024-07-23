from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from questionmodel import QuestionModel
from main_prog import getsqlresponse,get_schema,run_query
import uvicorn

# origins = ["http://localhost:4200"]
app = FastAPI()
handler = Mangum(app)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

import gradio as gr

def gradio_predict(question: str):
    result = getsqlresponse(question)
    return result.content

demo = gr.Interface(
    fn=gradio_predict,
    inputs=gr.Textbox(label="Ask a question", placeholder="[Ex.]How many albums are there?"),
    outputs=[gr.Textbox(label="Answer")],
    allow_flagging="never",
    title="Talk to your data!!"
)

demo.launch()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int,q: Union[str, None] = None):
#     return {"item_id":item_id, "q":q}

# @app.post("/getresponse")
# def getresponse(question: QuestionModel):
#     print("Get response..");
#     result = getsqlresponse(question.question)
#     return getsqlresponse(question)

# app = gr.mount_gradio_app(app, demo, path="/")
