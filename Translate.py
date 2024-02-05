import requests
import json
from gtts import gTTS


class ServerException(Exception):
    def __init__(self):
        self.message = 'Service Offline'
        super().__init__(self.message)


class Translate:
    def __init__(self):
        self.language_code = None
        self.target_language = None
        self.base_string = None

    def translate(self, base_string):
        self.base_string = base_string
        self.language_code = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy',
                              'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn',
                              'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'croatian': 'hr', 'czech': 'cs',
                              'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et',
                              'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'galician': 'gl', 'georgian': 'ka',
                              'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'hebrew': 'he', 'hindi': 'hi',
                              'hungarian': 'hu', 'icelandic': 'is', 'indonesian': 'id', 'irish': 'ga',
                              'italian': 'it', 'japanese': 'ja', 'javanese': 'jv', 'kannada': 'kn', 'kazakh': 'kk',
                              'korean': 'ko', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'macedonian': 'mk',
                              'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'marathi': 'mr', 'mongolian': 'mn',
                              'nepali': 'ne', 'norwegian': 'no', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt',
                              'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'serbian': 'sr', 'sinhalese': 'si',
                              'slovak': 'sk', 'slovenian': 'sl', 'spanish': 'es', 'swahili': 'sw', 'swedish': 'sv',
                              'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk',
                              'urdu': 'ur', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh',
                              'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}

        target_language_code = self.language_code[self.target_language.lower()]
        request_url = 'https://deep-translator-api.azurewebsites.net/'
        translators = ['google/', 'mymemory/', 'libre/']
        json_data = {
            "source": "en",
            "target": target_language_code,
            "text": self.base_string
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(request_url + translators[0], data=json.dumps(json_data), headers=headers)
            if response.status_code != 200:
                response = requests.post(request_url + translators[1], data=json.dumps(json_data), headers=headers)
                if response.status_code != 200:
                    response = requests.post(request_url + translators[2], data=json.dumps(json_data), headers=headers)
                    if response.status_code != 200:
                        raise ServerException
        except ServerException:
            return 'Server Offline'
        data = json.loads(response.text)
        audio = gTTS(text=data['translation'], lang=target_language_code)
        audio.save('translated_audio.mp3')
        return data['translation']