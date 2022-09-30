'''
Created Date: Thursday, January 1st 1970, 1:00:00 am
Author: Hitesh Das
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

sys.path.insert(0, f'{package_abs_path}cooling/')
import cooling_fn as cf

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_2d_line as p2l

sys.path.insert(0, f'{package_abs_path}athena/figure_scripts/')
import sim_info as si

sys.path.insert(0, f'{package_abs_path}utils/')
import units as un


style_lib  = f'{package_abs_path}plot/style_lib/' 
# pallette   = style_lib + 'dark_pallette.mplstyle'
pallette   = style_lib + 'bright_pallette.mplstyle'
plot_style = style_lib + 'plot_style.mplstyle'
text_style = style_lib + 'text.mplstyle'

plt.style.use([pallette, plot_style, text_style])


def lum_fn(hst,i):

    N_last = 2000

    #* Copied cumulative cooling data
    tot_cool = np.copy(hst.total_cooling)[:N_last]

    dcool = np.roll(tot_cool, -1) - tot_cool
    dt    = np.roll(hst.time[:N_last], -1) - hst.time[:N_last]

    dcool = dcool   [hst.cold_gas_fraction[:N_last]>0.1]
    dt    = dt      [hst.cold_gas_fraction[:N_last]>0.1]
    time  = (hst.time[:N_last])[hst.cold_gas_fraction[:N_last]>0.1]

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


# Lambda_fac = [ 1.0, 1.0, 1.0, 1.0, 1.0, 10.0, 100.0, 1000.0, 10000.0]
Lambda_fac = [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
ncells     = [128, 128, 1280]


L_avg_list  = []
Da_list  = []

Da_list_line  = []
Da_list_point = []
Q_strong_list = []
Q_weak_list   = []



for j in range(len(si.Ma)):
    for i in range(len(si.box_width)):


        #* Damkohler number calculation
        # v_turb in km/s
        u  =  50 * (si.M**(4/5))
        u *=  ( si.cs_cold*un.unit_velocity/(15*1e5) )**0.8
        u *=  ( si.t_cool_cloud[0]/0.03 )**-0.1

        # tcool_tKH = np.round(si.t_cool_mix[i]/si.t_KH[0], 4)

        t_turb = si.box_width[i] / (u*1e5/un.unit_velocity)
        t_cool = cf.tcool_calc(si.amb_rho*np.sqrt(si.chi_cold), 2e5 ,si.Z, Lambda_fac=Lambda_fac[i])
        # t_cool = si.t_cool_Da[0]
        Da = t_turb/t_cool


        Da_cut = 2

        #* For strong cooling line
        p_e_strong= 1
        u_e_strong= 3/4
        L_e_strong= 1/4
        t_e_strong= -1/4

        #* For weak cooling line
        p_e_weak  = 1
        u_e_weak  = 1/2
        L_e_weak  = 1/2
        t_e_weak  = -1/2

        # Q0 = 1
        Q0 = 5.66e-8             # in code units

        P     = si.amb_rho*si.T_hot/si.mu    # in kB cm^-3 K

        P_term_strong = (P/160)**p_e_strong
        P_term_weak   = (P/160)**p_e_weak

        u_term_strong = (u/30)**u_e_strong
        u_term_weak   = (u/30)**u_e_weak

        L_term_strong = (si.box_width[i]*1000/100)**L_e_strong
        L_term_weak   = (si.box_width[i]*1000/100)**L_e_weak

        t_cool_cloud = cf.tcool_calc(si.amb_rho*si.chi_cold, si.T_floor ,si.Z, Lambda_fac=Lambda_fac[i])

        t_term_strong = (t_cool_cloud/0.03)**t_e_strong
        t_term_weak   = (t_cool_cloud/0.03)**t_e_weak

        Q_strong = Q0
        Q_strong *= P_term_strong
        Q_strong *= u_term_strong
        Q_strong *= L_term_strong
        Q_strong *= t_term_strong

        Q_weak   = Q0
        Q_weak   *= P_term_weak
        Q_weak   *= u_term_weak
        Q_weak   *= L_term_weak
        Q_weak   *= t_term_weak
        
        #* Q/Q_0
        Q_strong_list.append(Q_strong)
        Q_weak_list.append(Q_weak)

        # Q_strong_scaled_list.append(Q_strong)#/P_term_strong/u_term_strong/L_term_strong/t_term_strong)
        # Q_weak_scaled_list.append(Q_weak)#/P_term_weak/u_term_weak/L_term_weak/t_term_weak)

        print(f'Da: {Da}')
        Da_list_line.append(Da)
        Da_list_point.append(Da)

        k=0
        B_fl = False

        #* Read history file 
        file_add = si.filename_mix_add_ext(i,j,k,B_fl)# [:-7]
        if not B_fl:
            setup_name = file_add
        dir_name = f'/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_brent/'
        dir_name += f'mix{file_add}'

        hst = ht.hst_data(f'{dir_name}/Turb.hst', ncells, B_fl, cool_flag=True)     
        time, luminosity = lum_fn(hst, i)

        L_avg = np.average(luminosity[-250:])

        print(f'L_avg: {L_avg}')
        L_avg_list.append(L_avg)

        constant = 1

        # if Da<2:
        #     L_scaled_list.append(constant * L_avg)#/P_term_weak/u_term_weak/L_term_weak/t_term_weak)
        # else:
        #     L_scaled_list.append(constant * L_avg)#/P_term_strong/u_term_strong/L_term_strong/t_term_strong/1e4)


plt.figure()

plt.xscale('log')
plt.yscale('log')


# unit_Q = g.unit_energy * (g.unit_length**-2) * (g.unit_time**-1)

sim_plot    = []
theory_plot = []

sim_plot    = np.array(L_avg_list)
# sim_plot    = sim_plot/sim_plot[-1]

theory_strong_plot = np.array(Q_strong_list)
theory_weak_plot   = np.array(Q_weak_list)

# theory_plot = theory_plot/theory_plot[-1]

# plt.plot(Da_list, sim_plot, label='Simulation luminosity')
# plt.plot(Da_list, theory_plot, label=r'Q/Q$_0$ from Theory $\times 10^4$')
# plt.plot(Da_list, theory_plot/sim_plot, label='Theory')

for i_Da, Da in enumerate(Da_list_point):
    plt.scatter(Da, L_avg_list[i_Da], color='k')# ,label='Simulation luminosity')


plt.plot(Da_list_line, Q_strong_list, linestyle='dashed', label=r'Q: strong cooling')
plt.plot(Da_list_line, Q_weak_list,   linestyle='dashed', label=r'Q: weak cooling')

# Da_arr = np.array(Da_list)
# Q0_fit = (5/3)*1e-8*  (Da_arr**-(1/3))

# plt.plot(Da_arr, Q0_fit)

plt.xlabel("Da")
plt.ylabel(r"Q (erg cm$^{-2}$ s$^{-1}$)")

plt.legend()

plt.show()
# plt.savefig('hydro_check.png')
