import neutron_stars_computer.star.conversionfactors as cf

from dataclasses import asdict
from typing import Any, Iterable, Protocol
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import pandas as pd
import numpy as np


class Factory(Protocol):
    def create_two_fluid_star(self, central_pressure_1: float, central_pressure_2: float) -> Any:
        """Creates an admixedstar star."""


def create_two_fluid_stellar_family(
    fac: Factory, central_pressures_1: Iterable[float], central_pressures_2: Iterable[float]
) -> pd.DataFrame:
    """Creates a list of two-fluid stars from two EOS and
    two arrays of central pressures."""
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(fac.create_two_fluid_star, cp1, cp2) for cp1, cp2 in zip(central_pressures_1, central_pressures_2)]

    two_fluid_stars = pd.concat([pd.DataFrame(asdict(f.result()), index=[0]) for f in futures])
    two_fluid_stars.reset_index(drop=True, inplace=True)
    two_fluid_stars.dropna(axis=1, inplace=True)

    return two_fluid_stars


def create_stars_with_fixed_DM(central_pressures_BM: Iterable[float], chi: float,
    fac: Factory, cp_DM_L: float, cp_DM_R: float) -> None:

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(find_star, chi, fac, cp_BM, cp_DM_L, cp_DM_R) for cp_BM in central_pressures_BM]


    fixed_DM_star = pd.concat([f.result() for f in futures])
    fixed_DM_star.reset_index(drop=True, inplace=True)

    fixed_DM_star['total_mass'] = fixed_DM_star['mass_1'] + fixed_DM_star['mass_2']
    fixed_DM_star['radius'] = np.maximum(fixed_DM_star['radius_1'], fixed_DM_star['radius_2'])

    return fixed_DM_star


def find_star(chi_target: float, fac: Factory, cp_BM: float, cp_DM_L: float, cp_DM_R: float) -> pd.DataFrame:

    cp_BM_arr = np.array([cp_BM])

    while True:
            cp_DM_M = (cp_DM_L + cp_DM_R) / 2
            central_pressures_DM = np.array([cp_DM_M])

            two_fluid_stars: pd.DataFrame = create_two_fluid_stellar_family(fac, central_pressures_DM, cp_BM_arr)

            two_fluid_stars["mass_1"] = two_fluid_stars["mass_1"] / cf.M_SUN_IN_KM
            two_fluid_stars["mass_2"] = two_fluid_stars["mass_2"] / cf.M_SUN_IN_KM

            chi_M = two_fluid_stars["mass_1"].values[0] / (two_fluid_stars["mass_1"].values[0] + two_fluid_stars["mass_2"].values[0])

            if abs(chi_M - chi_target) < 1e-5:
                return two_fluid_stars

            if abs(cp_DM_R - cp_DM_M) < 1e-5:
                return None

            if chi_M < chi_target:
                cp_DM_L = cp_DM_M

            else:
                cp_DM_R = cp_DM_M