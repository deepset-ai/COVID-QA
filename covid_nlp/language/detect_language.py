import sys
import os
import pycld2 as cld2
import hmac
from hashlib import sha1
from time import time
import requests

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
