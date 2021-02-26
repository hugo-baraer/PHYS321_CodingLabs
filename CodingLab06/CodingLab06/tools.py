import numpy as np

def square(arr):
    return arr**2

def get_pi():
    return np.pi

def picky(num):
    if not isinstance(num, (np.float, float, np.int, int)):
        raise TypeError("Must input a number")
