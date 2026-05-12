from dataclasses import asdict
from typing import Any, Iterable, Protocol
from concurrent.futures import ProcessPoolExecutor

import pandas as pd


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
