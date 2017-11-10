# -*- coding: utf-8 -*-
'''
Created on Jul 5, 2017

@author: Robin
'''
import prime, polynomial

def secret_int_to_points(secret_int, point_threshold, num_points):
    """ Split a secret (integer) into shares (pair of integers / x,y coords).

        Sample the points of a random polynomial with the y intercept equal to
        the secret int.
    """
    if point_threshold < 2:
        raise ValueError("Threshold must be >= 2.")
    if point_threshold > num_points:
        raise ValueError("Threshold must be < the total number of points.")
    prime_num = prime.get_large_enough_prime([secret_int, num_points])
    if not prime_num:
        raise ValueError("Error! Secret is too long for share calculation!")
    coefficients = polynomial.random_polynomial(point_threshold-1, secret_int, prime_num)
    points = polynomial.get_polynomial_points(coefficients, num_points, prime_num)
    return (points, prime_num, coefficients)  

def points_to_secret_int(points):
    """ Join int points into a secret int.

        Get the intercept of a random polynomial defined by the given points.
    """
    if not isinstance(points, list):
        raise ValueError("Points must be in list form.")
    for point in points:
        if not isinstance(point, tuple) and len(point) == 2:
            raise ValueError("Each point must be a tuple of two values.")
        if not isinstance(point[0], (int, long)) and \
            isinstance(point[1], (int, long)):
            raise ValueError("Each value in the point must be an int.")
    x_values, y_values = zip(*points)
    prime_num = prime.get_large_enough_prime(y_values)
    free_coefficient = polynomial.modular_lagrange_interpolation(0, points, prime_num)
    secret_int = free_coefficient # the secret int is the free coefficient
    return secret_int