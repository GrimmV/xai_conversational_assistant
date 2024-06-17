import json

class Bot:
    
    def get_history(self, history):

        return "This is the conversation history so far: " + json.dumps(history)