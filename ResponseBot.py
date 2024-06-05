from openai import OpenAI
import json


class ResponseBot:

    def __init__(self) -> None:

        self.llm = OpenAI()
        self.model = "gpt-4o-2024-05-13"

        self.intro = """You are a virtual assistant and help an expert to analyze a machine learning model with every request as good as you can. \
                The ML model is specialized in answering questions about the quality of wine based on given chemical properties. \
                
                You are specialized in answering questions concerning the ML model. \
                
                This is the data you have at hand to respond to the request: \
        """

        self.output_definition = """\n \
                Provide an answer in JSON format with the following structure: \
        
                {
                    "response": string # this is a text response to the user request,
                    "explanation": string # explain why you responded this way,
                    "next": string # make a recommendation for the next step
                }

                Provide a meaningful response to the end user that is specific and comprehensible

                This is the user request: \
        """

    def construct_prompt(self, data):

        return self.intro + json.dumps(data) + self.output_definition
    
    def handle_request(self, request="How does the model perform?", data=[]):

        response = self.llm.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.construct_prompt(data)},
                {"role": "user", "content": request},
            ],
        )

        output = response.choices[0].message.content

        return json.loads(output)