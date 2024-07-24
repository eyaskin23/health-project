import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''.join(page.extract_text() for page in reader.pages)
    return text

def parse_pdf_text(text):
    data = {}
    lines = text.split("\n")
    
    for line in lines:
        if "WBC" in line and "x10(3)" in line:
            data["WBC"] = float(line.split()[1])
        elif "RBC" in line and "x10(6)" in line:
            data["RBC"] = float(line.split()[1])
        elif "HGB" in line and "g/dL" in line:
            data["HGB"] = float(line.split()[1])
        elif "HCT" in line and "%" in line:
            data["HCT"] = float(line.split()[1])
        elif "MCV" in line and "fL" in line:
            data["MCV"] = float(line.split()[1])
        elif "MCH" in line and "pg" in line:
            data["MCH"] = float(line.split()[1])
        elif "MCHC" in line and "g/dL" in line:
            data["MCHC"] = float(line.split()[1])
        elif "RDW" in line and "%" in line:
            data["RDW"] = float(line.split()[1])
        elif "PLATELET COUNT" in line and "x10(3)/uL" in line:
            try:
                data["PLATELET COUNT"] = float(line.split()[2])
            except ValueError:
                data["PLATELET COUNT"] = float(line.split()[3])
        elif "Hemoglobin A1c" in line and "%" in line:
            data["Hemoglobin A1c"] = float(line.split()[2])
        elif "Glucose" in line and "mg/dL" in line:
            data["Glucose"] = float(line.split()[1])
    return data