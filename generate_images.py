import matplotlib.pyplot as plt

from utils.pdf_utils import extract_text_from_pdf, parse_pdf_text

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

    for test, value in data.items():
        fig, ax = plt.subplots(figsize=(6, 1))
        ref_range = reference_ranges[test]
        all_range = [ref_range[0] - 10, ref_range[1] + 10]  # Adjust the overall range for visualization

        ax.hlines(0, all_range[0], all_range[1], color='lightgray', linewidth=8)
        ax.hlines(0, ref_range[0], ref_range[1], color='lightgreen', linewidth=8)
        ax.plot([value], [0], 'ks', markersize=12)  # Black square for the specific value

        ax.set_xlim(all_range[0], all_range[1])
        ax.set_yticks([])
        ax.set_title(f'{test}', fontsize=14, pad=20)

        ax.annotate(f'{value}', xy=(value, 0), xytext=(0, -30), textcoords='offset points',
                    bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'),
                    ha='center', fontsize=12)
        ax.annotate(f'{ref_range[0]}', xy=(ref_range[0], 0), xytext=(0, 10), textcoords='offset points',
                    ha='center', fontsize=10, color='gray')
        ax.annotate(f'{ref_range[1]}', xy=(ref_range[1], 0), xytext=(0, 10), textcoords='offset points',
                    ha='center', fontsize=10, color='gray')

        image_path = f"{output_folder}/{test}.png"
        plt.savefig(image_path)
        plt.close()

def process_pdf(pdf_path, output_folder):
    text = extract_text_from_pdf(pdf_path)
    data = parse_pdf_text(text)
    visualize_lab_results(data, output_folder)
    return {test: f"{output_folder}/{test}.png" for test in data}

# Main Execution (Example for testing)
if __name__ == "__main__":
    pdf_path = 'pdf_folder/pdf1.pdf'  # Ensure this path is correct
    output_folder = 'static'  # Ensure this path is correct
    process_pdf(pdf_path, output_folder)
