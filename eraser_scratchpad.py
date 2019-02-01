## Import functions

from er_plot_functions import plot_all_freezing as plt_frz
from er_plot_functions import plot_experiment_traj as pltexp
import numpy as np
import Placefields as pf
##
# Get freezing for all mice

# Specify mice to plot here
all_mice = ['Marble3', 'Marble6', 'Marble7', 'DVHPC_5', 'DVHPC_6',
            'DVHPC_7', 'DVHPC_8', 'DVHPC_9', 'DVHPC_10']  # All mice
dmice_beh = ['DVHPC_5', 'DVHPC_6', 'DVHPC_7', 'DVHPC_8', 'DVHPC_9', 'DVHPC_10']  #DREADDS behavioral pilots
imice_cont = ['Marble3', 'Marble6', 'Marble7']  # Control imaging mice
gen_mice = ['GEN_1', 'GEN_2', 'GEN_3', 'GEN_4']


_, axall = plt_frz(all_mice)
axall.set_title('All Mice Combined')

_, axdbeh = plt_frz(dmice_beh)
axdbeh.set_title('DREADDS Beh. Pilots Only')
_, axic = plt_frz(imice_cont)
axic.set_title('Imaging Control Mice Only')

# Plot individual mouse trajectories

for mouse in all_mice:
    pltexp(mouse)


## Run through and get limits for all sessions for Marble7 to get idea of x/y lims of data
days = [-2, -1, 0, 4, 1, 2, 7]
arena = 'Shock'
mouse = 'Marble07'
lims = np.ones((2, 2, len(days)))*np.nan
for ida, day in enumerate(days):
    PF = pf.load_pf(mouse, arena, day)
    temp = np.asarray([[np.min(PF.xEdges), np.min(PF.yEdges)],
                       [np.max(PF.xEdges), np.max(PF.yEdges)]])
    lims[:, :, ida] = temp



