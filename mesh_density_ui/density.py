import numpy as np

# Example density function, returns the value of the function described in
#  Ringler, T. D., D. Jacobsen, M. Gunzburger, L. Ju, M. Duda, and W. Skamarock, 2011. “Exploring a
# Multiresolution Modeling Approach within the Shallow-Water Equations”. Mon. Wea. Rev., 139, 3348
# – 3368.
def get_density(x, y):
    minimum_density = (1.0/15.0)**4
    half_width_high_resolution = 0.0350
    transition_zone_width = 0.10944
    coefficient = (1 - minimum_density) / 2
    to_calculate = (half_width_high_resolution - np.sqrt((x * x) + (y * y))) / transition_zone_width
    return coefficient * (np.tanh(to_calculate) + 1) + minimum_density