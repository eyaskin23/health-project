import os
import matplotlib
import matplotlib.pyplot as plt
from flask import current_app

matplotlib.use('Agg')

def visualize_lab_results(data):
    num_tests = len(data)
    cols = 2
    rows = (num_tests // cols) + (num_tests % cols > 0)
    fig, ax = plt.subplots(rows, cols, figsize=(6, 3))  # Adjusted the figure size
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
    
    plot_path = os.path.join(current_app.config['STATIC_FOLDER'], 'lab_results_number_line.png')
    plt.savefig(plot_path)
    plt.close()
    return plot_path
