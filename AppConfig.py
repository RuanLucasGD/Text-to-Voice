import json
import os.path

import PySimpleGUI as gui

config = {'api': '', 'url': '', 'theme':''}

themes = [
    ["DarkGrey 13"],
    ["Black"],
    ["BlueMono"],
    ["BrownBlue"],
    ["DarkBlue"],
    ["DarkBlue2"],
    ["DarkGreen6"],
    ["DarkGrey10"],
    ["DarkGrey8"],
    ["DarkGrey5"],
    ["DarkGrey15"],
    ["Default1"],
    ["GrayGrayGray"],
    ["GreenMono"],
    ["LightGrey"],
    ["LightGrey1"]
]

def config_window(on_close=None):
    load_config()

    __SAVE = "-SAVE-"
    __CANCEL = "-CANCEL-"
    __THEME_SELECTOR = "-THEME-"

    __API = "-API-"
    __URL = "-URL"

    layout = [
        [gui.Text("URL Connection Instance IBM", expand_x=True)],
        [gui.InputText(expand_x=True, default_text=config['url'], key=__URL)],
        [gui.Text("API Key Text to Speech", expand_x=True)],
        [gui.InputText(expand_x=True, default_text=config['api'], key=__API)],
        [gui.Text("Editor Theme", expand_x=True)],
        [gui.Combo(themes, default_value=config['theme'], key=__THEME_SELECTOR)],
        [gui.Column([[gui.Button("Cancel", key=__CANCEL), gui.Button("Save", key=__SAVE)]], expand_x=True,
                    expand_y=True)]
    ]

    window = gui.Window("Configs", layout=layout, size=(800, 600), resizable=True)
    event, values = window.read()

    if event == __SAVE:
        __api_key = window[__API].get()
        __url_connection = window[__URL].get()


        config['url'] = __url_connection.replace(" ", "")
        config['api'] = __api_key.replace(" ", "")

        selected_theme = window[__THEME_SELECTOR].get()
        print(config['theme'])
        if selected_theme != config['theme']:
            config['theme'] = selected_theme
            gui.popup("Restart the program to update theme")

        save_config()

    if event == __CANCEL:
        pass

    if on_close is not None:
        on_close()

    window.close()
    pass

def load_config():
    if os.path.isfile('config.json'):
        global config
        file = open('config.json')
        config = json.load(file)

    else:
        config['theme'] = themes[0][0]

def save_config():
    with open('config.json', 'w+') as file:
        json.dump(config, file, ensure_ascii=False)