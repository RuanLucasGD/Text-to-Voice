from AppConfig import *
from Locations import *
from TextTranslation import *
from VoiceAudioGenerator import *

#gui.theme_previewer()

__OPEN_CONFIGURATION_WINDOW = "Configurations"
__ABOUT_WINDOW = "About"

__EVENT_TRANSLATE_USER_TEXT = "-TRANSLATE-"
__EVENT_GENERATE_AUDIO = "-GENERATE-VOICE-AUDIO-"

__FIELD_SOURCE_TEXT = "-USER-TEXT-"
__FIELD_TRANSLATED_TEXT = "-TRANSLATED-TEXT-"

__USER_TEXT_LANGUAGE_DROPDOWN = "-USER-LANGUAGE-"
__TRANSLATION_TEXT_LANGUAGE_SELECTOR = "-TRANSLATION-LANGUAGE-"
__EVENT_CHANGE_AUDIO_VOICE = "-VOICE-SELECTION"


# chamado quando o usuario traduz o texto
def on_translate_source_text():
    source_text = window[__FIELD_SOURCE_TEXT].get()
    current_language_name = window[__USER_TEXT_LANGUAGE_DROPDOWN].get()[0]
    target_language_name = window[__TRANSLATION_TEXT_LANGUAGE_SELECTOR].get()[0]

    current_text_language_ref = get_language_by_name(current_language_name).google_translation_ref[0]
    target_translation_ref = get_language_by_name(target_language_name).google_translation_ref[0]

    text_translated = translate_text(source_text, from_lang=current_text_language_ref, to_lang=target_translation_ref,
                                     on_fail=on_translate_text_error)

    window[__FIELD_TRANSLATED_TEXT].update(text_translated)


# chamado quando o usuario gera o audio de fala
def on_generate_voice_audio():
    text_translated = window[__FIELD_TRANSLATED_TEXT].get()
    voice_name = window[__EVENT_CHANGE_AUDIO_VOICE].get()[0]

    if text_translated == "":
        gui.popup("Error on create Audio", "Translated text field is empty, please add something to this field")

        return

    ibm_voice = get_ibm_voice_by_voice_name(voice_name)
    write_audio_file_from_text(text_translated, voice=ibm_voice, on_fail=on_generate_audio_voice_error,
                               on_completed=lambda: gui.popup("Success", "Export audio complete"))


def on_change_user_text(value):
    pass


def on_translate_text_error(error):
    gui.popup("Error on Translate Text", "Check if is connected with internet...")


def on_generate_audio_voice_error(error_code, error_message):
    if error_code == 400:
        gui.popup("Incorrect IBM Service API Key",
                  "Your API Key of Service Text to Speech is incorrect, check your configurations")

    if error_code == 403:
        gui.popup("Incorrect IBM Service URL",
                  "Your URL of IBM Service Text to Speech is incorrect, check configurations")

    else:
        gui.popup("Error", error_message + "\n error: " + str(error_code))


# chamado quando o usuario muda o idioma da tradução do texto
def on_change_text_translation_option():
    selected_language_name = window[__TRANSLATION_TEXT_LANGUAGE_SELECTOR].get()[0]
    language = get_language_by_name(selected_language_name)

    # atualiza a lista de vozes disponiveis para a linguagem selecionada
    voices = []
    for l in language.ibm_voice_location: voices.append(l.name)
    window[__EVENT_CHANGE_AUDIO_VOICE].update(value=voices[0][0], values=voices)
    pass


load_config()
gui.theme(config.config['theme'])

draw_menu_layout = gui.Menu([['&Options', [__OPEN_CONFIGURATION_WINDOW]], ['About', [__ABOUT_WINDOW]]], tearoff=False,
                            pad=(200, 1))

draw_user_text_field = gui.Column([
    [gui.Text('Source Text', expand_x=True)],
    [gui.Multiline(size=(80, 40), key=__FIELD_SOURCE_TEXT, expand_x=True)]
])

draw_translation_text_field = gui.Column([
    [gui.Text('Translated Text', expand_x=True)],
    [gui.Multiline(size=(80, 40), key=__FIELD_TRANSLATED_TEXT, expand_x=True)]
])

draw_audio_and_translation_field = gui.Column([
    [gui.Text('Source language', expand_x=True)],
    [gui.Combo(get_all_locations_names(), key=__USER_TEXT_LANGUAGE_DROPDOWN, enable_events=True,
               default_value=get_all_locations_names()[1])],
    [gui.Text('Translate To', expand_x=True)],
    [gui.Combo(get_all_locations_names(), key=__TRANSLATION_TEXT_LANGUAGE_SELECTOR, enable_events=True,
               default_value=get_all_locations_names()[0])],
    [gui.Button('Apply Translation', key=__EVENT_TRANSLATE_USER_TEXT, expand_x=True)],
    [gui.Text("Voice generation", expand_x=True)],
    [gui.Combo(get_all_voices_name_by_language_name(locations[0].name[0]), key=__EVENT_CHANGE_AUDIO_VOICE,
               enable_events=True, expand_x=True,
               default_value=get_all_voices_name_by_language_name(locations[0].name[0])[0])],
    [gui.Button("Generate Audio", expand_x=True, key=__EVENT_GENERATE_AUDIO)]])

layout = [[gui.Column([
    [
        draw_menu_layout,
        draw_user_text_field,
        draw_translation_text_field,
        draw_audio_and_translation_field
    ]
])]]

window = gui.Window('Text to Voice', layout=layout, size=(1400, 720), resizable=True)

while True:
    event, values = window.read()
    if event == __EVENT_TRANSLATE_USER_TEXT:
        on_translate_source_text()
    if event == __FIELD_SOURCE_TEXT:
        on_change_user_text(values[__FIELD_SOURCE_TEXT])
    if event == __EVENT_GENERATE_AUDIO:
        on_generate_voice_audio()

    if event == __TRANSLATION_TEXT_LANGUAGE_SELECTOR:
        on_change_text_translation_option()

    if event == __OPEN_CONFIGURATION_WINDOW:
        config_window()

    if event == __ABOUT_WINDOW:
        gui.popup("About",
                  "System for creating multi-language systemized audio \nDeveloper: Ruan Lucas \ncontact: ruanlucaspgbr@outlook.com")

    if event in (None, 'Exit'):
        break

    if event == 'Display':
        window['-OUTPUT-'].update(values['-IN-'])

window.close()
