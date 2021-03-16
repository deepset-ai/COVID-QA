# Detector_Data.py functions to process the data to hide data processing
# from the user, and returning of data is done by detect_detect_language.py

import sys
import os
import pycld2 as cld2
import hmac
from hashlib import sha1
from time import time
import requests

class Detector_Data:
    my_text = "Was ist das Coronavirus?"
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