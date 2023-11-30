import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import os

# Function to get an image as a byte array for PySimpleGUI
def get_img_data(f, maxsize=(200, 200)):
    img = Image.open(f)
    img.thumbnail(maxsize)
    with io.BytesIO() as output:
        img.save(output, format="PNG")
        data = output.getvalue()
    return data

# Function to create a window layout with a flexible image grid
def create_window():
    layout = [
        [sg.Text("Select Images: "), sg.Input(), sg.FilesBrowse(key="-FILES-"), sg.Button("Load Images")],
        [sg.Column([], key='-IMAGE-COLUMN-')]  # Placeholder for image elements
    ]
    return sg.Window("Image Viewer", layout, size=(800, 600))

# Create the window
window = create_window()

# Event loop
while True:
    event, values = window.read()

    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

    if event == "Load Images":
        filenames = values["-FILES-"].split(';')
        
        # Build new layout for images
        new_layout = []
        for idx, file_path in enumerate(filenames):
            if os.path.exists(file_path) and file_path.lower().endswith(('.png', '.jpg', 'jpeg')):
                new_layout.append([sg.Image(data=get_img_data(file_path), key=f"-IMAGE-{idx}-")])

        # Update the column with the new layout
        window['-IMAGE-COLUMN-'].update(new_layout)

# Close the window
window.close()
