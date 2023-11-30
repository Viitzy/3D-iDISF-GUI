import PySimpleGUI as sg
from PIL import Image, ImageTk
import io

# Função para converter imagem para exibição
def convert_to_bytes(file_or_bytes, resize=None):
    if isinstance(file_or_bytes, str):
        img = Image.open(file_or_bytes)
    else:
        try:
            img = Image.open(io.BytesIO(file_or_bytes))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_width/cur_width, new_height/cur_height)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

# Função para atualizar a imagem exibida
def update_displayed_image(image_list):
    if image_list:
        filename = image_list[0]
        window["-TOUT-"].update(filename)
        window["-IMAGE-"].update(data=convert_to_bytes(filename, resize=(400, 400)))
    else:
        window["-TOUT-"].update("")
        window["-IMAGE-"].update(data=None)

# Função para visualizar todas as imagens
def view_all_images(image_files):
    images_in_bytes = [convert_to_bytes(img, resize=(200, 200)) for img in image_files]
    image_elements = [[sg.Image(data=image_data)] for image_data in images_in_bytes]
    
    layout = [
        [sg.Column(image_elements, scrollable=True, vertical_scroll_only=True, size=(220, 600))],
        [sg.Button("Close")]
    ]
    
    window = sg.Window("View All Images", layout, modal=True, resizable=True)
    while True:
        event, _ = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break
    window.close()

# Layout principal
file_list_column = [
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
    [sg.Button("Add Image"), sg.Button("Remove Image"), sg.Button("View All")],
]

image_viewer_column = [
    [sg.Text("Choose an image from list above:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer + Editor", layout)

image_files = []
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FILE LIST-":
        try:
            filename = values["-FILE LIST-"][0]
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(data=convert_to_bytes(filename, resize=(400, 400)))
        except:
            pass
    elif event == "Add Image":
        filenames = sg.popup_get_file("Choose an image file", multiple_files=True, file_types=(("Image Files", "*.png;*.jpg;*.jpeg;*.gif"),))
        if filenames:
            for file in filenames.split(";"):
                image_files.append(file)
            window["-FILE LIST-"].update(image_files)
            update_displayed_image(image_files)
    elif event == "Remove Image":
        if values["-FILE LIST-"]:
            image_files.remove(values["-FILE LIST-"][0])
            window["-FILE LIST-"].update(image_files)
            update_displayed_image(image_files)
    elif event == "View All":
        view_all_images(image_files)

window.close()
