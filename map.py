# This function will take a state and its alerts, and generate a map
def map_gen(state, alerts):
    # Import necessary libraires/classes/functions
    import folium
    import geopandas as gpd
    from shapely.geometry import Polygon, MultiPolygon
    from main import get_coords
    # A dictionary of the coordinates of the center of each state, zoom
    state_center = {'OR':[[43.9336, -120.5583],7],
                    'WA':[[47.3826, -120.4472],7],
                    'ID':[[45.6, -114.6130],6],
                    'AK':[[63.5888, -154.4931],4]}
    # Color scheme to use for severity
    color_map = {'Moderate':'#00008b',
                 'Severe':'#FFA500',
                 'Extreme':'#8B0000'}
    color_map2 = {'Moderate':'darkblue',
                 'Severe':'orange',
                 'Extreme':'darkred'}
    
    coords = state_center[state][0]
    zoom = state_center[state][1]
    # Initiate a map
    map = folium.Map(location=coords,
                     zoom_start=zoom)
    # Parse each alert
    if alerts:
        for alert in alerts:
            # Pull out necessary info
            zones = alert['zones'].split(';')
            severity = alert['severity']
            headline = alert['headline']
            # For each zone, get coordinates and generate a polygon shape
            for zone_api in zones:
                typ, zone_coords = get_coords(zone_api)
                try: 
                    if typ == 'Polygon':
                        polygon_geom = Polygon(zone_coords[0])
                    elif typ == 'MultiPolygon':
                        polygon_geom = MultiPolygon(zone_coords)
                    else:
                        continue
                    centr = polygon_geom.centroid
                    centr = [centr.y, centr.x]
                    polygon = gpd.GeoDataFrame(index=[0],
                                            crs='epsg:4326', 
                                            geometry=[polygon_geom])
                    # Add shape to the map based on color assigned to alert severity
                    folium.GeoJson(polygon, style={'fillColor':color_map[severity],
                                                   'color':color_map[severity]}).add_to(map)
                    # Add a marker of the same color as well with headline info
                    folium.Marker(location=centr,
                                crs='epsg:4326', 
                                popup=severity+":"+headline,
                                icon=folium.Icon(color=color_map2[severity])
                                ).add_to(map)
                except:
                    pass
    return map

# This will run during testing, when this script is called directly
if __name__ == '__main__':
    map_gen('OR')