from fastapi import FastAPI, UploadFile, File
from src.parser import parse_document
from src.model import MetadataExtractorModel
import shutil
import os

app = FastAPI()
model = MetadataExtractorModel()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/extract")
async def extract_metadata(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = parse_document(file_path)
    result = model.extract_metadata(text)
    os.remove(file_path)
    return {"file_name": file.filename, "extracted_metadata": result}