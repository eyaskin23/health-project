
import pandas as pd
import matplotlib.pyplot as plt

# Data input
data = {
    "City": ["Detroit, MI", "Cleveland, OH", "Memphis, TN", "Milwaukee, WI", "Philadelphia, PA", "Baltimore, MD", "Columbus, OH", "Kansas City, MO", "Tulsa, OK", "Wichita, KS", "New Orleans, LA", "Jacksonville, FL", "Oklahoma City, OK", "Las Vegas, NV", "Tampa, FL", "Omaha, NE", "Tucson, AZ", "Brookhaven, NY", "Aurora, CO", "Virginia Beach, VA", "Miami, FL", "Fort Worth, TX", "Dallas, TX", "Phoenix, AZ", "Chicago, IL", "Houston, TX", "Arlington, TX", "Fresno, CA", "Mesa, AZ", "Charlotte, NC", "Bakersfield, CA", "Portland, OR", "Raleigh, NC", "Colorado Springs, CO", "Minneapolis, MN", "Boston, MA", "Atlanta, GA", "Denver, CO", "San Antonio, TX", "Albuquerque, NM", "El Paso, TX", "New York, NY", "Sacramento, CA", "Long Beach, CA", "Oakland, CA", "Los Angeles, CA", "Austin, TX", "Anaheim, CA", "San Diego, CA", "San Francisco, CA", "San Jose, CA", "Seattle, WA"],
    "Percentage of adults who smoke": [28.9, 27.8, 24.3, 23.1, 21.8, 21.7, 21.4, 21.1, 20.3, 20.0, 19.8, 19.7, 19.6, 19.3, 19.1, 18.7, 18.6, 18.5, 18.4, 18.2, 17.5, 17.5, 17.5, 17.4, 17.4, 17.1, 16.7, 16.6, 16.4, 16.4, 16.1, 16.1, 16.1, 16.0, 15.6, 15.5, 15.5, 15.5, 15.4, 15.4, 15.1, 15.1, 14.8, 13.7, 13.7, 13.4, 13.3, 12.7, 12.7, 11.8, 10.9, 10.3],
    "Air Quality Index": [60, 58, 72, 50, 55, 57, 45, 48, 53, 51, 54, 56, 52, 59, 60, 47, 55, 58, 46, 49, 62, 61, 59, 57, 56, 54, 53, 75, 70, 65, 68, 67, 66, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Filter for California cities
california_cities = df[df['City'].str.contains('CA')]
# Save the visualization as an SVG file
plt.figure(figsize=(30, 30))

# Plot smoking rates
plt.plot(california_cities['City'], california_cities['Percentage of adults who smoke'], marker='o', label='Smoking Rates')

# Plot air quality index
plt.plot(california_cities['City'], california_cities['Air Quality Index'], marker='s', label='Air Quality Index', linestyle='--')

# Highlight Fresno
plt.plot('Fresno, CA', california_cities[california_cities['City'] == 'Fresno, CA']['Percentage of adults who smoke'], marker='o', markersize=10, color='red', label='Fresno Smoking Rate')
plt.plot('Fresno, CA', california_cities[california_cities['City'] == 'Fresno, CA']['Air Quality Index'], marker='s', markersize=10, color='red', label='Fresno Air Quality')

plt.title('Smoking Rates and Air Quality in California Cities')
plt.xlabel('City')
plt.ylabel('Percentage / Air Quality Index')
plt.legend()
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()

# Save as SVG
plt.savefig('static/plots/california.svg', format='svg')

plt.show()
