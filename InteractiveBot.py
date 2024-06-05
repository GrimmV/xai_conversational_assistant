from defined_texts import intro_visuals, structure_visuals_model
from openai import OpenAI
import json


class InteractiveBot:

    def __init__(self) -> None:

        self.llm = OpenAI()
        self.model = "gpt-4-turbo-preview"

        self.data_format_instructions = 'Output a JSON in the following format: \n{ \
            "needData": bool  // if data is needed to answer the given question \
            "data": list({name, parameters})  // list of the needed data and active parameters to answer the user question. \
        }'

        self.visuals_format_instructions = 'Output a JSON in the following format: \n{ \
            "needVisual": bool  // if data is needed to answer the given question \
            "components": list({name, parameters})  // The necessary data and active parameters to answer the user question \
        }'

        self.data_system_message = f"{intro_visuals}\n{structure_visuals_model}\n{self.visuals_format_instructions}"

    def handle_request(self, request="How does the model perform?"):

        response = self.llm.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.data_system_message},
                {"role": "user", "content": request},
            ],
        )

        output = response.choices[0].message.content

        self.get_visualization_info(output)

        dict_output = json.loads(output)

        return output

    def get_visualization_info(self, dataInfo):
        pass