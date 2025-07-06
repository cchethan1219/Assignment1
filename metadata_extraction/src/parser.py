import os
import pytesseract
from PIL import Image
from docx import Document

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return ""

def extract_text_from_image(file_path):
    try:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"❌ Error reading image {file_path}: {e}")
        return ""

def parse_document(file_path):
    print(f"🔍 Checking file: {file_path}")
    
    # If file exists exactly, try to parse it
    if os.path.exists(file_path):
        if file_path.lower().endswith(".docx"):
            return extract_text_from_docx(file_path)
        elif file_path.lower().endswith(".png"):
            return extract_text_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    
    # If file has no extension, try adding common ones
    for ext in [".docx", ".png"]:
        alt_path = file_path + ext
        if os.path.exists(alt_path):
            print(f"🔄 Trying fallback file: {alt_path}")
            return parse_document(alt_path)
    
    raise ValueError(f"File not found or unsupported format: {file_path}")
