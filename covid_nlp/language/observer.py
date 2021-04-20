import csv
from abc import ABC, abstractclassmethod
from __future__ import annotations
import pandas as pd
from typing import List
from ms_translate import MSTranslator



class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """
    @abstractclassmethod
    def attach(self, observer: Observer) -> None:
        # attach new subscribers 
        pass

    @abstractclassmethod
    def detach(self, observer: Observer) -> None:
        # detach a subscriber
        pass

    @abstractclassmethod
    def notify(self) -> None:
        # notify the observers in the Observer list about the event
        pass

class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """
    @abstractclassmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass



"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""
class ConcreteObserver(Observer):
    def update(self, subjects: Subject) -> None:
        print("Translation has been done and recorded in faq_covidbert successfully!")