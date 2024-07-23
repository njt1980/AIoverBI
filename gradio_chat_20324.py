import gradio as gr
from main_prog_chat import predict

# def predict(message,history):
#     buffer_list = []
#     print("input",message)
#     print(message + "result")
#     print("history",history)
#     if len(history) > 0:
#         # print(history[0][0])
#         # print(history[0][1])
#         for item in history:
#             buffer_list.extend([item[0],item[1]])
#     print("buffer_list:",buffer_list)
#     return message + "result"

# with gr.Blocks() as demo:
    # gr.Image(value=r"C:\Users\nimel.thomas\Desktop\GenAI-POC\PicassoHumanSQL.png")
    # gr.Image('<img src=r"C:\\Users\\nimel.thomas\\Desktop\\GenAI-POC\\PicassoHumanSQL.png">')
css1 = "body {background-image: url(r'./PicassoHumanSQL.png');}"
gr.ChatInterface(predict,
                 title="Talk to your data",
                 css=css1
                 ).launch()
    
# demo.launch()