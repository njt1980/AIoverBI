import gradio as gr
from main_prog_chat import predict
from helper_functions import get_db_openaikey
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import os
import main_prog_chat
css = """
.bold-italic-text {
    font-style: italic;
    font-weight: bold;
}
"""
markdown_text = """
<div style="text-align: center;">
    <strong>DBTalker</strong>
</div>
"""

show_chatinterface_flag = False;

def plot_function():
    print("in plot function..")
    # print(main_prog_chat.image_placeholder)
    return main_prog_chat.image_placeholder
#New code
with gr.Blocks(css=css) as demo:
    header = gr.Markdown(value=markdown_text)
    database = gr.Textbox(show_label=False,placeholder="Enter the database URN");
    openaikey = gr.Textbox(show_label=False,
                           placeholder="Enter your OpenAI key",
                           type="password");
    databasename = gr.Textbox(show_label=False,placeholder="Enter friendly database name(ex. trades, customers)",value="");
    button = gr.Button(value="Let's talk..");
    # New Code
    
    with gr.Row(visible=False) as row_:
            with gr.Column():
                chat = gr.ChatInterface(predict);
            with gr.Column():
                iface = gr.Interface(
                fn = plot_function,
                inputs = [],
                outputs = gr.Image(type="pil"),
                live=True
                )
    conn = gr.Textbox(value="Connected to " + databasename.value,
                          interactive=False,
                          show_label=False,
                          visible=False,
                          elem_classes=["bold-italic-text"],
                          );
            
    button.click(get_db_openaikey,[database,openaikey,databasename],[database,openaikey,databasename,button,row_,conn])


    # New Code
    # with gr.Column(visible=False) as chat_col:
    #     conn = gr.Textbox(value="Connected to " + databasename.value,
    #                       interactive=False,
    #                       show_label=False);
    #     chat = gr.ChatInterface(predict);
    #     #New code
    #     iface = gr.Interface(
    #         fn = plot_function,
    #         inputs = [],
    #         outputs = gr.Image(type="pil"),
    #         live=True
    #     )
    #     #New code
    #     # chat = gr.ChatInterface(predict,outputs=["text","image"]);
    # button.click(get_db_openaikey,[database,openaikey,databasename],[database,openaikey,databasename,button,chat_col,conn])
demo.launch(server_name="0.0.0.0",server_port=7860)