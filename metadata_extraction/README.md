# Metadata Extraction from Contracts

This project extracts metadata from `.docx` and `.png` documents using an AI-based Question Answering model.

## Extracted Metadata Fields
- Agreement Value
- Agreement Start Date
- Agreement End Date
- Renewal Notice
- Party One
- Party Two

##  Setup Instructions

bash
pip install -r requirements.txt


##  Train Model

--python
from src.dataset import MetadataDataset
from src.train import train_model

dataset = MetadataDataset("data/train.csv", "data/train").get_data()
train_model(dataset, output_dir="model")
```

## Predict

```python
from src.predict import run_prediction
run_prediction("data/test.csv", "data/test", model_path="model", output_csv_path="predictions.csv")
```

## Evaluate

```python
from src.evaluate import evaluate_predictions
evaluate_predictions("data/test.csv", "predictions.csv")
```

## Run API

```bash
uvicorn app.main:app --reload
```
 ## NOTE
 when u run the program and if u get 404 NOT FOUND that means your FastAPI app is running perfectly fine!
 Then run with by using URL  http://127.0.0.1:8000/docs

## After running u will open with the interface as FASTAPI
Step1: Click on extract metadata
Step2: On the Right Side u will Have try it out click on it
Step3: Choose any document file and click execute
Step4: you will get the output in json form and u can also download it. 

## For Per Field Recall
#run python test_model.py

POST to `/extract` with a `.docx` or `.png` file to get metadata.

## 📁 Project Structure

```
metadata_extraction/
├── app/
│   └── main.py
├── src/
│   ├── dataset.py
│   ├── evaluate.py
│   ├── model.py
│   ├── parser.py
│   ├── predict.py
│   └── train.py
├── requirements.txt
├── README.md
└── run.sh
```
