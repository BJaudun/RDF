import numpy as np


# Compute an integral using an increasing number of intervals until the difference
# between the current value and the previous falls below a specified converge threshold.
# Parameters
#     integral_method:   integration method, must be 'mid' or 'trap'
#     convergence_threshold: value below which the integral is considered to have converged
#     initial_intervals: initial number of intervals
#     interval_increment: number of intervals to add when refining the integral value
# Return {area under the curve, x-values, y-values, number of intervals}
def _converge_interval(start,end,function,integral_method, converge_threshold, initial_intervals, interval_change):
    area_prev, x_values, y_values = _integrate(start,end,function,integral_method, initial_intervals)
    intervals = initial_intervals
    epsilon = converge_threshold * 2
    while epsilon > converge_threshold:
        intervals += interval_change
        area_current, x_values, y_values = _integrate(start,end,function,integral_method, intervals)
        epsilon = abs(area_current - area_prev)
        area_prev = area_current
    return area_current, x_values, y_values, intervals


# Computes the integral using the specified method
# Parameters:
#   method: the method of integration 'mid' or 'trap'
#   intervals: the number of intervals to use
# Returns { integral value (area under the curve), x-values, y-values}
def _integrate(start,end,function, integral_method, intervals):
    length = (end - start) / intervals
    if integral_method == 'mid':
        x_values = _mid_points(start,end,intervals)
        y_values = _values_range(function, x_values)
        integral = length * (sum(y_values))
        return integral, x_values, y_values
    elif integral_method == 'trap':
        x_values = _linear_points(start,end,intervals)
        y_values = _values_range(function,x_values)
        integral = length * (1 / 2) * (2 * sum(y_values) - y_values[0] - y_values[-1])
        return integral, x_values, y_values
    else:
        raise Exception("Bad integration method, should be 'mid' or 'trap'.")


# Computes the RDF of the wave function at a given number of points
# Parameters:
#   x_values: x coordinates (radius) of the points to calculate
def _values_range(function, x_values):
    y_values = []
    for radius in x_values:
        four_pi_radius_squared = 4 * np.pi * (radius ** 2)
        y = four_pi_radius_squared * ((function(radius)) ** 2)
        y_values.append(y)
    return y_values

# Calculates the x-values for the mid-point rectangle integration method
# Parameters:
#   intervals: number of intervals (will result in `intervals` x-values)
# Returns {x-values}
def _mid_points(start,end,intervals):
    interval_length = (end - start) / intervals
    points = []
    x = start
    for i in range(intervals):
        points.append((x * 2 + interval_length) / 2)
        x = x + interval_length
    return points

# Calculates the x coordinates for Trapezoidal integration method
# Parameters:
#   intervals: number of intervals (will result in `intervals + 1` x-values)
# Returns {x-values}
def _linear_points(start,end,intervals):
    interval_length = (end - start) / intervals
    points = []
    for i in range(intervals + 1):
        points.append(start + interval_length * i)
    return points