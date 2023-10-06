def move_to_point(center_lat, center_lon, lat, lon):
    new_lon = lon + center_lon
    new_lat = lat + center_lat
    return new_lon, new_lat