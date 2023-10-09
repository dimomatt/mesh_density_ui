import argparse
import configparser
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
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

    # Get grid
    x = np.linspace(-180, 180, int(config.get('MAP','latitude_cells')))
    y = np.linspace(-90, 90, int(config.get('MAP','longitude_cells')))
    x, y = np.meshgrid(x, y)

    # setup numpy vectorization
    get_density_vectorized = np.vectorize(get_density)
    get_resolution_vectorized = np.vectorize(get_resolution)
    density = get_density_vectorized(x, y)
    density = get_resolution_vectorized(density)

    # Transform center points
    center_latitude = float(config['GEO']['center_latitude'])
    center_longitude = float(config['GEO']['center_longitude'])
    x, y = move_to_point(center_latitude, center_longitude, x, y)

    # create plot with plate carree projection
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    contour_plot = ax.contour(x, y, density, levels)
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