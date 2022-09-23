'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-21 16:57:23 
'''

import numpy as np
import sys
import os
import gc

import pickle as pk

import matplotlib.pyplot as plt

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]


sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

style_lib  = f'{package_abs_path}plot/style_lib/' 
# pallette   = style_lib + 'dark_pallette.mplstyle'
pallette   = style_lib + 'bright_pallette.mplstyle'
plot_style = style_lib + 'plot_style.mplstyle'
text_style = style_lib + 'text.mplstyle'

plt.style.use([pallette, plot_style, text_style])

main_dir_loc  = '/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_brent/'
dir_list = [ main_dir_loc + f'mix_L{i}_Ma0_Bnot_hydro_moving/' for i in range(9)]


if False:
    for i_dir, dir in enumerate(dir_list):

        print(f'{dir=}')

        front_dict = {}
        front_dict['time'] = []
        front_dict['loc']  = []

        for i in range(201):

            print(f'{i=}')

            file_loc = dir + f'Turb.out2.{str(i).zfill(5)}.athdf'

            try:
                out_dict = dr.get_array_athena(file_loc, fields=['rho', 'coord'],MHD_flag=False)
            except:
                break

            rho_z   = np.average(out_dict['rho'], axis=(1,2))
            z_coord = out_dict['coord'][2]

            rho_mix = np.sqrt(rho_z.max()*rho_z.min())

            rho_mix_loc = np.min(z_coord[np.argwhere(rho_z<rho_mix)])

            front_dict['loc'] .append(rho_mix_loc)
            front_dict['time'].append(out_dict['time'])


        with open(f'./save_arr/front_location_L{i_dir}.pkl', 'wb') as f:
            pk.dump(front_dict, f)
            
box_width  = np.array([10000.0, 1000.0, 100.0, 10.0, 1.0, 1.0 , 1.0  , 1.0   , 1.0    ]) * 0.1
Lambda_fac = np.array([1.0    , 1.0   , 1.0  , 1.0 , 1.0, 10.0, 100.0, 1000.0, 10000.0])

# box_width *= Lambda_fac

if True:

    plt.figure()
    m_list = []
    w_list = []

    for i_dir, dir in enumerate(dir_list):

        try:
            with open(f'./save_arr/front_location_L{i_dir}.pkl', 'rb') as f:
                front_dict = pk.load(f)
        except:
            continue

        if i_dir<8:
            x_plot = np.array(front_dict['time'])#/box_width[i_dir]
            y_plot = np.array(front_dict['loc']) #/box_width[i_dir]

            x_plot = x_plot[50:150]
            y_plot = y_plot[50:150]

            label_str  = r'$\Lambda_0=$'+f'{Lambda_fac[i_dir]}, '
            label_str += r'$L_{\rm box}=$'+f'{box_width[i_dir]}'

            plt.plot(x_plot/box_width[i_dir], y_plot/box_width[i_dir], label=label_str)

            m,b = np.polyfit(x_plot, y_plot, 1)

            m_list.append(m)
            w_list.append(box_width[i_dir])

            # plt.scatter(box_width[i_dir], m)

    # w_list = np.array(w_list)
    # v_m, v_b = np.polyfit(np.log10(w_list), np.array(m_list), 1)

    # v_m = round(v_m,5)
    # v_b = round(v_b,5)

    # plt.plot( w_list, v_m*np.log10(w_list)+v_b , label=f'{v_m} log(w)+{v_b}', color='k', zorder=-5)

    plt.legend()
    # plt.xscale('log') 
    # plt.yscale('log')
    # plt.xlim(0,1e6)
    # plt.ylim(0,1e4)

    # plt.xlabel("Box size (w) (kpc)")
    plt.xlabel("time (Myr)")
    plt.ylabel("Front position (kpc)")