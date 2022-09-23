'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-20 16:41:18 
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


m_dot_data    = []
time_data     = []

for i_wd, wd in enumerate(si.wdir_list):

    try:
        with open(f'{package_abs_path}pluto/save_arr/{si.file_list[i_wd]}/{si.file_list[i_wd]}_evolution.pkl', 'rb') as f:
            sim_data = pk.load(f)
    except:
        continue

    x_data = sim_data['time']/si.t0[i_wd]    
    y_data = sim_data['cold_gas']/si.M0[i_wd] - 1.0

    x_data = x_data[1:]
    y_data = y_data[1:]

    m_dot = np.roll(y_data,-1) - y_data
    m_dot /= (np.roll(x_data,-1) - x_data)

    m_dot_data.append(m_dot*si.M0[i_wd]/si.t0[i_wd])
    time_data.append(x_data)

def m_dot_fit_func(R):
    return 4e-2*(si.R_list**(5/4))

plt.figure()


for i_wd, wd in enumerate(si.wdir_list):

    plt.scatter(si.R_list[i_wd]+np.zeros_like(m_dot_data[i_wd]) ,m_dot_data[i_wd] )

plt.plot(si.R_list, m_dot_fit_func(si.R_list))

plt.xscale('log')
plt.yscale('log')
plt.show()

plt.figure()
plt.violinplot(m_dot_data, positions=np.log10(si.R_list))

plt.plot(np.log10(si.R_list), m_dot_fit_func(si.R_list))

# plt.xscale('log')
plt.yscale('log')
plt.show()