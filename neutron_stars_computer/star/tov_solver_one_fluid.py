import functools
import numpy as np
from scipy.integrate import solve_ivp
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

from . import conversionfactors as cf
from ..equationsofstate.eos import EquationOfState

Array = np.ndarray
Event = Callable[[float, Array], float]


@dataclass(slots=True)
class TOVInputOneFluid:
    """Dataclass that contains all necessary inputs to solve one-fluid TOV eqs."""

    eos: EquationOfState
    MIN_RADIUS: float = 1e-6
    MAX_RADIUS: float = 1e5
    RELATIVE_TOLERANCE: float = 1e-6
    ABSOLUTE_TOLERANCE: list[float] = field(default_factory=lambda: [1e-4, 1e-15])
    events: Iterable[Event] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.MIN_RADIUS <= 0.0:
            raise ValueError(
                "Minimum radius has to be larger than zero "
                + "to integrate TOV equations."
            )
        if self.MAX_RADIUS <= self.MIN_RADIUS:
            raise ValueError("Maximum radius has to be larger than minimum radius.")


def solve_one_fluid_tov(tov_input_one_fluid: TOVInputOneFluid, central_mass: float, central_pressure: float) -> Any:
    """Solves the one-fluid TOV equations for a given central pressure, central mass and EOS.
    Returns a bunch object, see solve_ivp documentation for more details."""

    if central_pressure <= 0:
        raise ValueError("Central pressure has to be a larger than zero.")


    def boundary_event(r: float, y: Array) -> float:
        """Defines the boundary of the star by reaching p(r=R) = 0."""
        return y[1]


    boundary_event.terminal = True
    boundary_event.direction = -1

    initial_integration_vector = (central_mass, central_pressure)

    def one_fluid_tov_equations(r: float, y: Array) -> tuple[float, float]:
        """TOV equations. System of differential equations for pressure and mass.
        ------------------------------
        Units:
        -------
        r: radius in km.
        p, e: pressure and energy density in MeV/fm^3.
        m: mass in km.
        """

        m, p = y
        e: float = tov_input_one_fluid.eos.energy_density_from(pressure=p)

        dvdr: float = time_metric_fn_derivative(r, p, m)
        dmdr: float = mass_derivative(r, e)
        dpdr: float = pressure_derivative(e, p, dvdr)

        return (dmdr, dpdr)

    one_fluid_tov_integration: Any = solve_ivp(
        one_fluid_tov_equations,
        (tov_input_one_fluid.MIN_RADIUS, tov_input_one_fluid.MAX_RADIUS),
        initial_integration_vector,
        method="DOP853",
        dense_output=True,
        rtol=tov_input_one_fluid.RELATIVE_TOLERANCE,
        atol=tov_input_one_fluid.ABSOLUTE_TOLERANCE,
        events=(boundary_event, *tov_input_one_fluid.events),
    )

    def check_integration_validity(success: bool, status: int) -> None:
        if not success:
            raise TOVIntegrationError(
                "The integration of the TOV eqs. was not successfull..."
            )

        if status != 1:
            raise BoundaryNotFoundError(
                "The integration was successfull, "
                + "but the star's boundary was not reached. "
                + "Perhaps your TOVInputOneFluid.MAXRADIUS is too small?"
            )

    check_integration_validity(one_fluid_tov_integration.success, one_fluid_tov_integration.status)

    return one_fluid_tov_integration


@functools.lru_cache
def time_metric_fn_derivative(r: float, p: float, m: float) -> float:
    exp_lambda: float = np.exp(-2 * radial_metric_fn(r, m))
    return (4 * np.pi * r * p * cf.MEV_FM3_TO_KM_2 + m / r**2) / exp_lambda


@functools.lru_cache
def mass_derivative(r: float, e: float) -> float:
    return 4.0 * np.pi * r**2.0 * e * cf.MEV_FM3_TO_KM_2


@functools.lru_cache
def pressure_derivative(e: float, p: float, dvdr: float) -> float:
    return -(e + p) * dvdr


@functools.lru_cache
def radial_metric_fn(radius: float, mass: float) -> float:
    return -np.log(1 - 2 * mass / radius) / 2


class TOVIntegrationError(Exception):
    pass


class BoundaryNotFoundError(Exception):
    pass
