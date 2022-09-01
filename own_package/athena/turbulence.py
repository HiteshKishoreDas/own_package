'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-01 12:19:22 
'''


import numpy as np
import sys
import os

import matplotlib.pyplot as plt

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}athena/')
import history as ht

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
from v_turb import cs_calc
import units as un


# TODO: Change to using plot_2d.py for multicolor line plots
def plot_mach (file_list, MHD_list, ncells_list, cool_flag_list):

    if file_list[0][-1]=='/':
        hst_add = 'Turb.hst'
    else:
        hst_add = '/Turb.hst'

    for i_fl, fl in enumerate(file_list):

        hst = ht.hst_data(fl, \
                          ncells    = ncells_list[i_fl], \
                          MHD_flag  = MHD_list[i_fl] , \
                          cool_flag = cool_flag_list[i_fl]  )

        fig,ax = plt.subplots(nrows=1, ncols=1)

        ax.plot(hst.time, hst.turb_vel)

    return fig,ax