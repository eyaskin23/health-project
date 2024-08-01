import pandas as pd

data = {
    "Rank": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
             21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
             41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52],
    "City": ["Detroit, MI", "Cleveland, OH", "Memphis, TN", "Milwaukee, WI", "Philadelphia, PA",
             "Baltimore, MD", "Columbus, OH", "Kansas City, MO", "Tulsa, OK", "Wichita, KS",
             "New Orleans, LA", "Jacksonville, FL", "Oklahoma City, OK", "Las Vegas, NV", "Tampa, FL",
             "Omaha, NE", "Tucson, AZ", "Brookhaven, NY", "Aurora, CO", "Virginia Beach, VA",
             "Miami, FL", "Fort Worth, TX", "Dallas, TX", "Phoenix, AZ", "Chicago, IL",
             "Houston, TX", "Arlington, TX", "Fresno, CA", "Mesa, AZ", "Charlotte, NC",
             "Bakersfield, CA", "Portland, OR", "Raleigh, NC", "Colorado Springs, CO", "Minneapolis, MN",
             "Boston, MA", "Atlanta, GA", "Denver, CO", "San Antonio, TX", "Albuquerque, NM",
             "El Paso, TX", "New York, NY", "Sacramento, CA", "Long Beach, CA", "Oakland, CA",
             "Los Angeles, CA", "Austin, TX", "Anaheim, CA", "San Diego, CA", "San Francisco, CA",
             "San Jose, CA", "Seattle, WA"],
    "Percentage of adults who smoke": [28.9, 27.8, 24.3, 23.1, 21.8, 21.7, 21.4, 21.1, 20.3, 20.0,
                                       19.8, 19.7, 19.6, 19.3, 19.1, 18.7, 18.6, 18.5, 18.4, 18.2,
                                       17.5, 17.5, 17.5, 17.4, 17.4, 17.1, 16.7, 16.6, 16.4, 16.4,
                                       16.1, 16.1, 16.1, 16.0, 15.6, 15.5, 15.5, 15.5, 15.4, 15.4,
                                       15.1, 15.1, 14.8, 13.7, 13.7, 13.4, 13.3, 12.7, 12.7, 11.8,
                                       10.9, 10.3],
    "Percentage of adults in poor physical health": [20.9, 18.7, 17.4, 16.0, 14.8, 13.4, 11.7, 13.6, 14.6, 13.2,
                                                     13.7, 13.9, 14.1, 15.1, 13.9, 11.0, 14.5, 15.0, 11.6, 10.6,
                                                     16.1, 13.9, 13.2, 14.2, 12.0, 13.3, 13.0, 15.4, 14.0, 10.3,
                                                     15.1, 12.6, 9.9, 10.9, 9.7, 11.1, 11.1, 10.0, 13.4, 12.8,
                                                     14.1, 12.1, 13.1, 12.9, 12.8, 13.3, 9.6, 13.1, 11.5, 9.7,
                                                     10.9, 8.8],
    "Percentage of adults with COPD": [11.2, 11.1, 9.3, 6.8, 7.3, 7.4, 7.1, 7.2, 7.8, 7.1,
                                       7.5, 8.2, 7.5, 7.7, 7.5, 6.0, 6.6, 9.4, 5.2, 5.5,
                                       7.5, 6.3, 6.2, 6.2, 6.1, 6.1, 6.0, 6.4, 7.0, 5.5,
                                       6.2, 5.4, 5.0, 5.2, 3.8, 4.7, 5.7, 4.4, 6.0, 5.6,
                                       5.9, 6.1, 5.6, 5.2, 5.1, 5.2, 4.1, 5.0, 4.3, 3.9,
                                       3.9, 3.5],
    "Percentage of adults with cancer": [6.0, 5.9, 5.6, 5.3, 5.8, 5.7, 5.1, 6.0, 6.6, 6.4,
                                         5.5, 6.0, 6.1, 6.1, 5.5, 6.1, 5.9, 8.5, 5.4, 5.9,
                                         5.6, 5.2, 5.0, 5.4, 5.2, 4.8, 5.3, 5.2, 6.8, 5.3,
                                         5.2, 5.9, 5.2, 5.9, 4.4, 4.8, 4.9, 5.4, 5.2, 5.9,
                                         5.2, 5.6, 5.4, 5.0, 5.2, 5.1, 4.4, 5.0, 5.3, 5.2,
                                         5.0, 5.7],
    "Percentage of adults who have experienced a stroke": [6.2, 5.6, 4.8, 3.7, 4.1, 4.4, 3.1, 3.6, 3.7, 3.3,
                                                           4.3, 3.6, 3.5, 3.3, 3.5, 3.0, 3.2, 3.8, 2.7, 2.6,
                                                           4.2, 3.2, 3.4, 2.9, 3.4, 3.3, 2.8, 3.4, 3.3, 2.9,
                                                           3.1, 2.6, 2.5, 2.7, 2.4, 2.6, 3.5, 2.4, 3.2, 2.9,
                                                           3.3, 3.2, 3.1, 2.8, 3.2, 2.9, 2.1, 2.6, 2.4, 2.4,
                                                           2.3, 2.1]
}

df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('smoker_data.csv', index=False)