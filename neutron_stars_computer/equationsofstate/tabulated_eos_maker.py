import neutron_stars_computer.star.conversionfactors as cf
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.fermionic_dm import FermionicDarkMatter
from neutron_stars_computer.equationsofstate.pQCD import PQCD

import numpy as np
import pandas as pd


def FDM_table_maker(MF: float, Y: float) -> None:
    eos: EquationOfState = FermionicDarkMatter(MF, Y)

    data_list = []

    for z in np.geomspace(1e-3, 1e0, 200):
	    e = eos.energy_density(z)*cf.GEV4_TO_MEVFM3
	    p = eos.pressure(z)*cf.GEV4_TO_MEVFM3

	    data_list.append({'e': e, 'p': p})


    tabulated_eos = pd.DataFrame(data_list)

    tabulated_eos.to_csv(f'/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m{MF}_y{Y}.csv',
	                        index = False, sep = ' ', float_format = '%.5e')


def pQCD_table_maker(X: float) -> None:
    eos: EquationOfState = PQCD(X=X)

    data_list = []

    for muB in np.geomspace(1e0, 6e0, 200):
	    e = eos.energy_density_from_mu(muB)*cf.GEV4_TO_MEVFM3
	    p = eos.pressure_from_mu(muB)*cf.GEV4_TO_MEVFM3

	    data_list.append({'e': e, 'p': p})


    tabulated_eos = pd.DataFrame(data_list)

    tabulated_eos.to_csv(f'/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/QM_EOS/pQCD_X{X}.csv',
	                        index = False, sep = ' ', float_format = '%.5e')