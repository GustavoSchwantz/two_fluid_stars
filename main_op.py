from neutron_stars_computer.star.stability import CentralRadOscInput
from neutron_stars_computer.star.tov_solver import TOVInput
from neutron_stars_computer.star.factory import StarStabilityFactory, StarFactory
from neutron_stars_computer.star.constellation import create_stellar_family
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.massless_mit_bm import MasslessMITBM

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main() -> None:
    #print('Starting...')
    #start = time.time()

    eos: EquationOfState = MasslessMITBM(60)
    central_pressures = np.geomspace(1e-1, 1e4, 100)
    #tov_input = TOVInput(
    #    eos,
    #    ABSOLUTE_TOLERANCE=[1e-4, 1e-4, 1e-6],
    #    RELATIVE_TOLERANCE=1e-3
    #)


    #fac = StarFactory(tov_input)
    #stars: pd.DataFrame = create_stellar_family(
    #    fac,
    #    central_pressures
    #)
    #print(stars)

    #end = time.time()
    #print(f"Time to complete: {end - start:.2f} s")

    central_densities = np.array([eos.energy_density_from(p) for p in central_pressures])

    df = pd.DataFrame({'pressures': central_pressures, 'densities': central_densities})

    print(df)

    df.plot('densities', 'pressures', loglog=True, xlim=(1e0, 1e5), ylim=(1e0, 1e4))
    plt.savefig('fig.png')

if __name__ == '__main__':
    main()
