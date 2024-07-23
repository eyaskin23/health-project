import PyPDF2
import matplotlib.pyplot as plt
import numpy as np

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
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

def visualize_lab_results(data):
    num_tests = len(data)
    cols = 2
    rows = (num_tests // cols) + (num_tests % cols > 0)
    fig, ax = plt.subplots(rows, cols, figsize=(16, 8))
    fig.tight_layout(pad=5.0)
    
    reference_ranges = {
        "WBC": (4.0, 10.1),
        "RBC": (3.58, 5.19),
        "HGB": (11.0, 15.5),
        "HCT": (31.5, 44.8),
        "MCV": (78.0, 98.0),
        "MCH": (25.2, 32.6),
        "MCHC": (31.0, 34.7),
        "RDW": (12.0, 15.5),
        "PLATELET COUNT": (140, 425),
        "Hemoglobin A1c": (0.0, 5.7),
        "Glucose": (70, 99)
    }

    ax = ax.flatten()
    for i, (test, value) in enumerate(data.items()):
        ref_range = reference_ranges[test]
        all_range = [ref_range[0] - 10, ref_range[1] + 10]  # Adjust the overall range for visualization
        
        ax[i].hlines(0, all_range[0], all_range[1], color='lightgray', linewidth=8)
        ax[i].hlines(0, ref_range[0], ref_range[1], color='lightgreen', linewidth=8)
        ax[i].plot([value], [0], 'ks', markersize=12)  # Black square for the specific value
        
        ax[i].set_xlim(all_range[0], all_range[1])
        ax[i].set_yticks([])
        ax[i].set_title(f'{test}', fontsize=14, pad=20)
        
        ax[i].annotate(f'{value}', xy=(value, 0), xytext=(0, -30), textcoords='offset points',
                       bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'),
                       ha='center', fontsize=12)
        ax[i].annotate(f'{ref_range[0]}', xy=(ref_range[0], 0), xytext=(0, 10), textcoords='offset points',
                       ha='center', fontsize=10, color='gray')
        ax[i].annotate(f'{ref_range[1]}', xy=(ref_range[1], 0), xytext=(0, 10), textcoords='offset points',
                       ha='center', fontsize=10, color='gray')
    
    for j in range(i + 1, len(ax)):
        fig.delaxes(ax[j])  # Remove unused subplots
    
    plt.show()

# Main Execution
pdf_path = 'pdf_folder/pdf1.pdf'  # Update the path to your PDF file
text = extract_text_from_pdf(pdf_path)
data = parse_pdf_text(text)
visualize_lab_results(data)
