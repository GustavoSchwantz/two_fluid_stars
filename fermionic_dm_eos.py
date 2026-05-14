import neutron_stars_computer.star.conversionfactors as cf
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.fermionic_dm import FermionicDarkMatter

import numpy as np
import pandas as pd

def main() -> None:
    MF = 1

    eos: EquationOfState = FermionicDarkMatter(MF)

    data_list = []

    #for z in np.geomspace(1e-3, 1e0, 200):
    for z in np.geomspace(1e-1, 1e1, 200):
	    e = eos.energy_density(z)*cf.GEV4_TO_MEVFM3
	    p = eos.pressure(z)*cf.GEV4_TO_MEVFM3

	    data_list.append({'e': e, 'p': p})


    tabulated_eos = pd.DataFrame(data_list)

    tabulated_eos.to_csv(f'./neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m{MF}_y0.csv',
	                        index = False, sep = ' ', float_format = '%.5e')

if __name__ == '__main__':
    main()	