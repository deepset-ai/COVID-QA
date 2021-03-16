import sys
import os
import pycld2 as cld2
import hmac
from hashlib import sha1
from time import time
import requests

#
# class to detect what language users query is in
#
class LanguageDetector():
    def __init__(self, model = 'sil'):
        self.model = model

    def detect_lang_cld2(self, text):
        pred = cld2.detect(text)[2][0]
        return pred[1], float(pred[2])

    def detect_lang_cld3(self, text):
        import cld3  # requires protobuf
        pred = cld3.get_language(text)
        return pred.language, 100*pred.probability

    def detect_lang_sil(self, text):
        algorithm = 'HMAC+SHA1'
        curr_time = str(int(time()))
        concat = curr_time+os.environ.get('SIL_API_KEY')
        concatB = (concat).encode('utf-8')
        secretB = os.environ.get('SIL_API_SECRET').encode('utf-8')
        h1 = hmac.new(secretB, concatB, sha1)
        api_sig = h1.hexdigest()
        params = {'api_key': os.environ.get('SIL_API_KEY'), 'api_sig': api_sig}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(os.environ.get('SIL_API_URL'), json=[{"text": text}],
                headers=headers, params=params)
        return r.json()[0]['language'], 100*r.json()[0]['probability']

    def detect_lang(self, text):
        if self.model == 'cld2':
            return self.detect_lang_cld2(text)
        if self.model == 'cld3':
            return self.detect_lang_cld3(text)
        if self.model == 'sil':
            return self.detect_lang_sil(text)

    def detect_freq_lang(self, text, n = 3):
        import cld3  # requires protobuf
        pred = cld3.get_frequent_languages(text, num_langs = n)
        pred_list = [ (p.language, 100*p.probability) for p in pred ]
        return pred_list


def main():
    my_text = "Was ist das Coronavirus?"

    ld3 = LanguageDetector(model = 'cld3')
    ld3_result = ld3.detect_lang(my_text)
    print(f"cld3: {ld3_result}")
    ld3_top_results = ld3.detect_freq_lang(my_text, 4)
    print(f"cld3-freq: {ld3_top_results}")

    ld2 = LanguageDetector(model = 'cld2')
    ld2_result = ld2.detect_lang(my_text)
    print(f"cld2: {ld2_result}")

    ldsil = LanguageDetector(model = 'sil')
    ldsil_result = ldsil.detect_lang(my_text)
    print(f"sil: {ldsil_result}")

if __name__ == "__main__":
    main()



#
#language translator to translate users query to search with other similar queries
#

class MSTranslator():
    def __init__(self, key = None, endpoint = None, lang = None):
        if key:
            self.azure_key = key
        else:
            self.azure_key = os.environ['AZURE_TRANSLATE_KEY']
        self.azure_endpoint = endpoint
        self.lang = lang
        self.url = f"{self.azure_endpoint}/translate?api-version=3.0&to={self.lang}"
        self.headers =  {
                'Ocp-Apim-Subscription-Key': self.azure_key,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
        }

    def translate(self, text):
        body = [{'text': text.strip()}]
        request = requests.post(self.url, headers = self.headers, json = body)
        response = request.json()
        trans_text = ""
        if len(response) > 0:
            trans_text = response[0]['translations'][0]['text']
        return trans_text


def main():
    lang = "ar"
    azure_endpoint = "https://api.cognitive.microsofttranslator.com/"
    ms_translator = MSTranslator(endpoint = azure_endpoint, lang = lang)

    faq_file = "../../data/faqs/faq_covidbert.csv"
    df = pd.read_csv(faq_file)
    df[f'question_{lang}'] = df.apply(lambda x: ms_translator.translate(x.question), axis=1)
    df[f'answer_{lang}'] = df.apply(lambda x: ms_translator.translate(x.answer), axis=1)

    faq_filename = os.path.basename(faq_file)
    df.to_csv(f"MT_{lang}_{faq_filename}")

if __name__ == "__main__":
    main()
