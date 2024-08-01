import matplotlib.pyplot as plt
import os

def air_quality_gauge(value, save_path=None):
    # Determine the color based on the air quality value
    if value <= 50:
        color = 'green'
        status = 'Good'
    elif value <= 100:
        color = 'yellow'
        status = 'Moderate'
    else:
        color = 'red'
        status = 'Unhealthy'
    
    # Create a figure and an axes
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Create a filled circle
    circle = plt.Circle((0.5, 0.5), 0.4, color=color, ec='black', lw=2)
    
    # Add the circle to the axes
    ax.add_patch(circle)
    
    # Add the text inside the circle
    plt.text(0.5, 0.55, f'{value}', horizontalalignment='center', verticalalignment='center', fontsize=50, color='black', transform=ax.transAxes)
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
    
    plt.title("Fresno Air Quality", pad=20)
    
    if save_path:
        plt.savefig(save_path, format='svg')
    
    plt.show()

# Example usage to show the visualization and save it
air_quality_value = 75  # Replace with actual air quality value for Fresno
save_directory = 'static/plots'
os.makedirs(save_directory, exist_ok=True)
save_path = os.path.join(save_directory, 'fresno_aqi.svg')
air_quality_gauge(air_quality_value, save_path)
