import folium
import matplotlib.pyplot as plt
import pandas as pd

# Load data
data = pd.read_csv('nato_members.csv')

# Create map
m = folium.Map(location=[52.5200, 13.4050], zoom_start=4)

# Add countries to map
for index, row in data.iterrows():
    folium.Polygon([(row['lat'], row['lon'])], color='blue', fill=True).add_to(m)

# Create timeline
plt.figure(figsize=(10, 6))
plt.bar(data['Year Joined NATO'], data['Country'], color='blue')
plt.xlabel('Year')
plt.ylabel('Country')
plt.title('NATO Membership Timeline')
plt.show()

# Save map as HTML
m.save('nato_map.html')

# Use a video editing software to combine the map and timeline

