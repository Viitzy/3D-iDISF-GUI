import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import subprocess

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
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.Resampling.LANCZOS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

# Layout principal
file_list_column = [
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
    [sg.Button("Add Image"), sg.Button("Remove Image"), sg.Button("Open in iDISF")],
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
    elif event == "Remove Image":
        try:
            selected_file = values["-FILE LIST-"][0]
            image_files.remove(selected_file)
            window["-FILE LIST-"].update(image_files)
        except:
            pass
    # elif event == "View All":
    #     view_all_images(image_files)
    elif event == "Open in iDISF":
        # Aqui será adicionada a lógica para abrir o iDISF com a imagem selecionada
        selected_image = values["-FILE LIST-"][0]
        # Precisamos agora modificar o iDISF.py para aceitar esta imagem como entrada
        # Esta parte será implementada posteriormente
        subprocess.Popen(['python', 'iDISF.py', selected_image]) # Substitua 'caminho_para_iDISF.py' pelo caminho correto
        pass

window.close()
