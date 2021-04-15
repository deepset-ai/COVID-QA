import sys
import os
import pycld2 as cld2
import hmac
from hashlib import sha1
from time import time
import requests
from abc import ABCMeta, abstractmethod

# apply bridge pattern
# print method is commonly used by the three class

# abstract class
class Bridge:
    def __init__(self, model):
        self.model = model
    def bridge_print(self):
        pass

# concrete abstract class
class Bridge_cld2(Bridge):
    def __init__(self, model):
        self.model = model

class Bridge_cld3(Bridge):
    def __init__(self, model):
        self.model = model

class Bridge_cil(Bridge):
    def __init__(self, model):
        self.model = model


# Implementation class
class DlPrint:
    def Dl_print(self, text):
        pass

# concrete implementation class
class DlPrint_Detect_lang_cld2(DlPrint):
        
    def Dl_print(self, text):
        pred = cld2.detect(text)[2][0]
        print(f"cld2: {pred[1], float(pred[2])}")


class DlPrint_Detect_lang_cld3(DlPrint):
        
    def Dl_print(self, text, n = 3):
        # print ld3_detect_result
        import cld3  # requires protobuf
        pred = cld3.get_language(text)
        print(f"cld3: {pred.language, 100*pred.probability}")

        # print ld3_freq_top_results
        pred = cld3.get_frequent_languages(text, num_langs = n)
        pred_list = [ (p.language, 100*p.probability) for p in pred ]
        print(f"cld3-freq: {pred_list}")


class DlPrint_Detect_lang_sil(DlPrint):

    def Dl_print(self, text):
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
        pred_sil = r.json()[0]['language'], 100*r.json()[0]['probability']
        print(f"sil: {pred_sil}")


def main():
    my_text = "Was ist das Coronavirus?"
    ld3 = Bridge_cld3('ld3')
    ld3_p = DlPrint_Detect_lang_cld3(text = my_text)
    ld3_p.Dl_print

    ld2 = Bridge_cld2('ld2')
    ld2_p = DlPrint_Detect_lang_cld2(text = my_text)
    ld2_p.Dl_print

    ldsil = Bridge_cil('sil')
    ldsil_p = DlPrint_Detect_lang_sil(text = my_text)
    ldsil_p.Dl_print

if __name__ == "__main__":
    main()
