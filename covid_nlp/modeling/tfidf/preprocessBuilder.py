from preprocess import Preprocessor

class preprocessBuilder():
    def __init__(self):
        self.language = None
    
    @staticmethod
    def item():
        return preprocessBuilder()

    def withLanguage(self, language):
        self.language = language
        return self

    def build(self):
        return Preprocessor(self.language)

def main():
    Preprocessor = preprocessBuilder.item().withLanguage("English").build()
if __name__ == "__main__":
    main()