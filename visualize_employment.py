import matplotlib.pyplot as plt
import pandas as pd
import os

# df = pd.read_csv('unemployment.csv').head(5)

# # Create a DataFrame with state and unemployment rate
# state_unemployment_df = df[['State/Area', 'Percent (%) of Labor Force Unemployed in State/Area']]

# # Convert unemployment rate to numeric, removing any non-numeric characters
# state_unemployment_df['Percent (%) of Labor Force Unemployed in State/Area'] = pd.to_numeric(state_unemployment_df['Percent (%) of Labor Force Unemployed in State/Area'], errors='coerce')

# # Group by state and calculate the average unemployment rate for each state
# average_unemployment_by_state = state_unemployment_df.groupby('State/Area').mean().reset_index()

# # Sort by the average unemployment rate
# average_unemployment_by_state = average_unemployment_by_state.sort_values(by='Percent (%) of Labor Force Unemployed in State/Area', ascending=False)

# # Plot the data
# plt.figure(figsize=(10, 8))
# plt.barh(average_unemployment_by_state['State/Area'], average_unemployment_by_state['Percent (%) of Labor Force Unemployed in State/Area'], color='skyblue')
# plt.xlabel('Average Unemployment Rate (%)')
# plt.ylabel('State')
# plt.title('Average Unemployment Rate by State')
# plt.gca().invert_yaxis()  # Highest unemployment rate at the top
# plt.grid(axis='x', linestyle='--', alpha=0.7)
# plt.show()

# svg_file_path = 'static/plots/unemployment.svg'
# plt.figure(figsize=(15, 10))
# plt.barh(average_unemployment_by_state['State/Area'], average_unemployment_by_state['Percent (%) of Labor Force Unemployed in State/Area'], color='skyblue')
# plt.xlabel('Average Unemployment Rate (%)')
# plt.ylabel('State')
# plt.title('Average Unemployment Rate by State')
# plt.gca().invert_yaxis()  # Highest unemployment rate at the top
# plt.grid(axis='x', linestyle='--', alpha=0.7)
# plt.savefig(svg_file_path, format='svg')

# import matplotlib.pyplot as plt
# import os

def air_quality_gauge(value, save_path=None):
    # Determine the color based on the air quality value
    if value <= 3.8:
        color = 'green'
        status = 'Good'
    elif value <= 5:
        color = 'yellow'
        status = 'Moderate'
    else:
        color = 'red'
        status = 'Bad'
    
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
    
    plt.title("Fresno Unemployment Rate", pad=20)
    
    if save_path:
        plt.savefig(save_path, format='svg')
    
    plt.show()

# Example usage to show the visualization and save it
air_quality_value = 3.8  # Replace with actual air quality value for Fresno
save_directory = 'static/plots'
os.makedirs(save_directory, exist_ok=True)
save_path = os.path.join(save_directory, 'fresno_unemployment.svg')
air_quality_gauge(air_quality_value, save_path)
