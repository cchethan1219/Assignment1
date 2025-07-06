import os
import pandas as pd
from src.parser import parse_document
from src.model import MetadataExtractorModel

# Predicts metadata fields for all documents in test set
def run_prediction(test_csv_path, test_folder_path, model_path="deepset/roberta-base-squad2", output_csv_path="predictions.csv"):
    df = pd.read_csv(test_csv_path)
    extractor = MetadataExtractorModel(model_name=model_path)

    predictions = []
    for idx, row in df.iterrows():
        file_name = row["file_name"]
        file_path = os.path.join(test_folder_path, file_name)
        text = parse_document(file_path)
        pred = extractor.extract_metadata(text)
        pred["file_name"] = file_name
        predictions.append(pred)

    result_df = pd.DataFrame(predictions)
    result_df.to_csv(output_csv_path, index=False)
    print(f"Predictions saved to {output_csv_path}")
