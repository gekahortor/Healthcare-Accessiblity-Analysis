# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "folium==0.20.0",
#     "geopandas==1.1.4",
#     "leafmap==0.63.0",
#     "networkx==3.6.1",
#     "osmnx==2.1.0",
#     "rioxarray==0.22.0",
#     "shapely==2.1.2",
#     "worldpoppy==0.4.1",
#     "xarray==2026.7.0",
# ]
# ///


__generated_with = "0.24.0"

# %%


# %%
import subprocess
import sys

# List of packages to install
packages = [
    "numpy",
    "pandas", 
    "geopandas",
    "rioxarray",
    "xarray",
    "osmnx",
    "matplotlib",
    "networkx",
    "folium",
    "worldpoppy",
    "leafmap",
    "shapely"
]

# Install each package
for package in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# %%
import numpy as np
import pandas as pd
import geopandas as gpd
import rioxarray as rxr
import xarray as xr
import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import folium
import worldpoppy as wpy
import leafmap
import shapely
from worldpoppy import wp_raster
from matplotlib.colors import LogNorm

# %%
# Specify the region for data retrieval
place_name = "Greater Accra Region, Ghana"

# Define tags to filter for hospital locations from OpenStreetMap
tags = {
    "amenity": ["clinic", "hospital"],
    "healthcare": ["clinic", "hospital"]
}

# Download hospital features as a GeoDataFrame for the defined region
hospital = ox.features_from_place(place_name, tags)

# %%
# Drop rows where the 'name' column is NaN
hospitals = hospital.dropna(subset=['name'])

# %%
# Select only the required columns
facilities = hospitals[['name','geometry', 'amenity']]

# %%
facilities['geometry_refined'] = facilities.geometry.apply(lambda geom: geom if geom.geom_type == 'Point' else geom.centroid)

# %%
# Delete the original geometry column and rename geometry_refined to geometry
facilities_a = facilities.drop(columns=['geometry']).rename(columns={'geometry_refined': 'geometry'})

# Update the GeoDataFrame with the new geometry column
fac_gpd = gpd.GeoDataFrame(facilities_a, geometry='geometry', crs='epsg:4326')

# %%
# Download the drivable road network for the Greater Accra Region to use for routing
acc_roads = ox.graph_from_place(place_name, network_type="drive")

# %%
# Reproject the road network and facilities to EPSG:32630 (UTM Zone 30N)
acc_roads_proj = ox.project_graph(acc_roads, to_crs="epsg:32630")
fac_gpd_proj = fac_gpd.to_crs("epsg:32630")

# %%
def add_speeds_and_travel_times(graph):
    """
    Add edge speeds and travel times to a graph.

    Parameters:
    graph (networkx.MultiDiGraph): The input graph

    Returns:
    networkx.MultiDiGraph: Graph with added speed and travel time attributes
    """
    # Calculate and add missing edge speeds based on street types
    graph_with_speeds = ox.add_edge_speeds(graph)

    # Calculate travel times for each road segment based on length and speed
    graph_with_times = ox.add_edge_travel_times(graph_with_speeds)

    return graph_with_times

# Apply the function to add speeds and travel times to the road network
roads_s_t = add_speeds_and_travel_times(acc_roads_proj)

# %%
# Map each hospital point to the nearest node on the drivable road network
# This allows us to use the road graph for travel time analysis starting from the hospital
fac_gpd_proj["nearest_node"] = fac_gpd_proj.apply(
    lambda row: ox.nearest_nodes(roads_s_t, X=row.geometry.x, Y=row.geometry.y),
    axis=1
)

# %%
# Writing a function to create isochrone polygons of each facility data point.
def make_isochrone(G, center_node, time_limit, buffer_dist=100):

    subgraph = nx.ego_graph(
        G,
        center_node,
        radius=time_limit,
        distance="travel_time"
    )

    nodes_gdf, edges_gdf = ox.graph_to_gdfs(subgraph)

    iso_poly = edges_gdf.buffer(buffer_dist).union_all()

    return iso_poly

# %%
all_isochrones_data = []

# Iterate through all hospitals to calculate their catchment areas
for idx, hospital_row in fac_gpd_proj.iterrows():
    facility_node = hospital_row["nearest_node"]
    facility_name = hospital_row.get('name', f'Facility {idx}')

    # Generate a polygon representing areas reachable within 8 minutes (480 seconds)
    iso_8 = make_isochrone(roads_s_t, facility_node, 480)

    # Store the result if a valid isochrone was created
    if iso_8:
        all_isochrones_data.append({"facility_name": facility_name, "time": "8 min", "geometry": iso_8})

# %%
# Create a single GeoDataFrame from all collected isochrone data
iso_poly = gpd.GeoDataFrame(all_isochrones_data, crs='epsg:32630')

# %%
# Fetch Ghana Population raster
pop_data = wp_raster(product_name='pop_g1_unadj',
                     aoi=['GHA'],
                     years=[2020])

# %%
try:
    gdf_accra = ox.geocode_to_gdf(place_name)
    print(f"Successfully retrieved boundary for {place_name}")
    gdf_accra
except Exception as e:
    print(f"An error occurred while fetching the boundary for {place_name}: {e}")

# %%
# Reproject the Accra boundary and population data to EPSG:32630
boundary_accra_proj = gdf_accra.to_crs("epsg:32630")
Ghana_pop = pop_data.rio.reproject("epsg:32630")

# %%
# Clip the population raster to the Accra boundary
accra_pop = Ghana_pop.rio.clip(boundary_accra_proj.geometry, boundary_accra_proj.crs)

# %%
# Dissolve all isochrones into a single polygon
isochrone_poly = iso_poly.dissolve()

# %%
# Clip the population raster to the dissolved isochrone polygon
pop_within_isochrone = accra_pop.rio.clip(isochrone_poly.geometry, isochrone_poly.crs)

# %%
# Clip the population raster to the area outside the dissolved isochrone polygon
pop_outside_isochrone = accra_pop.rio.clip(isochrone_poly.geometry, isochrone_poly.crs, invert=True)

# %%
# Calculate total population within the entire Accra area
total_accra_pop = accra_pop.sum().values.item()

# Calculate total population within the isochrone (reachable areas)
total_pop_within_isochrone = pop_within_isochrone.sum().values.item()

# Calculate total population outside the isochrone (non-reachable areas)
total_pop_outside_isochrone = pop_outside_isochrone.sum().values.item()

# Display the results
print(f"Total population in Accra: {total_accra_pop:,.0f}")
print(f"Population within 8-minute reach: {total_pop_within_isochrone:,.0f}")
print(f"Population outside 8-minute reach: {total_pop_outside_isochrone:,.0f}")

# %%
total = total_pop_outside_isochrone + total_pop_within_isochrone
total