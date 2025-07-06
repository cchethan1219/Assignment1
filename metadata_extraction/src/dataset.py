import pandas as pd
import os
from src.parser import parse_document

class MetadataDataset:
    def __init__(self, csv_path, docs_folder):
        self.df = pd.read_csv(csv_path)
        self.docs_folder = docs_folder
        self.data = []
        self.prepare()

    def prepare(self):
        for idx, row in self.df.iterrows():
            file_name = row['file_name']
            file_path = os.path.join(self.docs_folder, file_name)
            text = parse_document(file_path)
            labels = {
                "Agreement Value": row.get("Agreement Value", ""),
                "Agreement Start Date": row.get("Agreement Start Date", ""),
                "Agreement End Date": row.get("Agreement End Date", ""),
                "Renewal Notice": row.get("Renewal Notice", ""),
                "Party One": row.get("Party One", ""),
                "Party Two": row.get("Party Two", "")
            }
            self.data.append((text, labels))

    def get_data(self):
        return self.data
