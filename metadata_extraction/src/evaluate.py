import pandas as pd
import re
from difflib import SequenceMatcher
import dateparser

def normalize_text(text, is_date=False, is_renewal=False, is_value=False):
    text = str(text).strip().lower()

    if is_date:
        parsed = dateparser.parse(text)
        if parsed:
            return parsed.strftime("%d.%m.%Y")

    if is_renewal:
        # Convert "11 months" → 330 days, "60 days" → 60
        if "month" in text:
            match = re.search(r'\d+', text)
            if match:
                return str(int(match.group()) * 30)
        elif "day" in text:
            match = re.search(r'\d+', text)
            if match:
                return str(int(match.group()))
        elif re.match(r'\d+$', text):
            return text

    if is_value:
        # Remove Rs., commas, etc. and return numeric string
        text = text.replace(",", "")
        text = re.sub(r'(rupees|rs|only|/-)', '', text)
        match = re.search(r'\d+(\.\d+)?', text)
        return match.group() if match else text

    # Remove role titles for party names, punctuation
    text = re.sub(r'\b(sri|mr|mrs|ms|shri|dr|m/s|lessor|lessee|tenant|owner|party|agent|heir|witness|subordinate|etc)\b', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def is_match(pred, true, field=None, threshold=0.8):
    is_date_field = field and "date" in field.lower()
    is_renewal_field = field and "renewal" in field.lower()
    is_value_field = field and "value" in field.lower()

    norm_pred = normalize_text(pred, is_date=is_date_field, is_renewal=is_renewal_field, is_value=is_value_field)
    norm_true = normalize_text(true, is_date=is_date_field, is_renewal=is_renewal_field, is_value=is_value_field)

    # If it's a value field, compare numerically
    if is_value_field:
        try:
            return int(float(norm_pred)) == int(float(norm_true))
        except:
            return False

    # Otherwise, use fuzzy match
    return SequenceMatcher(None, norm_pred, norm_true).ratio() >= threshold

def evaluate_predictions(pred_file, true_file):
    pred_df = pd.read_csv(pred_file)
    true_df = pd.read_csv(true_file)

    fields = ["Agreement Value", "Agreement Start Date", "Agreement End Date", 
              "Renewal Notice", "Party One", "Party Two"]

    total = len(true_df)
    field_correct = {field: 0 for field in fields}

    for i in range(total):
        for field in fields:
            pred = pred_df.loc[i, field]
            true = true_df.loc[i, field]
            if is_match(pred, true, field):
                field_correct[field] += 1

    print("\n📊 Per-field Recall:")
    for field in fields:
        recall = field_correct[field] / total
        print(f"{field}: {recall:.2f}")

    avg_recall = sum(field_correct.values()) / (total * len(fields))
    print(f"\n📈 Average Recall: {avg_recall:.2f}")
