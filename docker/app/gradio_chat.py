import gradio as gr
from main_prog_chat import predict
from helper_functions import get_db_openaikey
import os

show_chatinterface_flag = False;
with gr.Blocks() as demo:
    database = gr.Textbox(show_label=False,placeholder="Enter the database URN");
    openaikey = gr.Textbox(show_label=False,
                           placeholder="Enter your OpenAI key",
                           type="password");
    databasename = gr.Textbox(show_label=False,placeholder="Enter friendly database name(ex. trades, customers)");
    button = gr.Button(value="Let's talk..");
    with gr.Column(visible=False) as chat_col:
        conn = gr.Textbox(value="Connected to " + databasename.value,
                          interactive=False,
                          show_label=False);
        chat = gr.ChatInterface(predict);

    button.click(get_db_openaikey,[database,openaikey,databasename],[database,openaikey,databasename,button,chat_col,conn])
demo.launch(server_name="0.0.0.0",server_port=7860)