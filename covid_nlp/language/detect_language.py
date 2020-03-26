import sys
import cld3 # requires protobuf
import pycld2 as cld2

class LanguageDetector():
    def __init__(self, version = 2):
        self.version = version

    def detect_lang_cld2(self, text):
        pred = cld2.detect(text)[2][0]
        return pred[1], float(pred[2])

    def detect_lang_cld3(self, text):
        pred = cld3.get_language(text)
        return pred.language, 100*pred.probability

    def detect_lang(self, text):
        if self.version == 2:
            return self.detect_lang_cld2(text)
        if self.version == 3:
            return self.detect_lang_cld3(text)

    def detect_freq_lang(self, text, n = 3):
        pred = cld3.get_frequent_languages(text, num_langs = n)
        pred_list = [ (p.language, 100*p.probability) for p in pred ]
        return pred_list


def main():
    my_text = "Was ist das Coronavirus?"

    ld3 = LanguageDetector(version = 3)
    ld3_result = ld3.detect_lang(my_text)
    print(f"cld3: {ld3_result}")
    ld3_top_results = ld3.detect_freq_lang(my_text, 4)
    print(f"cld3-freq: {ld3_top_results}")

    ld2 = LanguageDetector(version = 2)
    ld2_result = ld2.detect_lang(my_text)
    print(f"cld2: {ld2_result}")

if __name__ == "__main__":
    main()
