import unittest
from mesh_density_ui.point import Point

class TestPointSetters(unittest.TestCase):
    def test_default_constructor(self):
        test_point = Point()
        self.assertEqual(test_point.lat, 0.0)
        self.assertEqual(test_point.lon, 0.0)


    def test_setting_from_cart(self):
        test_point = Point()
        test_point.set_from_cart(0,0,0)
        self.assertAlmostEqual(test_point.lat, 0.0)
        self.assertAlmostEqual(test_point.lon, 0.0)

    def test_setting_from_lat_lon(self):
        test_point = Point()
        test_point.set_from_lat_lon(0.0, 0.0)
        self.assertAlmostEqual(test_point.x, 6371.4)
        self.assertAlmostEqual(test_point.y, 0.0)
        self.assertAlmostEqual(test_point.z, 0.0)

class TestPointRotations(unittest.TestCase):

    def test_no_rotation(self):
        test_point = Point(0.0, 0.0)
        prior_lat = test_point.lat
        prior_lon = test_point.lon
        test_point.rotate_about_point(100, test_point)
        self.assertAlmostEqual(prior_lat, test_point.lat)
        self.assertAlmostEqual(prior_lon, test_point.lon)
        self.assertAlmostEqual(test_point.x, 6371.4)
        self.assertAlmostEqual(test_point.y, 0.0)
        self.assertAlmostEqual(test_point.z, 0.0)

        rotation_point = Point()
        rotation_point.set_from_cart(0.0, 0.0, 1.0)
        test_point.rotate_about_point(0.0, rotation_point)
        self.assertAlmostEqual(prior_lat, test_point.lat)
        self.assertAlmostEqual(prior_lon, test_point.lon)
        self.assertAlmostEqual(test_point.x, 6371.4)
        self.assertAlmostEqual(test_point.y, 0.0)
        self.assertAlmostEqual(test_point.z, 0.0)

    
    def test_90_deg_rotation(self):
        test_point = Point(0.0, 0.0)
        self.assertAlmostEqual(test_point.x, test_point.r)
        self.assertAlmostEqual(test_point.y, 0.0)
        self.assertAlmostEqual(test_point.z, 0.0)
        z_axis_point = Point()
        z_axis_point.set_from_cart(0.0, 0.0, 1.0)
        test_point.rotate_about_point(90, z_axis_point)
        self.assertAlmostEqual(test_point.lat, 0.0)
        self.assertAlmostEqual(test_point.lon, 90.0)


