"""
Robotic Package Sorting System for Thoughtful AI

This module implements a robotic arm function that sorts packages into different stacks
based on their volume, dimensions, and mass according to specific criteria.
"""


def sort(width: float, height: float, length: float, mass: float) -> str:
    """
    Sort packages into appropriate stacks based on size and weight criteria.
    
    Args:
        width (float): Package width in centimeters
        height (float): Package height in centimeters  
        length (float): Package length in centimeters
        mass (float): Package mass in kilograms
        
    Returns:
        str: The stack name where the package should be dispatched:
            - "STANDARD": Normal packages that are neither bulky nor heavy
            - "SPECIAL": Packages that are either bulky or heavy (but not both)
            - "REJECTED": Packages that are both bulky and heavy
            
    Raises:
        ValueError: If any input parameter is negative or invalid
        
    Examples:
        >>> sort(50, 50, 50, 10)
        'STANDARD'
        >>> sort(200, 100, 100, 15)
        'SPECIAL'
        >>> sort(100, 100, 100, 25)
        'SPECIAL'
        >>> sort(200, 200, 200, 25)
        'REJECTED'
    """
    # Input validation
    if not all(isinstance(param, (int, float)) for param in [width, height, length, mass]):
        raise ValueError("All parameters must be numbers")
    
    if any(param < 0 for param in [width, height, length, mass]):
        raise ValueError("All parameters must be non-negative")
    
    # Calculate volume in cm³
    volume = width * height * length
    
    # Determine if package is bulky
    # Bulky if volume >= 1,000,000 cm³ OR any dimension >= 150 cm
    is_bulky = volume >= 1_000_000 or any(dim >= 150 for dim in [width, height, length])
    
    # Determine if package is heavy
    # Heavy if mass >= 20 kg
    is_heavy = mass >= 20
    
    # Sort according to rules:
    # STANDARD: neither bulky nor heavy
    # SPECIAL: either bulky or heavy (but not both)
    # REJECTED: both bulky and heavy
    if is_bulky and is_heavy:
        return "REJECTED"
    elif is_bulky or is_heavy:
        return "SPECIAL"
    else:
        return "STANDARD"


def get_package_info(width: float, height: float, length: float, mass: float) -> dict:
    """
    Get detailed information about a package's classification.
    
    Args:
        width (float): Package width in centimeters
        height (float): Package height in centimeters
        length (float): Package length in centimeters
        mass (float): Package mass in kilograms
        
    Returns:
        dict: Dictionary containing package details and classification
    """
    volume = width * height * length
    
    return {
        "dimensions": {"width": width, "height": height, "length": length},
        "volume_cm3": volume,
        "mass_kg": mass,
        "is_bulky": volume >= 1_000_000 or any(dim >= 150 for dim in [width, height, length]),
        "is_heavy": mass >= 20,
        "stack": sort(width, height, length, mass)
    }
