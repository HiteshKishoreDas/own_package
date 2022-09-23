'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-20 16:37:36 
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

def v_fit(x):
    x_mean = 1.5
    x_std  = 0.8
    A = 1.1
    B = -1.0
    y_fit  = A*np.exp(  ( -(x-x_mean)**2  )  /  (2*(x_std**2))   ) + B

    return y_fit 

plt.figure()

for i_wd, wd in enumerate(si.wdir_list):

    try:
        with open(f'{package_abs_path}pluto/save_arr/{si.file_list[i_wd]}/{si.file_list[i_wd]}_evolution.pkl', 'rb') as f:
            sim_data = pk.load(f)
    except:
        continue

    x_data = sim_data['time']/si.t0[i_wd]    

    y_data = sim_data['vol']/si.V[i_wd]

    x_data_list.append((x_data)[1:])
    y_data_list.append((y_data)[1:])

    # col_data_list.append(np.log10(si.R_list[i_wd]))
    col_data_list.append(si.N_list[i_wd])
    label_list.append(si.label_list[i_wd])



fig, ax = p2l.plot_multiline(x_data_list, y_data_list, \
                             color_list=col_data_list, \
                             label_list=label_list, \
                             cmap='viridis')#, mark_flag = True, markevery=5)

# ax.plot(x_fit, y_fit, linestyle='dashed', color='k')

ax.set_xlim(0,3)
ax.set_ylim(0,1.0)

ax.set_xlabel(r'$\tilde{t}$')
ax.set_ylabel(r'$V/V_{\rm 0, cloud}$')

ax.axvline(si.t_collapse, linestyle='dotted', color='k', label=r'$t_{\rm collapse}$')

ax.legend()
plt.show()
