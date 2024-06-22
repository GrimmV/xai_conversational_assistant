from openai import OpenAI
import json
from Bot import Bot


class ResponseBot(Bot):

    def __init__(self) -> None:

        self.llm = OpenAI()
        self.model = "gpt-4o-2024-05-13"

        self.intro = """You are a virtual assistant and help an expert to analyze a machine learning model with every request as good as you can. \
                The ML model is specialized in answering questions about the quality  of wine based on given chemical properties. \
                The user was presented with a specific datapoint and its model prediction. They are supposed to assess the trustworthiness of the model prediction. \
                
                You are specialized in answering questions concerning the ML model. \
                
                This is the data you have at hand to respond to the request: \
        """

        self.output_definition = """\n \
                Provide an answer in JSON format with the following structure: \
        
                {
                    "response": string # this is a text response to the user request,
                    "explanation": string # explain why you responded this way,
                }

                Provide a meaningful response to the end user that is specific and comprehensible.
        """

    def construct_prompt(self, data):

        return self.intro + json.dumps(data) + self.output_definition

    def handle_request(
        self, request="How does the model perform?", data=[], history=[]
    ):
        messages = [
            {"role": "system", "content": self.construct_prompt(data)},
            {"role": "system", "content": self.get_history(history)},
            {"role": "user", "content": request},
        ]

        response = self.llm.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=messages,
        )

        output = response.choices[0].message.content
        print(messages)

        return json.loads(output)
