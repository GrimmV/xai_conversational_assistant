from openai import OpenAI
import json
from category_information import category_information

class CategoryBot:

    def __init__(self, category: str) -> None:

        self.llm = OpenAI()
        self.model = "gpt-4o-2024-05-13"

        if category == "Model":
            specialization = "ML model"
        elif category == "Data":
            specialization = "underlying data"
        categorized_information = category_information[category]
        
        self.intro = f"""You are a virtual assistant and help an expert to analyze a machine learning model with every request as good as you can. \
                The ML model is specialized in answering questions about the quality of wine based \
                on given chemical properties. \
                
                You are specialized in answering questions concerning the {specialization}. \
                
                The following dictionary describes the available data to answer the request: \
                
                {categorized_information}
        """

        self.output_definition = """\n \
                Provide an answer in JSON format containing a list of the keys from the dictionary above and your parameter choice: \
        
                {
                    response: {
                            <information_acronym>: { \
                                <parameter_type>: <parameter>, \
                                ...
                        }, # e.g. 'confmat': {'kind': 'test'}\
                        ...
                    }
                    explanation: string # Why did you choose to respond in this way?
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