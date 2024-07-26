import PyPDF2
import pandas as pd
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def process_extracted_text(text):
    # Split the text into lines
    lines = text.split('\n')

    # Initialize a dictionary to store the results
    results = {
        'Test': [],
        'Value': [],
        'Reference Range': [],
        'Collected Date': [],
        'Received Date': [],
        'Reported Date': []
    }

    # Regex patterns to match different fields
    test_pattern = re.compile(r'^(WBC|RBC|HGB|HCT|MCV|MCH|MCHC|RDW|PLT|MPV|Hemoglobin A1c)')
    date_pattern = re.compile(r'Collected:\s*(\d{2}/\d{2}/\d{4} \d{2}:\d{2} [APM]{2})\s*Received:\s*(\d{2}/\d{2}/\d{4} \d{2}:\d{2} [APM]{2})\s*Reported:\s*(\d{2}/\d{2}/\d{4})')

    current_dates = {}

    for line in lines:
        # Extract the dates if present
        date_match = date_pattern.search(line)
        if date_match:
            current_dates['Collected Date'] = date_match.group(1)
            current_dates['Received Date'] = date_match.group(2)
            current_dates['Reported Date'] = date_match.group(3)
            continue

        # Extract the test result if present
        test_match = test_pattern.match(line)
        if test_match:
            parts = line.split()
            test_name = parts[0]
            test_value = parts[1]
            reference_range = ' '.join(parts[2:])
            
            results['Test'].append(test_name)
            results['Value'].append(test_value)
            results['Reference Range'].append(reference_range)
            results['Collected Date'].append(current_dates.get('Collected Date', ''))
            results['Received Date'].append(current_dates.get('Received Date', ''))
            results['Reported Date'].append(current_dates.get('Reported Date', ''))

    return results

def create_dataset(results):
    df = pd.DataFrame(results)
    return df

# Define the PDF path
pdf_path = "pdf_folder/pdf1.pdf"

# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Process the extracted text to extract lab results and other information
lab_results = process_extracted_text(extracted_text)

# Create a dataset
dataset = create_dataset(lab_results)

# Print the dataset
#print(dataset)

dataset.head

# Save the dataset to a CSV file
dataset.to_csv("lab_results.csv", index=False)

