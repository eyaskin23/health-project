import pandas as pd
import matplotlib.pyplot as plt
import os

def population_gauge(value, save_path=None):
    # Determine the color based on the population value
    if value <= 20000000:  # Example range for "Good"
        color = 'green'
        status = 'Healthy'
    elif value <= 40000000:  # Example range for "Moderate"
        color = 'yellow'
        status = 'Moderate'
    else:  # Example range for "Unhealthy"
        color = 'red'
        status = 'Overpopulated'
    
    # Create a figure and an axes
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Create a filled circle
    circle = plt.Circle((0.5, 0.5), 0.4, color=color, ec='black', lw=2)
    
    # Add the circle to the axes
    ax.add_patch(circle)
    
    # Add the text inside the circle
    plt.text(0.5, 0.55, f'{value}', horizontalalignment='center', verticalalignment='center', fontsize=30, color='black', transform=ax.transAxes)
    plt.text(0.5, 0.45, f'{status}', horizontalalignment='center', verticalalignment='center', fontsize=20, color='black', transform=ax.transAxes)
    
    # Set the x and y axis limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Keep the aspect ratio of the plot square
    ax.set_aspect('equal')
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.title("California Population", pad=20)
    
    if save_path:
        plt.savefig(save_path, format='svg')
    
    plt.show()

# Load the dataset
df = pd.read_csv('state_population_data.csv')

# Filter for California population
california_population = df[df['State'] == 'California']['2022'].values[0]

# Ensure the output directory exists
output_dir = 'static/plots'
os.makedirs(output_dir, exist_ok=True)

# Save the plot as an SVG file
save_path = os.path.join(output_dir, 'california_population.svg')
population_gauge(california_population, save_path)
