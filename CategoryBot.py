from openai import OpenAI
import json
from category_information import category_information
from Bot import Bot

feature_list = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol']

class CategoryBot(Bot):

    def __init__(self, category: str) -> None:

        self.llm = OpenAI()
        self.model = "gpt-4o-2024-05-13"

        if category == "Model":
            specialization = "ML model"
        elif category == "Data":
            specialization = "underlying data"
        elif category == "Prediction":
            specialization = "individual model prediction"
        elif category == "Context":
            specialization = "context of the model prediction"
        categorized_information = category_information[category]
        
        self.intro = f"""You are a virtual assistant and help an expert to analyze a machine learning model with every request as good as you can. \
                The ML model is specialized in answering questions about the quality of wine based on given chemical properties. \
                The user was presented with a specific datapoint and its model prediction. They are supposed to assess the trustworthiness of the model prediction. \
                
                The dataset contains the following features: \
                {feature_list}

                The labels are quality scores between 1 and 10. Due to limitations of the data, the labels contain only scores between 3 and 8.
                
                You are specialized in answering questions concerning the {specialization}. \
                
                The following dictionary describes the available data to answer the request: \
                
                {categorized_information}
        """

        self.output_definition = """\n \
                Provide an answer in JSON format containing the key-value pairs based on the keys from the dictionary above and your parameter choice: \
        
                {
                    response: {
                            <information_key>: { \
                                <parameter_type>: <parameter>, \
                                ...
                        }, # e.g. 'Confusion Matrix': {'kind': 'test'}\
                        ...
                    }
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