from src.predict import run_prediction
from src.evaluate import evaluate_predictions


run_prediction(
    test_csv_path="data/test.csv",
    test_folder_path="data/test",
    model_path="deepset/roberta-base-squad2",
    output_csv_path="predictions.csv"
)

evaluate_predictions("data/test.csv", "predictions.csv")

