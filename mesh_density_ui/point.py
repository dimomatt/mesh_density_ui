import numpy as np

def cross_product(a, b, normalize=False):
    point = Point()
    point.x = a.y * b.z - a.z * b.y
    point.y = -(a.x * b.z - a.z * b.x)
    point.z = a.x * b.y - a.y * b.x

    if (normalize):
        point.normalize()
    point.convert_to_lat_lon()

    return point

class Point:
    def __init__(self, lat=0.0, lon=0.0, radius=6371.4):
        self.lat = lat
        self.lon = lon
        self.r = radius
        self.convert_to_cart()
    
    def convert_to_lat_lon(self):
        self.lat = np.rad2deg(np.arcsin(self.z / self.r))
        self.lon = np.rad2deg(np.arctan2(self.y, self.x))

    def convert_to_cart(self):
        lat_radians = np.deg2rad(self.lat)
        lon_radians = np.deg2rad(self.lon)
        self.x = self.r * np.cos(lat_radians) * np.cos(lon_radians)
        self.y = self.r * np.cos(lat_radians) * np.sin(lon_radians)
        self.z = self.r * np.sin(lat_radians)

    def set_from_cart(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.convert_to_lat_lon()

    def set_from_lat_lon(self, lat, lon, radius=6371.4):
        self.lat = lat
        self.lon = lon
        self.r = radius
        self.convert_to_cart()
    
    #
    #def rotate_about_vector(self, theta, a, b, c, u, v, w):
    #    vw2 = v ** 2 + w ** 2
    #    uw2 = u ** 2 + w ** 2
    #    uv2 = u ** 2 + v ** 2

    #    self.x = (a*vw2 - u*(b*v+c*w-u*self.x-v*self.y-w*self.z))*(1-np.cos(theta)) + self.x*np.cos(theta) + (-c*v+b*w-w*self.y+v*self.z)*np.sin(theta)
    #    self.y = (b*uw2 - v*(a*u+c*w-u*self.x-v*self.y-w*self.z))*(1-np.cos(theta)) + self.y*np.cos(theta) + ( c*u-a*w+w*self.x-u*self.z)*np.sin(theta)
    #    self.z = (c*uv2 - w*(a*u+b*v-u*self.x-v*self.y-w*self.z))*(1-np.cos(theta)) + self.z*np.cos(theta) + (-b*u+a*v-v*self.x+u*self.y)*np.sin(theta)
    #    self.convert_to_lat_lon()

    def rotate_about_vector(self, theta, a, b, c, u, v, w):
        x = self.x
        y = self.y
        z = self.z

        vw2 = v ** 2 + w ** 2
        uw2 = u ** 2 + w ** 2
        uv2 = u ** 2 + v ** 2

        m = np.sqrt(u**2.0 + v**2.0 + w**2.0)
        
        self.x = (a*vw2 + u*(-b*v-c*w+u*x+v*y+w*z) + ((x-a)*vw2+u*(b*v+c*w-v*y-w*z))*np.cos(theta) + m*(-c*v+b*w-w*y+v*z)*np.sin(theta))/m**2.0
        self.y = (b*uw2 + v*(-a*u-c*w+u*x+v*y+w*z) + ((y-b)*uw2+v*(a*u+c*w-u*x-w*z))*np.cos(theta) + m*( c*u-a*w+w*x-u*z)*np.sin(theta))/m**2.0
        self.z = (c*uv2 + w*(-a*u-b*v+u*x+v*y+w*z) + ((z-c)*uv2+w*(a*u+b*v-u*x-v*y))*np.cos(theta) + m*(-b*u+a*v-v*x+u*y)*np.sin(theta))/m**2.0
        self.convert_to_lat_lon()


    # Rotate about the vector from the origin to the point by theta radians
    def rotate_about_point(self, theta, point):
        self.rotate_about_vector(theta, 0.0, 0.0, 0.0, point.x, point.y, point.z)

    def normalize(self):
        mag = np.sqrt(self.x**2 + self.y**2 + self.z**2)
        self.x /= mag
        self.y /= mag
        self.z /= mag

    def distance_from_origin(self):
        return (np.sqrt(self.x**2 + self.y**2 + self.z**2))