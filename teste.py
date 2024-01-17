import PySimpleGUI as sg
import io, os
from PIL import Image

file_types = [
    ("JPEG (*.jpg)", "*.jpg"),
    ("All files (*.*)", "*.*")
]

layout = [
    [sg.Image(key="-IMAGE-", size=(400, 400))],
    [sg.Text("Image files"), sg.Input(key="-FILES-", enable_events=True, visible=False), sg.FilesBrowse(file_types=file_types), sg.Button("Load Images")],
    [sg.Button("Previous"), sg.Button("Next"), sg.Button("Remove Image"), sg.Button("Show All Images")],
    [sg.Text("", key="-IMAGE_COUNT-", visible=False)]
]

window = sg.Window("Image Viewer ", layout)

image_list = []
current_image_index = 0
show_all_images = False

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Load Images":
        filenames = values["-FILES-"].split(';')
        for filename in filenames:
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                image_list.append((filename, bio.getvalue()))
        window["-IMAGE-"].update(data=image_list[0][1] if image_list else None)
        window["-IMAGE_COUNT-"].update(f"Image {current_image_index + 1} of {len(image_list)}", visible=bool(image_list))
    if event == "Previous":
        current_image_index = (current_image_index - 1) % len(image_list)
        window["-IMAGE-"].update(data=image_list[current_image_index][1])
        window["-IMAGE_COUNT-"].update(f"Image {current_image_index + 1} of {len(image_list)}")
    if event == "Next":
        current_image_index = (current_image_index + 1) % len(image_list)
        window["-IMAGE-"].update(data=image_list[current_image_index][1])
        window["-IMAGE_COUNT-"].update(f"Image {current_image_index + 1} of {len(image_list)}")
    if event == "Remove Image":
        if image_list:
            del image_list[current_image_index]
            if not image_list:
                window["-IMAGE-"].update(data=None)
                window["-IMAGE_COUNT-"].update(visible=False)
            else:
                current_image_index = min(current_image_index, len(image_list) - 1)
                window["-IMAGE-"].update(data=image_list[current_image_index][1])
                window["-IMAGE_COUNT-"].update(f"Image {current_image_index + 1} of {len(image_list)}")
    if event == "Show All Images":
        if image_list:
            show_all_images = True

    if show_all_images:
        sg.popup('All Images', image=image_list, no_titlebar=True, auto_close=True, auto_close_duration=3)

window.close()
