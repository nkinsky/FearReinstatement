# Import functions

from er_plot_functions import plot_all_freezing as plt_frz
from er_plot_functions import plot_experiment_traj as pltexp

# Get freezing for all mice

# Specify mice to plot here
all_mice = ['Marble3', 'Marble6', 'Marble7', 'DVHPC_5', 'DVHPC_6',
            'DVHPC_7', 'DVHPC_8', 'DVHPC_9', 'DVHPC_10']  # All mice
dmice_beh = ['DVHPC_5', 'DVHPC_6', 'DVHPC_7', 'DVHPC_8', 'DVHPC_9', 'DVHPC_10']  #DREADDS behavioral pilots
imice_cont = ['Marble3', 'Marble6', 'Marble7']  # Control imaging mice


_, axall = plt_frz(all_mice)
axall.set_title('All Mice Combined')

_, axdbeh = plt_frz(dmice_beh)
axdbeh.set_title('DREADDS Beh. Pilots Only')
_, axic = plt_frz(imice_cont)
axic.set_title('Imaging Control Mice Only')

# Plot individual mouse trajectories

for mouse in all_mice:
    pltexp(mouse)



