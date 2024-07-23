
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from langchain_core.tools import tool
import main_prog_chat
import traceback

@tool
def function_to_generate_graph(xcoordinates,ycoordinates,graphtype,title,xaxis,yaxis):
    """
    Call this tool to generate any of the following types of plots, line, histogram, bar, scatter.

    Args:
        xcoordinates : List of values corresponding to the x-coordinates. 
        ycoordinates : List of values corresponding to the y-coordinates.
        graphtype : type of graph("line","histogram","bar","scatter")
        title : String describing the plot
        xaxis : String describing the data on the x axis
        yaxis : String describing the data on the y axis

    Returns:
        String confirming that graph has been generated
    """
    print("In plotting tool..")
    try:
        x = xcoordinates
        y = ycoordinates
        # Create the plot
        plt.figure()
        plt.rc('font', family='serif', size=8)
        plt.figure(figsize=(10, 9))
        if graphtype == "line":
            plt.plot(x, y, marker='o')
        elif graphtype == "histogram":
            plt.hist(x,y)
        elif graphtype == "bar":
            plt.bar(x,y)
        elif graphtype == "scatter":
            plt.scatter(x,y)
        else:
            return "Plot not in scope."
        plt.title(title,fontsize=10)
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)
        plt.legend()
        # Save the plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = Image.open(buf)
        print("Before :", main_prog_chat.image_placeholder)
        print("buf type :", type(buf))
        print("IMAGE type :", type(img))
        main_prog_chat.image_placeholder = img
        print("After :", main_prog_chat.image_placeholder)
        return "Plot generated."
    except Exception as e:
        error_message = f"An error occurred while generating the plot: {str(e)}"
        traceback.print_exc()  # Print the full traceback for debugging purposes
        return error_message
    # pass

