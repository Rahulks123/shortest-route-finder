import os
import openrouteservice
import folium

def init_client():
    api_key = os.getenv("ORS_API_KEY")  # get API key from env variable
    if not api_key:
        raise ValueError("No OpenRouteService API key found. Set ORS_API_KEY environment variable.")
    return openrouteservice.Client(key=api_key)

# rest of your code...

def get_route(client, coords):
    try:
        return client.directions(coords, profile='driving-car', format='geojson')
    except Exception as e:
        print("Error getting route:", e)
        return None

def create_map(route, coords, map_file='map.html'):
    # Center map between start and end points
    center_lat = (coords[0][1] + coords[1][1]) / 2
    center_lon = (coords[0][0] + coords[1][0]) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    
    if route:
        folium.GeoJson(route).add_to(m)
        folium.Marker(location=[coords[0][1], coords[0][0]], popup='Start').add_to(m)
        folium.Marker(location=[coords[1][1], coords[1][0]], popup='End').add_to(m)
    
    m.save(f'static/{map_file}')  # Save inside static folder
    return map_file  # Return just filename (not path)
