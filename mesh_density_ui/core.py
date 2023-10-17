import argparse
import configparser
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from point import Point, cross_product
from density import get_density
from helpers import move_to_point, get_resolution

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument( 
        "-c", "--config",
        dest="configFilepath",
        help="Path to configuration file",
        type=str,
        default="../config.ini"
    )
    args = parser.parse_args()
    return args

def fmt(x):
    string = f"{x:.1f}"
    if string.endswith("0"):
        string = f"{x:.0f}"
    return f"{string} km"

def main(config):
    levels = config.getlist('CONFIG', 'levels')
    birdseye_rotation_rad = np.deg2rad(float(config.get('GEO', 'ccw_rotation_deg')))
    initial_lat_rad = np.deg2rad(float(config.get('GEO', 'initial_center_latitude')))
    initial_lon_rad = np.deg2rad(float(config.get('GEO', 'initial_center_longitude')))
    new_lat_rad = np.deg2rad(float(config.get('GEO', 'new_center_latitude')))
    new_lon_rad = np.deg2rad(float(config.get('GEO', 'new_center_longitude')))

    # Get grid
    lats = np.linspace(-90, 90, int(config.get('MAP','latitude_cells')))
    lons = np.linspace(-180, 180, int(config.get('MAP','longitude_cells')))
    points = [Point(lat, lon) for lat, lon in zip(lats, lons)]
    lats, lons = np.meshgrid(lats, lons)

    # setup numpy vectorization
    get_density_vectorized = np.vectorize(get_density)
    get_resolution_vectorized = np.vectorize(get_resolution)
    density = get_density_vectorized(lats, lons)
    density = get_resolution_vectorized(density)

    # Transform center points
    d_lat =  new_lat_rad - initial_lat_rad
    d_lon =  new_lon_rad - initial_lon_rad
    d_birdseye = birdseye_rotation_rad
    
    z_axis_unit_vector = Point()
    z_axis_unit_vector.set_from_cart(0.0, 0.0, 1.0)

    original_long_point = Point()
    original_long_point.set_from_lat_lon(0.0, initial_lon_rad)
    original_long_point.normalize()

    cross_prod_vector = cross_product(z_axis_unit_vector, original_long_point, normalize=True)

    # latitude rotation
    for point in points:
        point.rotate_about_point(d_lon, z_axis_unit_vector)

        # Latitude rotation
        point.rotate_about_point(d_lat, cross_prod_vector)

        # Birdseye rotation
        point.rotate_about_point(d_birdseye, point)

    lats = [point.lat for point in points]
    lons = [point.lon for point in points]

    # create plot with plate carree projection
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    contour_plot = ax.contour(lons, lats, density, levels)
    ax.clabel(contour_plot,
              contour_plot.levels,
              inline=True,
              fmt=fmt)
    
    # Set globe, stock image, grid lines, and coastlines
    ax.set_global()
    ax.stock_img()
    ax.coastlines()
    ax.gridlines()

    plt.show()

if __name__ == '__main__':
    args = parse_args()
    config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    config.read(args.configFilepath)
    main(config)