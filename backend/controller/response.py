from pydantic import BaseModel



class LeafResponse(BaseModel):  
    # Class represents the leaf responses
    def __init__(self, *args):
          self.answers = []
          
    def getAnswers(self):
        return self.answers
    
class CompositeResponse(BaseModel):
    #  Class representing objects at any level of the hierarchy tree except for the bottom or leaf level  
        def __init__(self, *args):
            self.answers = []
            self.children = []
            
        def add(self, child):
            # Adds the supplied child element to the list of children elements "children".
            self.children.append(child)
            
        def remove(self, child):
        # Removes the supplied child element from the list of children elements "children".
            self.children.remove(child)
            
            
        def getAnswers(self):
            # returns the answer to the current object and the answers to its children as well
            allAnswers = [self.answers]
            for child in self.children:
                allAnswers.append(child.getAnswers)
            return allAnswers