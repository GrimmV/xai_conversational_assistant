from openai import OpenAI
import json
from Bot import Bot
from category_information import category_information

categories = {
    "Model": {
        "description": "Information all around the model, like performance and feature importance",
        "available_data": [
            f"{key}: {value['description']}" for key, value in category_information["Model"].items()
        ]
    },
    "Data": {
        "description": "Information around the underlying data, like distributions, correlations and descriptions",
        "available_data": [
            f"{key}: {value['description']}" for key, value in category_information["Data"].items()
        ]
    },
    "Prediction": {
        "description": "Information about the individual prediction that is analyzed such as prediction, prediction probabilities and trustscore",
        "available_data": [
            f"{key}: {value['description']}" for key, value in category_information["Prediction"].items()
        ]
    },
    "Context": {
        "description": "Information about the context of the model prediction, i.e., how the model behaves around the datapoint.",
        "available_data": [
            f"{key}: {value['description']}" for key, value in category_information["Context"].items()
        ]
    },
    "General": {
        "description": "General Information about explainable AI and machine learning."
    },
}

class GuidanceBot(Bot):

    def __init__(self) -> None:

        self.llm = OpenAI()
        self.model = "gpt-4o-2024-05-13"

        
        self.intro = f"""You are a virtual assistant and help an expert to analyze a machine learning model with every request as good as you can. \
                The ML model is specialized in answering questions about the quality of wine based \
                on given chemical properties. \
                
                You are specialized helping to guide the user by providing suggestions for next steps. \
                
                There are the following thematic categories for the user and the available data to answer user requests: \

                {categories}
        """

        self.output_definition = """\n \
                Provide an answer in JSON format: \
        
                {
                    response: string
                    explanation: string # Why did you choose to respond in this way?
                }
        """

        self.full_prompt = self.intro + self.output_definition
    
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