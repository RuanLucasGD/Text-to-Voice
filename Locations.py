class Location():
    name = "",
    google_translation_ref = "",
    ibm_voice_location = ""

    def __init__(self, name, google_translation_ref, ibm_voice_location):

        self.name = name,
        self.google_translation_ref = google_translation_ref,
        self.ibm_voice_location = ibm_voice_location

class Voice():
    name = "",
    ibm_voice_ref=""

    def __init__(self, name, ibm_voice_ref):
        self.name = name,
        self.ibm_voice_ref = ibm_voice_ref

locations = [
    Location(name= "English", 
            google_translation_ref= "en", 
            ibm_voice_location= [
                Voice(name="Charlotte", ibm_voice_ref="en-GB_CharlotteV3Voice"),
                Voice(name="James", ibm_voice_ref="en-GB_JamesV3Voice"),
                Voice(name="Kate", ibm_voice_ref="en-GB_KateV3Voice"),
                Voice(name="Allison", ibm_voice_ref="en-US_AllisonV3Voice"),
                Voice(name="Emily", ibm_voice_ref="en-US_EmilyV3Voice"),
                Voice(name="Henry", ibm_voice_ref="en-US_HenryV3Voice"),
                Voice(name="Kevin", ibm_voice_ref="en-US_KevinV3Voice"),
                Voice(name="Lisa", ibm_voice_ref="en-US_LisaV3Voice"),
                Voice(name="Michael", ibm_voice_ref="en-US_MichaelV3Voice")
            ]),

    Location(name= "Portuguese", 
            google_translation_ref= "pt", 
            ibm_voice_location=  [
                Voice(name="Isabela", ibm_voice_ref="pt-BR_IsabelaV3Voice")
            ]),

    Location(name= "Spainsh", 
            google_translation_ref=  "es", 
            ibm_voice_location=  [
                Voice(name="Enrique", ibm_voice_ref="es-ES_EnriqueV3Voice"),
                Voice(name="laura", ibm_voice_ref="es-ES_LauraV3Voice"),
                Voice(name="Sofia", ibm_voice_ref="es-LA_SofiaV3Voice"),
    ]),
]

def get_language_by_name(name):
    for l in locations:
        if l.name[0] == name:
            return l

    return None

def get_all_locations_names():
    names = []
    for l in locations: names.append(l.name)
    return names

def get_all_voices_name_by_language_name(language):

    voices_names = []

    for l in locations:
        if l.name[0] == language:
            for v in l.ibm_voice_location:
                voices_names.append(v.name)

    return voices_names

def get_ibm_voice_by_voice_name(voice_name):

    for l in locations:
        for v in l.ibm_voice_location:
            if v.name[0] == voice_name:
                return v.ibm_voice_ref
    
    return ""