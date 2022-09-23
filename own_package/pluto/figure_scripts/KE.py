'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-20 16:47:05 
'''

import numpy as np
import pickle as pk
import os
import sys
import gc

import matplotlib.pyplot as plt

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-(len(cwd.split('/')[-1])+len(cwd.split('/')[-2])+1)]

style_lib  = f'{package_abs_path}plot/style_lib/' 
# pallette   = style_lib + 'dark_pallette.mplstyle'
pallette   = style_lib + 'bright_pallette.mplstyle'
plot_style = style_lib + 'plot_style.mplstyle'
text_style = style_lib + 'text.mplstyle'

plt.style.use([pallette, plot_style, text_style])

sys.path.insert(0, f'{package_abs_path}pluto/')
import units as g 

sys.path.insert(0, f'{package_abs_path}pluto/figure_scripts/')
import sim_info as si

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_2d_line as p2l


x_data_list      = []
y_data_cold_list = []
y_data_hot_list  = []
col_data_list    = []
label_hot_list   = []
label_cold_list  = []


for i_wd, wd in enumerate(si.wdir_list):

    try:
        with open(f'{package_abs_path}pluto/save_arr/{si.file_list[i_wd]}/{si.file_list[i_wd]}_evolution.pkl', 'rb') as f:
            sim_data = pk.load(f)
    except:
        continue

    x_data = sim_data['time']/si.t0[i_wd]    
    x_data_list.append(x_data[1:])

    y_data_cold = sim_data['KE_cold']/si.M0[i_wd]
    y_data_hot  = sim_data['KE_hot' ]/si.M0[i_wd]

    y_data_cold_list.append(y_data_cold[1:])
    y_data_hot_list .append(y_data_hot[1:])

    # col_data_list.append(np.log10(si.R_list[i_wd]))
    col_data_list.append(si.N_list[i_wd])
    label_cold_list.append(si.label_list[i_wd]+' Cold')
    label_hot_list .append(si.label_list[i_wd]+' Hot')



fig, ax = p2l.plot_multiline(x_data_list, y_data_cold_list, \
                             color_list=col_data_list, \
                             label_list=label_cold_list, \
                             cmap='viridis')#, mark_flag = True, markevery=5)

fig, ax = p2l.plot_multiline(x_data_list, y_data_hot_list, \
                             color_list=col_data_list, \
                             label_list=label_hot_list, \
                             cmap='viridis', linestyle='dashed',\
                             new_fig=False, fig=fig, ax=ax )

ax.set_xlim(0.25,3)
# ax.set_ylim(0,0.175)

# ax.set_yscale('log')
# ax.set_xscale('log')

ax.axvline(si.t_collapse, linestyle='dotted', color='k', label=r'$t_{\rm collapse}$')

ax.set_xlabel(r'$\tilde{t}$')
ax.set_ylabel(r'$KE/M_{\rm 0,cloud}$')

ax.legend()
plt.show()

#*_______________________________#

x_data_list      = []
y_data_list = []
col_data_list    = []
label_list   = []

for i_wd, wd in enumerate(si.wdir_list):

    try:
        with open(f'{package_abs_path}pluto/save_arr/{si.file_list[i_wd]}/{si.file_list[i_wd]}_evolution.pkl', 'rb') as f:
            sim_data = pk.load(f)
    except:
        continue

    x_data = sim_data['time']/si.t0[i_wd]    
    x_data_list.append(x_data[1:])

    y_data = sim_data['KE_cold']/si.M0[i_wd]
    y_data /= (sim_data['KE_hot' ]/si.M0[i_wd])

    y_data_list.append(y_data[1:])

    # col_data_list.append(np.log10(si.R_list[i_wd]))
    col_data_list.append(si.N_list[i_wd])
    label_list.append(si.label_list[i_wd])



fig, ax = p2l.plot_multiline(x_data_list, y_data_list, \
                             color_list=col_data_list, \
                             label_list=label_list, \
                             cmap='viridis')#, mark_flag = True, markevery=5)


ax.set_xlim(0.25,3)
# ax.set_ylim(0,0.175)

ax.set_yscale('log')
# ax.set_xscale('log')

ax.axvline(si.t_collapse, linestyle='dotted', color='k', label=r'$t_{\rm collapse}$')

ax.set_xlabel(r'$\tilde{t}$')
ax.set_ylabel(r'$KE_{\rm cold}/KE_{\rm hot}$')

ax.legend()
plt.show()