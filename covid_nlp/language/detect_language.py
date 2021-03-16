# detect_language.py functions to receive the processed data
# from Detector_Data and return the data to the user
# We apply aggregation by first passing object created by Detector_Data
# as a param/rootIdentity to LangugaeDetector().

import sys
import os
import pycld2 as cld2
import hmac
from hashlib import sha1
from time import time
import requests
from Detector_Data import Detector_Data

class LanguageDetector(object):
    def __init__(self, rootIdentity):
        # initialization of root entity of this aggregation
        try:
            self.data = rootIdentity
        except:
            raise Exception("Error connecting to source!")


    def detect_lang_cld2(self, text):
        return self.data.detect_lang_cld2(text)

    def detect_lang_cld3(self, text):
        return self.data.detect_lang_cld3(text)

    def detect_lang_sil(self, text):
        return self.data.detect_lang_sil(text)

    def detect_lang(self, text):
        return self.data.detect_lang(text)

    def detect_freq_lang(self, text, n = 3):
        return self.data.detect_freq_lang(text, n=3)

# I also aggregate the main() and change the calling of Detector_Data(),
# by first initialize rootIdentity and then pass it into LanguageDetector()

def main():
    my_text = "Was ist das Coronavirus?"

    rootIdentity1 = Detector_Data(model = 'cld3')
    ld3 = LanguageDetector(rootIdentity1)
    ld3_result = ld3.detect_lang(my_text)
    print(f"cld3: {ld3_result}")
    ld3_top_results = ld3.detect_freq_lang(my_text, 4)
    print(f"cld3-freq: {ld3_top_results}")

    rootIdentity2 = Detector_Data(model = 'cld2')
    ld2 = LanguageDetector(rootIdentity2)
    ld2_result = ld2.detect_lang(my_text)
    print(f"cld2: {ld2_result}")

    rootIdentity3 = Detector_Data(model = 'sil')
    ldsil = LanguageDetector(rootIdentity3)
    ldsil_result = ldsil.detect_lang(my_text)
    print(f"sil: {ldsil_result}")

if __name__ == "__main__":
    main()
