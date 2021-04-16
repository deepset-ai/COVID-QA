# -*- coding: utf-8 -*-
import os, requests, uuid, json
import sys

import pandas as pd

import json
from typing import Dict


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
        t__(self, shared_state: str) -> None:
        self._shared_state = shared_state

    def operation(self, unique_state: str) -> None:
        s = json.dumps(self._shared_state)
        u = json.dumps(unique_state)


class MSTranslatorFactory():


    _MSTranslators: Dict[str, MSTranslator] = {}

    def __init__(self, initial_MSTranslators: Dict) -> None:
        for state in initial_MSTranslators:
            self._MSTranslators[self.get_key(state)] = MSTranslator(state)

    def get_key(self, state: Dict) -> str:


        return "_".join(sorted(state))

    def get_MSTranslator(self, shared_state: Dict) -> MSTranslator:

        key = self.get_key(shared_state)

        if not self._MSTranslators.get(key):
            print("MSTranslatorFactory: Can't find a MSTranslator, creating new one.")
            self._MSTranslators[key] = MSTranslator(shared_state)
        else:
            print("MSTranslatorFactory: Reusing existing MSTranslator.")

        return self._MSTranslators[key]

    def list_MSTranslators(self) -> None:
        count = len(self._MSTranslators)


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
