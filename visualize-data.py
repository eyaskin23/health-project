import PyPDF2
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=list(data.keys()))
    
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

    for i, (test, value) in enumerate(data.items()):
        ref_range = reference_ranges[test]
        all_range = [ref_range[0] - 10, ref_range[1] + 10]  # Adjust the overall range for visualization
        
        row = (i // cols) + 1
        col = (i % cols) + 1
        
        fig.add_trace(go.Scatter(x=[all_range[0], all_range[1]], y=[0, 0], 
                                 mode='lines', line=dict(color='lightgray', width=8), showlegend=False), 
                      row=row, col=col)
        
        fig.add_trace(go.Scatter(x=[ref_range[0], ref_range[1]], y=[0, 0], 
                                 mode='lines', line=dict(color='lightgreen', width=8), showlegend=False), 
                      row=row, col=col)
        
        fig.add_trace(go.Scatter(x=[value], y=[0], 
                                 mode='markers', marker=dict(color='black', size=12, symbol='square'), showlegend=False), 
                      row=row, col=col)
        
        fig.add_annotation(x=value, y=0, text=f'{value}', showarrow=True, arrowhead=2,
                           ax=0, ay=-30, font=dict(size=12, color='black'),
                           bgcolor='white', bordercolor='black', row=row, col=col)
        
        fig.add_annotation(x=ref_range[0], y=0, text=f'{ref_range[0]}', showarrow=False,
                           yshift=10, font=dict(size=10, color='gray'), row=row, col=col)
        
        fig.add_annotation(x=ref_range[1], y=0, text=f'{ref_range[1]}', showarrow=False,
                           yshift=10, font=dict(size=10, color='gray'), row=row, col=col)
        
    fig.update_layout(height=rows*200, width=800, title_text="Lab Results Visualization", showlegend=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    
    fig.show()

# Main Execution
pdf_path = 'pdf_folder/pdf1.pdf'  # Update the path to your PDF file
text = extract_text_from_pdf(pdf_path)
data = parse_pdf_text(text)
visualize_lab_results(data)
