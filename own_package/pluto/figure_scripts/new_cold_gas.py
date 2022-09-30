'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-20 16:03:09 
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


x_data_list   = []
y_data_list   = []
col_data_list = []
label_list    = []

# m_dot_fit     = []
m_dot_data    = []
time_data     = []
# t_fit         = []

for i_wd, wd in enumerate(si.wdir_list):

    try:
        with open(f'{package_abs_path}pluto/save_arr/{si.file_list[i_wd]}/{si.file_list[i_wd]}_evolution.pkl', 'rb') as f:
            sim_data = pk.load(f)
    except:
        continue

    x_data = sim_data['time']/si.t0[i_wd]    
    # y_data = sim_data['cold_gas']/si.M0[i_wd] - 1.0
    y_data = (sim_data['cold_gas'] - si.M0[i_wd])/si.V[i_wd]
    y_data /= si.Chi_f[i_wd]**(1/2)
    # y_data /= si.R_list[i_wd] ** (1/12)


    x_data_list.append(x_data[1:])
    y_data_list.append(y_data[1:])
    # col_data_list.append(np.log10(si.R_list[i_wd]))
    col_data_list.append(si.N_list[i_wd])
    label_list.append(si.label_list[i_wd])

    # t_fit.append(np.linspace(0,3.0,num=50))
    # m_dot_fit.append( mdot[i_wd]*(t_fit[i_wd]-0.25) + mb[i_wd] )

    m_dot = np.roll(y_data_list[i_wd],-1) - y_data_list[i_wd]
    m_dot /= (np.roll(x_data_list[i_wd],-1) - x_data_list[i_wd])

    m_dot_data.append(m_dot*si.M0[i_wd]/si.t0[i_wd])
    time_data.append(x_data_list[i_wd])


fig, ax = p2l.plot_multiline(x_data_list, y_data_list, \
                             color_list=col_data_list, \
                             label_list=label_list, \
                             cmap='viridis')#, mark_flag = True, markevery=5)

# fig, ax = p2l.plot_multiline(t_fit, m_dot_fit, \
#                              color_list=col_data_list, \
#                             #  label_list=label_list, \
#                              cmap='viridis', linestyle='dashed', \
#                              new_fig=False, fig=fig, ax=ax)
ax.set_xlim(0.25, 3.0 )
# ax.set_ylim(0,1.1)
ax.set_ylim(0,0.05)

# ax.set_yscale('log')
# ax.set_xscale('log')

ax.axvline(si.t_collapse, linestyle='dotted', color='k')

ax.set_xlabel(r'$\tilde{t}$')
ax.set_ylabel(r'$\Delta M_{\rm cold}/V_{\rm 0,cloud}$')

ax.legend()
plt.show()