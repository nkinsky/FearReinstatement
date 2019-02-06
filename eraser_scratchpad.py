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
mouse = 'Marble12'
lims = np.ones((2, 2, len(days)))*np.nan
for ida, day in enumerate(days):

    # Use this code if you have run Placefields on data without manual limits
    # PF = pf.load_pf(mouse, arena, day)
    # temp = np.asarray([[np.min(PF.xEdges), np.min(PF.yEdges)],
    #                    [np.max(PF.xEdges), np.max(PF.yEdges)]])

    # use this code if you have run with manual limits and you want to check
    PF = pf.load_pf(mouse, arena, day, pf_file='placefields_cm1_manlims.pkl')
    temp = np.asarray([[np.min(PF.pos_align[0, :]), np.min(PF.pos_align[1, :])],
                       [np.max(PF.pos_align[0, :]), np.max(PF.pos_align[1, :])]])
    lims[:, :, ida] = temp

## Mice to run PFs on
control_mice_good = ['Marble06', 'Marble11', 'Marble12', 'Marble24']

ani_mice = ['Marble19', 'Marble25']

# Run with limits set to 1st session!
import Placefields as pf
import numpy as np
# mouse = 'Marble07'
mice = ['Marble11', 'Marble14']
arenas = ['Shock']
days = [-2, -1, 0, 4, 1, 2, 7]
for mouse in mice:
    for arena in arenas:
        try:  # load in PF object for day -2
            PForig = pf.load_pf(mouse, arena, -2)
        except FileNotFoundError:  # run placefields first if not done
            pf.placefields(mouse, arena, -2)
            PForig = pf.load_pf(mouse, arena, -2)

        lims_use = np.asarray([[np.min(PForig.xEdges) - 3, np.min(PForig.yEdges) - 3],
                               [np.max(PForig.xEdges) + 3, np.max(PForig.yEdges) + 3]])

        for day in days:  # run placefields again with new limits and save!
            try:
                pf.placefields(mouse, arena, day, lims_method=lims_use,
                               save_file='placefields_cm1_manlims.pkl', nshuf=1000)
            except:
                print('Bad session')


## Check to make sure all PF plots in a given arena are good/aligned
arena = 'Shock'
mouse = 'Marble14'
PF = []
days = [-2, -1, 4, 1, 2, 7]  # make sure to include day 0 for open arena!
for day in days:
    try:
        PF = pf.load_pf(mouse, arena, day, pf_file='placefields_cm1_manlims.pkl')
        PF.pfscroll()
    except FileNotFoundError:
        print('missing file for day ' + str(day))