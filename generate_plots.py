import io
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_to_svg(data, test):
    plt.figure(figsize=(3, 2))
    plt.plot(range(len(data)), data, marker='o', linestyle='-', color='b')
    plt.title(test)
    plt.xlabel('Time')
    plt.ylabel('Value')
    img = io.BytesIO()
    plt.savefig(img, format='svg')
    img.seek(0)
    svg_data = img.getvalue().decode()
    plt.close()
    return svg_data

def generate_plots():
    # Example time-series data
    time_series_data = {
        "WBC": [6.1, 6.3, 6.2, 6.4, 6.1],
        "RBC": [4.7, 4.8, 4.9, 4.8, 4.9],
        "HGB": [13.2, 13.3, 13.5, 13.4, 13.3],
        "HCT": [40.0, 41.0, 42.0, 41.0, 40.5],
        "MCV": [85.0, 84.5, 84.0, 83.5, 84.0],
        "MCH": [28.0, 27.5, 27.0, 26.5, 27.0],
        "MCHC": [33.0, 32.5, 32.0, 32.5, 32.0],
        "RDW": [13.5, 13.6, 13.7, 13.8, 13.7],
        "PLATELET COUNT": [220, 230, 240, 235, 225],
        "Hemoglobin A1c": [5.5, 5.4, 5.3, 5.4, 5.5],
        "Glucose": [100, 98, 95, 97, 96]
    }

    output_dir = 'static/plots'
    os.makedirs(output_dir, exist_ok=True)

    for test, values in time_series_data.items():
        svg_data = plot_to_svg(values, test)
        plot_path = os.path.join(output_dir, f'{test}.svg')
        with open(plot_path, 'w') as f:
            f.write(svg_data)

    print(f"Plots saved in: {output_dir}")

if __name__ == "__main__":
    generate_plots()
