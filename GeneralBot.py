from openai import OpenAI
import json
from Bot import Bot

class GeneralBot(Bot):

    def __init__(self) -> None:

        self.llm = OpenAI()
        self.model = "gpt-4o-2024-05-13"

        
        self.intro = """You are a virtual assistant and help an expert to analyze a machine learning model with every request as good as you can. \
                The ML model is specialized in answering questions about the quality of wine based \
                on given chemical properties. \
                
                You are specialized in answering general questions with respect to machine learning and explainable AI. \
        """

        self.output_definition = """\n \
                Provide an answer in JSON format: \
        
                {
                    response: string 
                    explanation: string # Why did you choose to respond in this way?
                }

                This is the user request: \
        """

        self.full_prompt = self.intro + self.output_definition

    def construct_prompt(self, request):

        return self.intro + request + self.output_definition
    
    def handle_request(self, request="How does the model perform?", history=[]):

        response = self.llm.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.full_prompt},
                {"role": "system", "content": self.get_history(history)},
                {"role": "user", "content": request},
            ],
        )

        output = response.choices[0].message.content

        return json.loads(output)