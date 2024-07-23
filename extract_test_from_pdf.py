import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Define the PDF path
pdf_path = "pdf1.pdf"

# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Print the extracted text
print(extracted_text)
