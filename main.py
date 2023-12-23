import pandas as pd
import folium
from folium.plugins import MarkerCluster
import seaborn as sns

# Read the CSV file
bird_data = pd.read_csv("bird.csv")

# Create a folium map centered around the mean of coordinates
m = folium.Map(location=[bird_data['latitude'].mean(), bird_data['longitude'].mean()], zoom_start=10)

# Create a MarkerCluster for individual observations
marker_cluster = MarkerCluster().add_to(m)

# Generate a color palette based on the number of unique species
n_species = len(bird_data['species'].unique())
color_palette = sns.color_palette("husl", n_species).as_hex()

# Create a dictionary mapping species to colors
species_colors = dict(zip(bird_data['species'].unique(), color_palette))

# Add circles and labels for each observation
for index, row in bird_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,  # Adjust the radius as needed
        color=species_colors.get(row['species'], 'gray'),  # Use gray for unknown species
        fill=True,
        fill_color=species_colors.get(row['species'], 'gray'),
        fill_opacity=0.7,
        popup=f"Species: {row['species']}<br>Count: {row['observedCount']}",
        tooltip=row['species']  # Add tooltip with the species name
    ).add_to(marker_cluster)

# Display the map
m.save("bird_map.html")
