# -*- coding: utf-8 -*-
import os, requests, uuid, json
import sys
from typing import List
import pandas as pd
from observer import Observer, ConcreteObserver

class MSTranslator():

    # concrete subject
    _observers: List[Observer] = []

    # The subscription management methods.
    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    # concrete notify when event 
    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)


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
            self.notify()
        return trans_text


def main():
    lang = "ar"
    azure_endpoint = "https://api.cognitive.microsofttranslator.com/"
    ms_translator = MSTranslator(endpoint = azure_endpoint, lang = lang)

    concreteObs_a = ConcreteObserver()
    ms_translator.attach(concreteObs_a)

    faq_file = "../../data/faqs/faq_covidbert.csv"
    df = pd.read_csv(faq_file)
    df[f'question_{lang}'] = df.apply(lambda x: ms_translator.translate(x.question), axis=1)
    df[f'answer_{lang}'] = df.apply(lambda x: ms_translator.translate(x.answer), axis=1)

    faq_filename = os.path.basename(faq_file)
    df.to_csv(f"MT_{lang}_{faq_filename}")

if __name__ == "__main__":
    main()
