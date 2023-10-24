import numpy as np

def q_mult(q1, q2):
    out_quat = Quaternion()
    out_quat.w = q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z
    out_quat.x = q1.w * q2.x + q1.x * q2.w + q1.y * q2.z - q1.z * q2.y
    out_quat.y = q1.w * q2.y + q1.y * q2.w + q1.z * q2.x - q1.z * q2.z
    out_quat.z = q1.w * q2.z + q1.z * q2.w + q1.x * q2.y - q1.y * q2.x
    return out_quat

def q_point_mult(q1, p1):
    out_quat = Quaternion()
    point_quaternion = Quaternion()
    point_quaternion.x = p1.x
    point_quaternion.y = p1.y
    point_quaternion.z = p1.z
    point_quaternion.w = 0.0
    out_quat = q_mult(q_mult(q1, point_quaternion), q1.conjugate())
    return out_quat

def axis_angle_to_quat(point, theta):
    out_quat = Quaternion()
    point.normalize()
    theta /= 2.0
    out_quat.w = np.cos(theta)
    out_quat.x = point.x * np.sin(theta)
    out_quat.y = point.y * np.sin(theta)
    out_quat.z = point.z * np.sin(theta)
    return out_quat

def quaternion_to_axisangle(q):
    theta = np.arccos(q.w) * 2.0

class Quaternion:
    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def normalize(self):
        mag_squared= (self.w**2.0 + self.x**2.0 + self.y**2.0 + self.z**2.0)
        if abs(mag_squared - 1.0) > 0.00001:
            mag = np.sqrt(mag_squared)
            self.w = self.w / mag
            self.x = self.x / mag
            self.y = self.y / mag
            self.z = self.z / mag

    def conjugate(self):
        out_quat = Quaternion()
        out_quat.w = self.w
        out_quat.x = -self.x
        out_quat.y = -self.y
        out_quat.z = -self.z
        return out_quat