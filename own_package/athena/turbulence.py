'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-01 12:19:22 
'''

from matplotlib.pyplot import text
import numpy as np
import sys
import os

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}athena/')
import history as ht

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_2d as p2

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
from v_turb import cs_calc
import units as un

def turb_vel(hst):
    return hst.turb_vel

def mach_t (hst):
    return hst.turb_vel/hst.cs_avg

def beta(hst):
    return hst.PB_avg/hst.Pth_avg

def Ma(hst):
    va = hst.B_abs_avg
    return hst.turb_vel/va

def beta_0(hst):

    T_hot = 4e6
    rho   = 1.0

    Pth  = T_hot/(un.KELVIN*un.mu)
    Pth *= rho

    return Pth/hst.PB_avg

def PB(hst):
    return hst.PB_avg


def plot_time_evolution (y_func, file_list, MHD_list, ncells_list, cool_flag_list, \
                         normalise_list = {'x_norm':[None], 'y_norm':[None]}, \
                         ax_log= {'x_log': False, 'y_log':False, 'col_log':False}, \
                         label_list = None, linestyle='solid'):

    if file_list[0][-1]=='/':
        hst_add = 'Turb.hst'
    else:
        hst_add = '/Turb.hst'

    x_data_list = []
    y_data_list = []

    for i_fl, fl in enumerate(file_list):

        print(i_fl)

        hst = ht.hst_data(fl+hst_add, \
                          ncells    = ncells_list[i_fl], \
                          MHD_flag  = MHD_list[i_fl] , \
                          cool_flag = cool_flag_list[i_fl]  )

        x_data_list.append(hst.time)
        y_data_list.append(y_func(hst))

    fig, ax = p2.plot_multiline(x_data_list, y_data_list, ax_log=ax_log, linestyle=linestyle, \
                                normalise_list=normalise_list, label_list=label_list) 
    
    return fig, ax

if __name__ == "__main__":

    # wdir_loc  = '/afs/mpa/home/hitesh/remote/cobra/athena_fork_turb_box/turb_v2/'
    wdir_loc  = '/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/turb_v2/'

    file_loc1 = wdir_loc + 'para_scan_Rlsh0_1000_res0_64_rseed_1_M_0.5_fshear_0.0_beta_100'
    file_loc2 = wdir_loc + 'para_scan_Rlsh0_1000_res0_64_rseed_1_M_0.5_fshear_0.1_beta_100'
    file_loc3 = wdir_loc + 'para_scan_Rlsh0_1000_res0_64_rseed_1_M_0.5_fshear_0.3_beta_100'
    file_loc4 = wdir_loc + 'para_scan_Rlsh0_1000_res0_64_rseed_1_M_0.5_fshear_0.5_beta_100'
    file_loc5 = wdir_loc + 'para_scan_Rlsh0_1000_res0_64_rseed_1_M_0.5_fshear_0.75_beta_100'
    file_loc6 = wdir_loc + 'para_scan_Rlsh0_1000_res0_64_rseed_1_M_0.5_fshear_1.0_beta_100'

    # file_loc1 = wdir_loc + 'para_scan_comp_fshear_0.1_Rlsh0_10_res0_128_rseed_1_M_0.5_beta_100/'
    # file_loc2 = wdir_loc + 'para_scan_comp_fshear_0.3_Rlsh0_10_res0_128_rseed_1_M_0.5_beta_100/'
    # file_loc3 = wdir_loc + 'para_scan_comp_fshear_1.0_Rlsh0_10_res0_128_rseed_1_M_0.5_beta_100/'

    l_shatter = 8.6e-7
    cs = cs_calc(4e6, un.mu)
    print(cs)

    Rlsh  = 1000
    const = Rlsh*40*l_shatter/cs
    M = 0.5
    # const = 0.5

    arg_dict = {}
    arg_dict['file_list']      = [file_loc1               , file_loc2               , file_loc3               , file_loc4               , file_loc5                , file_loc6                ]
    arg_dict['MHD_list' ]      = [True                    , True                    , True                    , True                    , True                     , True                     ]
    arg_dict['ncells_list']    = [[64,64,64]              , [64,64,64]              , [64,64,64]              , [64,64,64]              , [64,64,64]               , [64,64,64]               ]
    arg_dict['cool_flag_list'] = [False                   , False                   , False                   , False                   , False                    , False                    ]
    arg_dict['label_list']     = [r'$f_{\rm shear} = 0.0$', r'$f_{\rm shear} = 0.1$', r'$f_{\rm shear} = 0.3$', r'$f_{\rm shear} = 0.5$', r'$f_{\rm shear} = 0.75$', r'$f_{\rm shear} = 1.0$' ]
    arg_dict['normalise_list'] = {'x_norm':[const/M for i in range(len(arg_dict['file_list']))], 'y_norm':[None]}


    import matplotlib.pyplot as plt
    # plt.style.use('dark_background')

    style_lib  = '../plot/style_lib/' 
    pallette   = style_lib + 'dark_pallette.mplstyle'
    # pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'

    plt.style.use([pallette, plot_style, text_style])

    fig,ax = plot_time_evolution(y_func = mach_t, **arg_dict )
    # ax.axhline(1.0, linestyle='dashed')

    ax.set_xlabel(r'$ t/t_{\rm eddy}$')
    ax.set_ylabel(r'$\mathcal{M}(t)$')
    
    plt.legend()
    plt.show()

    arg_dict['ax_log'] = {'x_log': False, 'y_log':True, 'col_log':False}

    fig,ax = plot_time_evolution(y_func = Ma, **arg_dict)
    ax.set_xlabel(r'$t/t_{\rm eddy}$')
    ax.set_ylabel(r'$\mathcal{M}_{A}$')

    ax.axhline(1.0, linestyle='dashed') 

    plt.legend()
    plt.show()
    # plt.savefig('test.png')

    fig,ax = plot_time_evolution(y_func = PB, **arg_dict) 
    ax.set_xlabel(r'$t/t_{\rm eddy}$')
    ax.set_ylabel(r'$P_{\rm B}$')
    

    plt.legend()
    plt.show()

    fig,ax = plot_time_evolution(y_func = beta_0, **arg_dict)
    ax.set_xlabel(r'$t/t_{\rm eddy}$')
    ax.set_ylabel(r'$\beta_0$')

    beta_eq = (2/un.g) / (M**2) 

    ax.axhline(beta_eq, linestyle='dashed', label=r'$\beta_{\mathcal{M}_{A} = 1}$') 

    plt.legend()
    plt.show()