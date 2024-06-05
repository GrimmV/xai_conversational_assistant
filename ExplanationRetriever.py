explanation = {
    "confusion": "Contains the number of occurrences for each label-prediction pair",
    "learning_curve": "Contains information about how the train and test score (f1-score) changed throughout the training process",
    "scores": "Different evaluation metrics (f1-score, precision, recall) for the specified dataset",
    "feature_relevance": "Shows the relevance of each feature (possibly with respect to a given prediction) based on the absolute sum of SHAP values over the test data.",
    "statistics": "General statistics over the features/labels, like count, mean, ...",
    "distribution": "Distribution of the feature-values over the value range (histogram)"
}


class ExplanationRetriever:

    def __init__(self) -> None:
        # To be implemented
        pass

    def get_explanation(self, key):
        return explanation[key]
