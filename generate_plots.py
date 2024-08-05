import io
import matplotlib.pyplot as plt
import os

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

def plot_to_svg(value, test, min_val, max_val):
    fig, ax = plt.subplots(figsize=(10, 2))  # Adjusted figsize for better fit
    create_number_line(ax, value, min_val, max_val, test)
    img = io.BytesIO()
    plt.savefig(img, format='svg', bbox_inches='tight', transparent=True)
    img.seek(0)
    svg_data = img.getvalue().decode()
    plt.close()
    return svg_data

def generate_plots():
    # Example data with reference ranges
    lab_data = {
        "WBC": (6.1, 4.0, 10.1),
        "RBC": (4.7, 3.58, 5.19),
        "HGB": (13.2, 11.0, 15.5),
        "HCT": (40.0, 31.5, 44.8),
        "MCV": (85.0, 78.0, 98.0),
        "MCH": (28.0, 25.2, 32.6),
        "MCHC": (33.0, 31.0, 34.7),
        "RDW": (13.5, 12.0, 15.5),
        "PLATELET_COUNT": (220, 140, 425),
        "Hemoglobin_A1c": (5.5, 0.0, 5.7),
        "Glucose": (100, 70, 99)
    }

    output_dir = 'static/plots'
    os.makedirs(output_dir, exist_ok=True)

    for test, (value, min_val, max_val) in lab_data.items():
        svg_data = plot_to_svg(value, test, min_val, max_val)
        plot_path = os.path.join(output_dir, f'{test}.svg')
        with open(plot_path, 'w') as f:
            f.write(svg_data)

    print(f"Plots saved in: {output_dir}")

if __name__ == "__main__":
    generate_plots()
