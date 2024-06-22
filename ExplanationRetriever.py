from acronyms import acronyms

explanation = {
    "confusion": "Contains the number of occurrences for each label-prediction pair",
    "learning_curve": "Contains information about how the train and test score (f1-score) changed throughout the training process",
    "scores": "Different evaluation metrics (f1-score, precision, recall) for the specified dataset",
    "feature_relevance": "Shows the relevance of each feature (possibly with respect to a given prediction) based on the absolute sum of SHAP values over the test data.",
    "statistics": "General statistics over the features/labels, like count, mean, ...",
    "distribution": "Distribution of the feature-values over the value range (histogram)",
    "datapoint": "Datapoint values and prediction for the datapoint under investigation. Might contain feature impact information based on shap.",
    "correlation": "Correlation between each pair of features in the dataset.",
    "context": "Condensed information about an individual feature value for a prediction and how it is embedded in the prediction space. \
                Contains feature value, overall feature distribution, anchor rules, prediction-based feature distribution, and shap value with respect to the chosen class",
    "trustscore": "Trustscore for the given class, closest class that was not predicted and the percentile of this trustscore among all trustscores in the dataset",
    "probabilities": "Probabilities of different predictions being correct based on the model"
}


class ExplanationRetriever:

    def __init__(self) -> None:
        # To be implemented
        pass

    def get_explanation(self, key):
        acronym = acronyms[key]
        return explanation[acronym]
