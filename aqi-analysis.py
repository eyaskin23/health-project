import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('US_AQI.csv')

# # Display the first 5 rows
# print(df.head())

# state_aqi = df.groupby('state_name')['AQI'].mean().sort_values()

# # Plot the bar chart
# plt.figure(figsize=(12, 8))
# state_aqi.plot(kind='bar', color='skyblue')
# plt.title('Average AQI by State')
# plt.xlabel('State')
# plt.ylabel('Average AQI')
# plt.xticks(rotation=45)
# plt.show()


# Extend the data dictionary for the full data to include the relevant columns
data = {
    "City": ["Detroit, MI", "Cleveland, OH", "Memphis, TN", "Milwaukee, WI", "Philadelphia, PA", "Baltimore, MD", "Columbus, OH", "Kansas City, MO", "Tulsa, OK", "Wichita, KS", "New Orleans, LA", "Jacksonville, FL", "Oklahoma City, OK", "Las Vegas, NV", "Tampa, FL", "Omaha, NE", "Tucson, AZ", "Brookhaven, NY", "Aurora, CO", "Virginia Beach, VA", "Miami, FL", "Fort Worth, TX", "Dallas, TX", "Phoenix, AZ", "Chicago, IL", "Houston, TX", "Arlington, TX", "Fresno, CA", "Mesa, AZ", "Charlotte, NC", "Bakersfield, CA", "Portland, OR", "Raleigh, NC", "Colorado Springs, CO", "Minneapolis, MN", "Boston, MA", "Atlanta, GA", "Denver, CO", "San Antonio, TX", "Albuquerque, NM", "El Paso, TX", "New York, NY", "Sacramento, CA", "Long Beach, CA", "Oakland, CA", "Los Angeles, CA", "Austin, TX", "Anaheim, CA", "San Diego, CA", "San Francisco, CA", "San Jose, CA", "Seattle, WA"],
    "Percentage of adults who smoke": [28.9, 27.8, 24.3, 23.1, 21.8, 21.7, 21.4, 21.1, 20.3, 20.0, 19.8, 19.7, 19.6, 19.3, 19.1, 18.7, 18.6, 18.5, 18.4, 18.2, 17.5, 17.5, 17.5, 17.4, 17.4, 17.1, 16.7, 16.6, 16.4, 16.4, 16.1, 16.1, 16.1, 16.0, 15.6, 15.5, 15.5, 15.5, 15.4, 15.4, 15.1, 15.1, 14.8, 13.7, 13.7, 13.4, 13.3, 12.7, 12.7, 11.8, 10.9, 10.3],
    "Percentage of adults with coronary heart disease": [8.9, 9.0, 7.3, 6.0, 6.2, 6.0, 5.6, 6.0, 7.5, 6.7, 6.5, 6.8, 7.3, 6.8, 6.3, 5.1, 6.6, 8.5, 4.6, 4.9, 8.5, 6.0, 6.0, 5.4, 5.4, 6.1, 5.5, 6.0, 6.4, 5.0, 5.5, 5.2, 4.5, 5.0, 4.0, 4.5, 5.0, 4.5, 6.7, 5.4, 6.7, 5.7, 5.3, 4.7, 5.0, 4.9, 4.3, 4.9, 4.5, 4.5, 4.2, 4.1]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Filter for California cities
california_cities = df[df['City'].str.contains('CA')]

# Visualization
plt.figure(figsize=(12, 6))
plt.barh(california_cities['City'], california_cities['Percentage of adults who smoke'], color='green', label='California Cities')
plt.axvline(df['Percentage of adults who smoke'].mean(), color='red', linestyle='--', label='National Average')

plt.xlabel('Percentage of adults who smoke')
plt.title('Smoking Rates in California Cities vs National Average')
plt.legend()
plt.grid(True)
plt.show()
