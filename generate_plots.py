import io
import matplotlib.pyplot as plt
import os

def plot_to_png(value, test, reference_range, output_dir):
    fig, ax = plt.subplots(figsize=(6, 2))

    # Plot the normal range
    ax.plot([reference_range[0], reference_range[1]], [0, 0], color='green', linewidth=10, solid_capstyle='butt')

    # Plot the specific value
    ax.plot([value], [0], 'ko', markersize=15)
    ax.text(value, 0.5, f'{value}', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    # Customize plot
    ax.set_xlim(reference_range[0], reference_range[1])
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title(test, fontsize=16)
    
    # Remove the axes for cleaner look
    ax.axis('off')

    # Save the plot as PNG
    img_path = os.path.join(output_dir, f'{test}.png')
    plt.savefig(img_path, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    return img_path

def generate_plots():
    # Example data and reference ranges
    test_data = {
        "WBC": 6.1,
        "RBC": 4.7,
        "HGB": 13.2,
        "HCT": 40.0,
        "MCV": 85.0,
        "MCH": 28.0,
        "MCHC": 33.0,
        "RDW": 13.5,
        "PLATELET COUNT": 220,
        "Hemoglobin A1c": 5.5,
        "Glucose": 100
    }
    
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

    output_dir = 'static/plots'
    os.makedirs(output_dir, exist_ok=True)

    for test, value in test_data.items():
        plot_path = plot_to_png(value, test, reference_ranges[test], output_dir)
        print(f"Plot saved in: {plot_path}")

if __name__ == "__main__":
    generate_plots()
