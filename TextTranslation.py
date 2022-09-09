from googletrans import Translator 

def translate_text(text, from_lang='auto', to_lang='en', on_fail=None):

    try:
        if (text == ""): return ""
        translator = Translator()
        translated_text =translator.translate(text=text, dest=to_lang, src=from_lang).text
        return translated_text
    except Exception as e:
        if on_fail is not None:
            on_fail(e)
    return ""