import xarray as xr
import numpy as np
from ...algorithm_class import Algorithm
from ...unit_handling import Unitfull, ureg

from .fusion_rates import calc_fusion_power


@Algorithm.register_algorithm(return_keys=["heavier_fuel_species_fraction"])
def require_P_fusion_less_than_P_fusion_limit(
    P_fusion_upper_limit: Unitfull, 
    P_fusion: Unitfull,
    heavier_fuel_species_fraction: float,
) -> tuple[Unitfull, ...]:
    """ Change heavier_fuel_species_fraction to reduce P_fusion to P_fusion_limit

    Args: 
        P_fusion_limit: :term:`glossary link<P_fusion_limit>`
        P_fusion: :term:`glossary link<P_fusion>`
        heavier_fuel_species_fraction: :term:`glossary link<heavier_fuel_species_fraction>`

    Returns:
        :term:`heavier_fuel_species_fraction`
    """
    # If P_fusion is already below the limit, return the current heavier_fuel_species_fraction
    if P_fusion <= P_fusion_upper_limit:
        return heavier_fuel_species_fraction
    
    # If P_fusion is above the limit, reduce (take lower root) heavier_fuel_species_fraction until P_fusion is below the limit
    else: 
        new_heavier_fuel_species_fraction = 1 - np.sqrt(1 - P_fusion_upper_limit / P_fusion * heavier_fuel_species_fraction * (1 - heavier_fuel_species_fraction))
        return new_heavier_fuel_species_fraction