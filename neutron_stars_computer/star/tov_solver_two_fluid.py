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
class TOVInputTwoFluid:
    """Dataclass that contains all necessary inputs to solve two-fluid TOV eqs."""

    eos1: EquationOfState
    eos2: EquationOfState
    MIN_RADIUS: float = 1e-6
    MAX_RADIUS: float = 1e5
    RELATIVE_TOLERANCE: float = 1e-6
    ABSOLUTE_TOLERANCE: list[float] = field(default_factory=lambda: [1e-4, 1e-4, 1e-15, 1e-15])
    events: Iterable[Event] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.MIN_RADIUS <= 0.0:
            raise ValueError(
                "Minimum radius has to be larger than zero "
                + "to integrate TOV equations."
            )
        if self.MAX_RADIUS <= self.MIN_RADIUS:
            raise ValueError("Maximum radius has to be larger than minimum radius.")


def solve_two_fluid_tov(tov_input_two_fluid: TOVInputTwoFluid, central_pressure_1: float, central_pressure_2: float) -> Any:
    """Solves the two-fluid TOV equations for two central pressures and two EOS.
    Returns a bunch object, see solve_ivp documentation for more details."""

    if central_pressure_1 <= 0 or central_pressure_2 <= 0:
        raise ValueError("Central pressures have to be larger than zero.")

    def compute_taylor_expansion_at_center() -> tuple[float, float, float]:
        """Taylor expansion near the stellar center (r ~ 0)."""
        r0: float = tov_input_two_fluid.MIN_RADIUS
        p0: float = central_pressure_1
        # v0: float = 0
        e0: float = tov_input_two_fluid.eos1.energy_density_from(pressure=p0)
        gamma0: float = tov_input_two_fluid.eos1.adiabatic_index_from(pressure=p0)

        v2: float = 8 * np.pi / 3 * (e0 + 3 * p0) * cf.MEV_FM3_TO_KM_2
        p2: float = -4 * np.pi / 3 * (e0 + p0) * (e0 + 3 * p0) * cf.MEV_FM3_TO_KM_2
        e2: float = p2 * (e0 + p0) / (gamma0 * p0)

        v4: float = (
            4 * np.pi / 5 * (e2 + 5 * p2)
            + 64 * np.pi**2 / 9 * e0 * (e0 + 3 * p0) * cf.MEV_FM3_TO_KM_2
        )
        v4 *= cf.MEV_FM3_TO_KM_2
        p4: float = -2 * np.pi / 5 * (e0 + p0) * (e2 + 5 * p2)
        p4 -= 2 * np.pi / 3 * (e2 + p2) * (p0 + 3 * p0)
        p4 -= 32 * np.pi**2 / 9 * e0 * (e0 + p0) * (e0 + 3 * p0) * cf.MEV_FM3_TO_KM_2
        p4 *= cf.MEV_FM3_TO_KM_2

        vc: float = 0.5 * v2 * r0**2 + 0.25 * v4 * r0**4  # + v0
        mc: float = 4 * np.pi * r0**3 * e0 / 3
        pc: float = p0 + 0.5 * p2 * r0**2 + 0.25 * p4 * r0**4
        # ec: float = e0 + 0.5*e2*r0**2

        return (vc, mc, pc)    

    def compute_taylor_expansion_at_center_2() -> tuple[float, float, float]:
        """Taylor expansion near the stellar center (r ~ 0)."""
        r0: float = tov_input_two_fluid.MIN_RADIUS
        p0: float = central_pressure_2
        # v0: float = 0
        e0: float = tov_input_two_fluid.eos2.energy_density_from(pressure=p0)
        gamma0: float = tov_input_two_fluid.eos2.adiabatic_index_from(pressure=p0)

        v2: float = 8 * np.pi / 3 * (e0 + 3 * p0) * cf.MEV_FM3_TO_KM_2
        p2: float = -4 * np.pi / 3 * (e0 + p0) * (e0 + 3 * p0) * cf.MEV_FM3_TO_KM_2
        e2: float = p2 * (e0 + p0) / (gamma0 * p0)

        v4: float = (
            4 * np.pi / 5 * (e2 + 5 * p2)
            + 64 * np.pi**2 / 9 * e0 * (e0 + 3 * p0) * cf.MEV_FM3_TO_KM_2
        )
        v4 *= cf.MEV_FM3_TO_KM_2
        p4: float = -2 * np.pi / 5 * (e0 + p0) * (e2 + 5 * p2)
        p4 -= 2 * np.pi / 3 * (e2 + p2) * (p0 + 3 * p0)
        p4 -= 32 * np.pi**2 / 9 * e0 * (e0 + p0) * (e0 + 3 * p0) * cf.MEV_FM3_TO_KM_2
        p4 *= cf.MEV_FM3_TO_KM_2

        vc: float = 0.5 * v2 * r0**2 + 0.25 * v4 * r0**4  # + v0
        mc: float = 4 * np.pi * r0**3 * e0 / 3
        pc: float = p0 + 0.5 * p2 * r0**2 + 0.25 * p4 * r0**4
        # ec: float = e0 + 0.5*e2*r0**2

        return (vc, mc, pc)     


    def core_event_1(r: float, y: Array) -> float:
        return y[2]

    core_event_1.terminal  = True
    core_event_1.direction = -1    

    def core_event_2(r: float, y: Array) -> float:
        return y[3]

    core_event_2.terminal  = True
    core_event_2.direction = -1

    #print(compute_taylor_expansion_at_center())
    #print(compute_taylor_expansion_at_center()[1])
    #print(compute_taylor_expansion_at_center()[2])
    
    initial_integration_vector = (0.0, 0.0, central_pressure_1, central_pressure_2)
    #initial_integration_vector = (compute_taylor_expansion_at_center()[1], compute_taylor_expansion_at_center_2()[1], 
    #                                compute_taylor_expansion_at_center()[2], compute_taylor_expansion_at_center_2()[2])

    def two_fluid_tov_equations(r: float, y: Array) -> tuple[float, float, float, float]:
        """TOV equations. System of differential equations for pressures and masses.
        ------------------------------
        Units:
        -------
        r: radius in km.
        p1, p2, e1, e2: pressures and energy densities in MeV/fm^3.
        m1, m2: masses in km.
        """

        m1, m2, p1, p2 = y
        e1: float = tov_input_two_fluid.eos1.energy_density_from(pressure=p1)
        e2: float = tov_input_two_fluid.eos2.energy_density_from(pressure=p2)

        p = p1 + p2 
        e = e1 + e2 
        m = m1 + m2

        dvdr: float = time_metric_fn_derivative(r, p, m)

        dm1dr: float = mass_derivative(r, e1)
        dm2dr: float = mass_derivative(r, e2)
        dp1dr: float = pressure_derivative(e1, p1, dvdr)
        dp2dr: float = pressure_derivative(e2, p2, dvdr)

        return (dm1dr, dm2dr, dp1dr, dp2dr)

    two_fluid_tov_integration: Any = solve_ivp(
        two_fluid_tov_equations,
        (tov_input_two_fluid.MIN_RADIUS, tov_input_two_fluid.MAX_RADIUS),
        initial_integration_vector,
        method="RK23",
        dense_output=True,
        rtol=tov_input_two_fluid.RELATIVE_TOLERANCE,
        atol=tov_input_two_fluid.ABSOLUTE_TOLERANCE,
        events=(core_event_1, core_event_2, *tov_input_two_fluid.events),
    )

    #print(tov_integration.t.size)
    #print(tov_integration.t)
    #print(tov_integration.y)
    #print(two_fluid_tov_integration.t_events)
    #print(two_fluid_tov_integration.y_events)
    #print(tov_integration.status)
    #print(tov_integration.message)
    #print(tov_integration)

    def check_integration_validity(success: bool, status: int) -> None:
        if not success:
            raise TwoFluidTOVIntegrationError(
                "The integration of the two-fluid TOV eqs. was not successfull..."
            )

        if status != 1:
            raise BoundaryNotFoundError(
                "The integration was successfull, "
                + "but the star's boundary was not reached. "
                + "Perhaps your TOVInputTwoFluid.MAXRADIUS is too small?"
            )

    check_integration_validity(two_fluid_tov_integration.success, two_fluid_tov_integration.status)

    return two_fluid_tov_integration


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


class TwoFluidTOVIntegrationError(Exception):
    pass


class BoundaryNotFoundError(Exception):
    pass
