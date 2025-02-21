import numpy as np

def is_close_to_multiple(value, base, tol=np.pi/10):
    """
    Check if `value` is close to any multiple of `base` within a given tolerance.

    Parameters:
    - value: The number to check.
    - base: The base value whose multiples we consider.
    - tol: Tolerance for closeness (default: 1e-5).

    Returns:
    - The closest multiple if within tolerance, else None.
    """
    multiple = np.round(value / base)  # Find the nearest multiple
    closest = multiple * base  # Compute the corresponding value
    return closest if np.isclose(value, closest, atol=tol) else None