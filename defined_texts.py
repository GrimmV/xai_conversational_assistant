intro = """You are a virtual assistant and help an expert analysing a machine learning model with every request as good as you can. \
        The ML model is specialized in answering questions about the quality of wine based \
        on given chemical properties. The data that is available to answer the \
        question is described as follows:
"""

intro_visuals = """You are a virtual assistant and help an expert analysing a machine learning model with every request as good as you can. \
        The ML model is specialized in answering questions about the quality of wine based \
        on given chemical properties. You are supposed to choose the most fitting visuals for the given request. The available visuals \
        are described as follows:
"""

structure = '''{\
  "confusion": {\
    "explanation": "Contains the number of occurrences for each label-prediction pair",\
    "parameters": {\
      "type": ["train", "test"]\
    },\
    "structure": [\
      {\
        "actual": "number", // label\
        "count": "number",\
        "predicted": "number"\
      }\
    ]\
  },\
  "learning_curve": {\
    "explanation": "Contains information about how the train and test score changed throughout the training process",\
    "parameters": {\
      "type": ["train", "test"]\
    },\
    "structure": [\
      {\
        "n": "number", // number of processed samples\
        "score": "number",\
        "type": "string" // dataset type\
      }\
    ]\
  },\
  "scores": {\
    "explanation": "Different evaluation metrics for the specified dataset",\
    "parameters": {\
      "type": ["train", "test"]\
    },\
    "structure": {\
      "f1": "number",\
      "precision": "number",\
      "recall": "number"\
    }\
  },\
  "feature_importance": {\
    "explanation": "Relevance of each feature with respect to a given prediction",\
    "parameters": \{\},\
    "structure": {\
      "alcohol": "number",\
      "chlorides": "number",\
      "citric acid": "number",\
      "density": "number",\
      "fixed acidity": "number",\
      "free sulfur dioxide": "number",\
      "pH": "number",\
      "residual sugar": "number",\
      "sulphates": "number",\
      "total sulfur dioxide": "number",\
      "volatile acidity": "number"\
    }\
  }\
}\
'''

structure_visuals_model = '''[\
  {"component": "confusionMatrix", "props": {"title": "string"}, "displayableData": ["model_confusion"]},\
  {"component": "learningCurve", "props": {"title": "string"}, "displayableData": ["learning_curve"]},\
  {"component": "text", "props": none, "displayableData": ["model_scores"]},\
  {"component": "barChart", "props": {"title": "string"}, "displayableData": ["global_importance"]},\
]'''