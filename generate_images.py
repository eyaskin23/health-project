import matplotlib.pyplot as plt
from utils.pdf_utils import extract_text_from_pdf, parse_pdf_text
import os

def visualize_lab_results(data, output_folder):
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

    def create_number_line(ax, value, min_val, max_val, title):
        all_range = [min_val - 10, max_val + 10]  # Adjust the overall range for visualization

        ax.hlines(0, all_range[0], all_range[1], color='lightgray', linewidth=8)
        ax.hlines(0, min_val, max_val, color='lightgreen', linewidth=8)
        ax.plot([value], [0], 'ks', markersize=12)  # Black square for the specific value

        ax.set_xlim(all_range[0], all_range[1])
        ax.set_yticks([])
        ax.set_title(title, fontsize=14, pad=20)

        ax.annotate(f'{value}', xy=(value, 0), xytext=(0, -30), textcoords='offset points',
                    bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'),
                    ha='center', fontsize=12)
        ax.annotate(f'{min_val}', xy=(min_val, 0), xytext=(0, 10), textcoords='offset points',
                    ha='center', fontsize=10, color='gray')
        ax.annotate(f'{max_val}', xy=(max_val, 0), xytext=(0, 10), textcoords='offset points',
                    ha='center', fontsize=10, color='gray')

    for test, value in data.items():
        fig, ax = plt.subplots(figsize=(12, 4))  # Adjusted figsize for better fit
        min_val, max_val = reference_ranges[test]
        create_number_line(ax, value, min_val, max_val, test)
        image_path = f"{output_folder}/{test}.svg"
        plt.savefig(image_path, format='svg')
        plt.close()

def process_pdf(pdf_path, output_folder):
    text = extract_text_from_pdf(pdf_path)
    data = parse_pdf_text(text)
    visualize_lab_results(data, output_folder)
    return {test: f"{output_folder}/{test}.svg" for test in data}

# Main Execution (Example for testing)
if __name__ == "__main__":
    pdf_path = 'pdf_folder/pdf1.pdf'  # Ensure this path is correct
    output_folder = 'static/plots'  # Ensure this path is correct
    os.makedirs(output_folder, exist_ok=True)
    process_pdf(pdf_path, output_folder)
