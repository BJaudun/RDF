
from helpers import _converge_interval, _linear_points,_values_range

class RDF:

    # Initialises the class
    # parameters
    #     wavefunction: the wave function to use ,
    #     start : start of the range (min x)
    #     end   : end of the range (max x)
    def __init__(self, function, start, end):
        self.function = function
        self.start = start
        self.end = end

    # Compute the normalised y values such that area under the curve is 1.
    # The integral is computed using an increasing number of intervals until the difference
    # between the current value and the previous falls below the specified converge threshold.
    # Parameters
    #     integration_method:   integration method, must be 'mid' or 'trap'
    #     convergence_threshold: value below which the integral is considered to have converged
    #     initial_intervals: initial number of intervals
    #     interval_increment: number of intervals to add when refining the
    # Return {normalised y-values, normalisation factor, x-values, number of intervals}
    def normalise_area(self, integration_method, convergence_threshold, initial_intervals, interval_increment):
        area, x_values, y_values, intervals = _converge_interval(self.start,self.end,self.function,integration_method, convergence_threshold, initial_intervals, interval_increment)
        norm_y_values = []
        normalization_factor = 1 / area
        for y in y_values:
            norm_y_values.append(y * normalization_factor)
        return norm_y_values, normalization_factor, x_values, intervals

    # Computes normalised y values such that their maximum individual value is 1.
    # Parameters:
    #     intervals: number of intervals (this will result in `intervals + 1` values)
    # Return {normalised y-values, normalisation factor, x-values}
    def normalise_height(self, intervals):
        x_values = _linear_points(self.start,self.end,intervals)
        y_values = _values_range(self.function, x_values)
        norm_y_values = []
        normalization_factor = 1 / max(y_values)
        for i in y_values:
            norm_y_values.append(i * normalization_factor)
        return norm_y_values, normalization_factor, x_values