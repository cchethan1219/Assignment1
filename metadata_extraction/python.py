from pdf2docx import Converter

def pdf_to_docx(pdf_path, docx_path):
    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
        print(f"✅ Converted PDF to DOCX: {docx_path}")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")

# Example usage
pdf_path = "data/test/228094620-Rental-Agreement.pdf.docx"
docx_path = "data/test/228094620-Rental-Agreement.docx"

pdf_to_docx(pdf_path, docx_path)