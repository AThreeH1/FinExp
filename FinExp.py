import gradio as gr
import os
from gradio import components

descpr = "Experiment Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

def select_image(folder):
    image_files = os.listdir(folder)
    image_path = os.path.join(folder, image_files[0])
    return image_path

def image_selector(option):
    folder_mapping = {
        "A": r"C:\Study\Finance\IIMV Intern\Experiment Images\A",
        "B": r"C:\Study\Finance\IIMV Intern\Experiment Images\B",
        "C": r"C:\Study\Finance\IIMV Intern\Experiment Images\C",
        "D": r"C:\Study\Finance\IIMV Intern\Experiment Images\D"
    }
    folder_path = folder_mapping[option]
    image_path = select_image(folder_path)
    return image_path

dropdown = gr.inputs.Dropdown(["A", "B", "C", "D"], label="Select an option")
output = components.Image()

iface = gr.Interface(
    fn=image_selector,
    inputs=dropdown,
    outputs=output,
    title="Image Selector",
    description=descpr,
    layout="vertical",
)
iface.launch()
















