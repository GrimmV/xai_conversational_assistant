from openai import OpenAI
import json

categories = {
    "General": "Answering general questions about machine learning and explainable AI that are independent of the data and model",
    "Model": "Answering questions about the model",
    "Data": "Answering questions about the data"
}

class CategoryRoutingBot:

    def __init__(self) -> None:

        self.llm = OpenAI()
        self.model = "gpt-4o-2024-05-13"

        
        self.intro = f"""You are a virtual assistant and help an expert to analyze a machine learning model with every request as good as you can. \
                The ML model is specialized in answering questions about the quality of wine based \
                on given chemical properties. Categorize the request of the user into one of the following categories to navigate to a specialized assistant for the category:\
                
                {categories} \
                
        """

        self.output_definition = """\n \
                Provide an answer in JSON format containing a single entry with the category (single word) as value like this: \
        
                {
                    "category": string # chosen category ,
                    "explanation: string # why did you choose this category?
                }

                This is the user request: \
        """

        self.full_prompt = self.intro + self.output_definition

    def construct_prompt(self, request):

        return self.intro + request + self.output_definition
    
    def handle_request(self, request="How does the model perform?"):

        response = self.llm.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.full_prompt},
                {"role": "user", "content": request},
            ],
        )

        output = response.choices[0].message.content

        return json.loads(output)