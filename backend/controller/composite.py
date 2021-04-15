from pydantic import BaseModel
from backend import api
from typing import Optional
from fastapi import APIRouter, status

class Leaf:
    def __init__(self, *args)
        self.reply = args[0]

    def getReply(self):
        print(self.reply)

class Composite:

    def __init__(self)
        self.child = []

    def add(self, child):
        self.children.append(child)

    def remove(self,child)
        self.chilren.remove(child)

    def getReply(self):
        replies = [self.reply]

        for child in self.children:
            replies.append(child.getReply)
        print(replies)

