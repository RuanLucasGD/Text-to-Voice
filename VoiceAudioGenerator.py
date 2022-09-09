from ibm_watson import TextToSpeechV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import AppConfig as config

from os import listdir
from os.path import isfile, join

AUDIO_PATH = "./exports/"
AUDIO_NAME_BASE = "audio "


# gera um arquivo de audio com um tempo e uma voz escolhida
# o audio deve ser uma das opções fornecidas do IBM Text to Speech
def write_audio_file_from_text(text, voice, on_completed=None, on_fail=None):
    def connect_to_api_service():

        service_text_to_speech : TextToSpeechV1

        auth = IAMAuthenticator(config.config['api'])
        service_text_to_speech = TextToSpeechV1(authenticator=auth)
        service_text_to_speech.set_service_url(config.config['url'])
        return  service_text_to_speech

    def file_name():
        name = AUDIO_PATH+AUDIO_NAME_BASE

        import os

        # folder path
        dir_path = AUDIO_PATH

        if os.path.isdir(dir_path) == False:
            os.makedirs(dir_path)

        # list to store files
        res = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        name+= str(len(res))

        return name

    text_to_speech = connect_to_api_service()

    try:
        try:
            audio_data = text_to_speech.synthesize(text=text, voice=voice, accept='audio/mp3')

            if audio_data is not None:
                f_name = file_name()
                with open(f_name + ".mp3", 'wb') as file:
                    file.write(audio_data.get_result().content)
                if on_completed is not None:
                    on_completed()

        except ApiException as e:
            if on_fail is not None:
                on_fail(e.code, e.message)
                return
    except Exception as e:
        if on_fail is not None:
            on_fail(11001, "Connection Error, check your internet.")
            return

