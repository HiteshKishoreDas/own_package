'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-20 16:33:19 
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

for i_wd, wd in enumerate(si.wdir_list):

    try:
        with open(f'{package_abs_path}pluto/save_arr/{si.file_list[i_wd]}/{si.file_list[i_wd]}_evolution.pkl', 'rb') as f:
            sim_data = pk.load(f)
    except:
        continue

    x_data = sim_data['time']/si.t0[i_wd]    
    y_data = np.array(sim_data['v_rad'])/si.v0[i_wd]

    x_data_list.append(x_data[1:])
    y_data_list.append(y_data[1:])

    # col_data_list.append(np.log10(si.R_list[i_wd]))
    col_data_list.append(si.N_list[i_wd])

    label_list.append(si.label_list[i_wd])


fig, ax = p2l.plot_multiline(x_data_list, y_data_list, \
                             color_list=col_data_list, \
                             label_list=label_list, \
                             cmap='viridis')#, mark_flag = True, markevery=5)

ax.set_xlim(0.25,3)
# ax.set_ylim(0,0.05)

# ax.axhline(-cs_cold linestyle='dashed', color='k', label=r'$c_{\rm s, floor}$')
ax.axhline(0.0, linestyle='dashed', color='k', label=r'$v_{\rm rad}/v_0 = 0$')
ax.axvline(si.t_collapse, linestyle='dotted', color='k', label=r'$t_{\rm collapse}$')

# ax.set_yscale('log')
# ax.set_xscale('log')

ax.set_xlabel(r'$\tilde{t}$')
ax.set_ylabel(r'$\frac{v_{\rm r, hot, avg}}{v_0}$', rotation=0, fontsize=30)

txt_box = ax.text(1.32,-1.23, r'$c_{\rm s, hot}/v_0 \approx 11.2 $',  
                  fontsize=20)
txt_box.set_bbox(dict(facecolor='white', edgecolor='gray'))
# ax.set_xlabel()

ax.legend()
plt.show()