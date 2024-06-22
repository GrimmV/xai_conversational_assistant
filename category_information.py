category_information = {
    "Model": {
        "Confusion Matrix": {
            "description": "Actual labels in relation to the model predictions",
            "parameters": ["kind: str, either 'train' or 'test'"],
        },
        "Performance Metrics": {
            "description": "Model performance metrics that show f1-score, precision and recall",
            "parameters": ["kind: str, either 'train' or 'test'"],
        },
        "Learning Curve": {
            "description": "Model performance with respect to the model evolution while increasing number of seen datapoints",
            "parameters": [
                "kinds: list[str], allowed strings in the list: 'train', 'test'"
            ],
        },
        "Feature Relevance": {
            "description": "How the model perceives the relevance of individual features. Based on the absolute sum of SHAP values over the test data.",
            "parameters": ["class: string, either the specific output class or 'all'"],
        },
    },
    "Data": {
        "Datapoint": {
            "description": "Individual datapoint under investigation and model prediction",
            "parameters": [
                "with_impact: bool, if you fetch additional feature impact information based on shap values",
            ],
        },
        "Statistics": {
            "description": "General statistics over the features/labels, like count, mean, ...",
            "parameters": [
                "kind: str, either 'train', 'test' or 'full'",
                "class_list: str | List[str], either 'all' or a list of the classes",
                "feature_list: str | List[str], either 'all' or a list of the features of interrest",
            ],
        },
        "Distribution": {
            "description": "Distribution of the feature-values over the value range (histogram)",
            "parameters": [
                "feature: str, feature to inspect",
                "class_list: str | List[str], either 'all' or a list of the classes",
                "kind: str, either 'train' or 'test'",
                "bins: int | str, either a number or 'auto' for automatic calculation of bins",
            ],
        },
        "Correlation": {
            "description": "Description of the correlation between each two individual features",
            "parameters": [
                "kind: str, either 'train', 'test' or 'full'",
            ],
        },
    },
    "Prediction": {
        "Datapoint": {
            "description": "Individual datapoint under investigation and model prediction",
            "parameters": [
                "with_impact: bool, if you fetch additional feature impact information based on shap values",
            ],
        },
        "Probabilities": {
            "description": "The probabilities of different predictions being correct based on the model.",
            "parameters": None,
        },
        "Trustscore": {
            "description": "The trustscore for the given class, closest class that was not predicted and the percentile of this trustscore among all trustscores in the dataset",
            "parameters": None,
        },
    },
    "Context": {
        "Datapoint": {
            "description": "Individual datapoint under investigation and model prediction",
            "parameters": [
                "with_impact: bool, if you fetch additional feature impact information based on shap values",
            ],
        },
        "Context": {
            "description": "Condensed information about an individual feature value for a prediction and how it is embedded in the prediction space. \
                Contains feature value, overall feature distribution, anchor rules, prediction-based feature distribution, and shap value with respect to the chosen class",
            "parameters": [
                "feature: str, name of the feature to focus on",
                "class: str, class to focus on. If 'auto', the model prediction of the datapoint at hand is used for class.",
            ],
        }
    },
}
