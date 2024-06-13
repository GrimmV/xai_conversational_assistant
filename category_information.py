category_information = {
    "Model": {
        "Confusion Matrix": {
            "acronym": "confusion",
            "description": "Actual labels in relation to the model predictions",
            "parameters": ["kind: str, either 'train' or 'test'"],
        },
        "Performance Metrics": {
            "acronym": "scores",
            "description": "Model performance metrics that show f1-score, precision and recall",
            "parameters": ["kind: str, either 'train' or 'test'"],
        },
        "Learning Curve": {
            "acronym": "learning_curve",
            "description": "Model performance with respect to the model evolution while increasing number of seen datapoints",
            "parameters": [
                "kinds: list[str], allowed strings in the list: 'train', 'test'"
            ],
        },
        "Feature Relevance": {
            "acronym": "feature_relevance",
            "description": "How the model perceives the relevance of individual features. Based on the absolute sum of SHAP values over the test data.",
            "parameters": [
                "class: string, either the specific output class or 'all'"
            ],
        },
    },
    "Data": {
        "Statistics": {
            "acronym": "statistics",
            "description": "General statistics over the features/labels, like count, mean, ...",
            "parameters": [
                "kind: str, either 'train', 'test' or 'full'",
                "class_list: str | List[str], either 'all' or a list of the classes",
                "feature_list: str | List[str], either 'all' or a list of the features of interrest"
            ]
        },
        "Distribution": {
            "acronym": "distribution",
            "description": "Distribution of the feature-values over the value range (histogram)",
            "parameters": [
                "feature: str, feature to inspect",
                "class_list: str | List[str], either 'all' or a list of the classes",
                "kind: str, either 'train' or 'test'",
                "bins: int | str, either a number or 'auto' for automatic calculation of bins"
            ]
        }
    }
}
