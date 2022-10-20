'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-22 11:39:58 
'''

import numpy as np
import sys
import os
import gc

import pickle as pk

import matplotlib.pyplot as plt
import scipy.signal as sg

cwd = os.path.dirname(__file__)
tail_cut = len(cwd.split('/')[-1])+len(cwd.split('/')[-2])+1
package_abs_path = cwd[:-tail_cut]

sys.path.insert(0, f'{package_abs_path}athena/')
import history as ht

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_2d_line as p2l

sys.path.insert(0, f'{package_abs_path}cooling/')
import cooling_fn as cf

sys.path.insert(0, f'{package_abs_path}utils/')
import units as un

sys.path.insert(0, f'{package_abs_path}athena/figure_scripts/')
# import sim_info as si
import sim_info_shift as si

style_lib  = f'{package_abs_path}plot/style_lib/' 
# pallette   = style_lib + 'dark_pallette.mplstyle'
pallette   = style_lib + 'bright_pallette.mplstyle'
plot_style = style_lib + 'plot_style.mplstyle'
text_style = style_lib + 'text.mplstyle'

plt.style.use([pallette, plot_style, text_style])




def overflow_cut(hst,i):

    N_last = 2000

    #* Copied cumulative cooling data
    tot_cool = np.copy(hst.total_cooling)[:N_last]

    dcool = np.roll(tot_cool, -1) - tot_cool
    dt    = np.roll(hst.time[:N_last], -1) - hst.time[:N_last]
    time  = (hst.time[:N_last])

    dcool = dcool   [hst.cold_gas_fraction[:N_last]>0.1]
    dt    = dt      [hst.cold_gas_fraction[:N_last]>0.1]
    time  = time    [hst.cold_gas_fraction[:N_last]>0.1]

    box_full = np.argwhere(hst.cold_gas_fraction[:N_last]>0.998)

    if len(box_full)!=0:
        dcool = dcool   [:np.min(box_full)]
        dt    = dt      [:np.min(box_full)]
        time  = hst.time[:np.min(box_full)]

    box_volume = si.box_length*si.box_width*si.box_width
    dz = (si.box_length[i]/si.nx3[0])
    dy = (si.box_width [i]/si.nx2[0])
    dx = (si.box_width [i]/si.nx1[0])

    luminosity  = (dcool/dt)[1:-1] * dx * dy * dz
    luminosity /= (si.box_width[i] * si.box_width[i])
    time       = time[1:-1]

    return time, luminosity


ncells     = [64, 64, 640]


plot_dict = {}

plot_dict['x_data_list']     = []
plot_dict['y_data_list']     = []
plot_dict['col_list']        = []
plot_dict['label_list']      = []
plot_dict['linestyle_list']  = []

plot_dict['B_list']          = []
plot_dict['marker_list']     = []
plot_dict['color_list']      = []

plot_dict['L_avg_list']      = []
plot_dict['L_avg_plot_list'] = []
plot_dict['Da_list']         = []
# plot_dict['shift_list']      = []

linesty = ['dashed', '-.', 'dotted']
# linesty = ['solid', 'dashed']
B_list = ['B_x', 'B_y', 'B_z']
marker_list = ['D', 'X', '^']
# marker_list = ['X', 'D']
color_list = ['tab:green', 'tab:red', 'tab:orange']
# color_list = ['tab:green', 'tab:blue']




for i in range(len(si.box_width)):
# for i in range(4,5):
    for j in range(len(si.Ma)):
        for B_fl in [True, False]:
        # for B_fl in [False]:
        # for B_fl in [True]:
            for k in range(1):
            # for B_fl in [True]:

                if not B_fl and k>0:
                    break

                #* Read history file 
                file_add = si.filename_mix_add_ext(i,j,k,B_fl)# [:-7]
                # dir_name = f'/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_brent/'
                dir_name = f'/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_shift/'
                # dir_name = f'/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_shift/Trial_1_half_shift/'
                # dir_name = f'/home/hitesh/remote/mpa/remote/freya/athena_fork_turb_box/mixing_layer_shift/'
                dir_name += f'mix{file_add}'
                # print(dir_name)

                hst = ht.hst_data(f'{dir_name}/Turb.hst', \
                                  ncells=ncells, \
                                  box_size= [si.box_width[i], si.box_width[i], si.box_length[i]], \
                                  MHD_flag=B_fl, cool_flag=True, shift_flag=True)     

                # try:
                #     hst = ht.hst_data(f'{dir_name}/Turb.hst', ncells, B_fl, cool_flag=True)     
                # except:
                #     continue

                #* Damkohler number calculation
                # v_turb in km/s
                u  =  50 * (si.M**(4/5))
                u *=  ( si.cs_cold*un.unit_velocity/(15*1e5) )**0.8
                u *=  ( si.t_cool_cloud[0]/0.03 )**-0.1
           
                # tcool_tKH = np.round(si.t_cool_mix[i]/si.t_KH[0], 4)
           
                t_turb = si.box_width[i] / (u*1e5/un.unit_velocity)
                t_cool = cf.tcool_calc(si.amb_rho*np.sqrt(si.chi_cold), 2e5 ,si.Z, Lambda_fac=si.Lambda_fac[0])
                # t_cool = si.t_cool_Da[0]
                Da = (t_turb/t_cool)[0]

                # print(Da)

                plot_dict['Da_list'].append(Da)
                # plot_dict['shift_list'].append(si.shift_flag[i])
                # plot_dict['linestyle_list'].append(linesty[si.shift_flag[i]])
                # plot_dict['marker_list'].append(marker_list[si.shift_flag[i]])
                # plot_dict['color_list'].append(color_list[si.shift_flag[i]])

                if not B_fl:
                    plot_dict['linestyle_list'].append('solid')
                    plot_dict['B_list'].append('hydro')
                    plot_dict['marker_list'].append('o')
                    plot_dict['color_list'].append('tab:blue')
                    plot_dict['label_list'].append(f'{Da = : .1e}')
                else:
                    plot_dict['linestyle_list'].append(linesty[k])
                    plot_dict['B_list'].append(B_list[k])
                    plot_dict['marker_list'].append(marker_list[k])
                    plot_dict['color_list'].append(color_list[k])
                    plot_dict['label_list'].append(f'{Da = : .1e}, {B_list[k]}')



                #* From history file
                # time, luminosity = hst.overflow_cut(hst, hst.luminosity)
                time, luminosity = hst.overflow_cut(hst.luminosity, \
                                                    cut_var = hst.front_posn_fraction, \
                                                    cut_list = [0.15,0.85] )
                # time, luminosity = overflow_cut(hst, i)

                plot_dict['x_data_list'].append(time/si.t_KH[i])
                plot_dict['y_data_list'].append(luminosity)

                plot_dict['col_list'].append(np.log10(si.box_width[i]))


                L_avg = np.average(luminosity[-100:])
                print(f'{L_avg = }, {k = }, {B_fl = }, box_size = {si.box_width[i]}, {Da = }')


                # t_turb = si.box_width[i_plot]/si.v_shear
                # t_cool = si.t_cool_Da
                # Da = (t_turb/t_cool)[0]



                plot_dict['L_avg_plot_list'].append([L_avg for i in range(len(plot_dict['x_data_list'][-1]))])
                plot_dict['L_avg_list'].append(L_avg)

        # print(f'Box_width: {si.box_width[i_plot]} kpc, Da = {Da}')


plt_dict = p2l.plot_multiline(plot_dict['x_data_list'], plot_dict['y_data_list'],\
                              cmap='plasma',                         \
                              linestyle=plot_dict['linestyle_list'], \
                              color_list=plot_dict['col_list'],      \
                              label_list=plot_dict['label_list'],    \
                              smooth_flag=True , smooth_window=11)

plt_dict = p2l.plot_multiline(plot_dict['x_data_list'], plot_dict['L_avg_plot_list'],\
                              cmap='plasma', linestyle='dotted',\
                              color_list=plot_dict['col_list'], \
                              new_fig=False, fig=plt_dict['fig'], ax=plt_dict['ax'])

# ax.legend(loc='lower left')
# ax.set_xlim(0,12)
plt_dict['ax'].set_xlim(0, None)
# ax.set_ylim(1e-7,7e-6)
# ax.set_ylim(1e-10,3e-8)
# ax.set_ylim(1e-10,1e-8)

plt_dict['ax'].set_yscale('log')

plt_dict['ax'].set_xlabel(r'$t/t_{\rm KH}$')
plt_dict['ax'].set_ylabel(r'$Q$ (code units)')

# plt_dict['ax'].legend()


# from matplotlib.patches import Patch
from matplotlib.lines import Line2D

Da_list = np.array(plot_dict['Da_list'])

plt.figure()

for i_Da, Da in enumerate(Da_list):
    plt.scatter(Da, plot_dict['L_avg_list'][i_Da], \
                marker=plot_dict['marker_list'][i_Da], \
                # label=plot_dict['B_list'][i_Da], \
                color=plot_dict['color_list'][i_Da], \
                edgecolor='k')


legend_elements = [ Line2D([0], [0], color='tab:orange', lw=4, label=r'$\alpha=1/2$', linestyle='dashed'),
                    Line2D([0], [0], color='tab:red'   , lw=4, label=r'$\alpha=1/4$', linestyle='dashed'),
                    Line2D([0], [0], marker='o', color='w', markerfacecolor='tab:blue'  , label='HD'    , markersize=15), 
                    Line2D([0], [0], marker='D', color='w', markerfacecolor='tab:green' , label=r'B$_x$', markersize=15), 
                    Line2D([0], [0], marker='X', color='w', markerfacecolor='tab:red'   , label=r'B$_y$', markersize=15), 
                    Line2D([0], [0], marker='^', color='w', markerfacecolor='tab:orange', label=r'B$_z$', markersize=15)  ] 

# legend_elements = [ Line2D([0], [0], color='tab:orange', lw=4, label=r'$\alpha=1/2$', linestyle='dashed'),
#                     Line2D([0], [0], color='tab:red'   , lw=4, label=r'$\alpha=1/4$', linestyle='dashed'),
#                     Line2D([0], [0], marker='X', color='w', markerfacecolor='tab:green' , label='Without shift', markersize=15), 
#                     Line2D([0], [0], marker='D', color='w', markerfacecolor='tab:blue', label='With shift', markersize=15)  ] 

plt.plot(Da_list, 1.7e-6*Da_list**0.5 , linestyle='dashed', color='tab:orange', zorder=-10,  label=r'$\alpha=1/2$')
plt.plot(Da_list, 1.7e-6*Da_list**0.25, linestyle='dashed', color='tab:red'   , zorder=-10,  label=r'$\alpha=1/4$')

plt.xscale('log')
plt.yscale('log')

plt.xlabel('Da')
plt.ylabel('Q (code units)')

plt.title("Scaling comparison with code units")

plt.legend(handles=legend_elements)

plt.show()
# plt.savefig("test.png")


# %%
