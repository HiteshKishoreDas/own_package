'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-22 11:39:58 
'''

from cProfile import label
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

sys.path.insert(0, f'{package_abs_path}athena/figure_scripts/')
import sim_info as si

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


# fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (10,10))

Da_list       = []
L_avg_list    = []
Q_theory_list = []


# Lambda_fac = [ 1.0, 1.0, 1.0, 1.0, 1.0, 10.0, 100.0, 1000.0, 10000.0]
Lambda_fac = [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
ncells     = [128, 128, 1280]


x_data_list = []
y_data_list = []
col_list    = []
label_list  = []

L_avg_list  = []
Da_list  = []

for i_plot,i in enumerate(range(len(si.box_width))):
    for j in range(len(si.Ma)):
        for k in range(1):
            # for B_fl in [True, False]:
            for B_fl in [False]:


                #* Read history file 
                file_add = si.filename_mix_add_ext(i,j,k,B_fl)# [:-7]
                if not B_fl:
                    setup_name = file_add
                dir_name = f'/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_brent/'
                dir_name += f'mix{file_add}'

                # dir_name = file_list[i] 

                # try:
                #     hst = ht.hst_data(f'{dir_name}/Turb.hst', ncells, B_fl)     
                # except:
                #     continue

                hst = ht.hst_data(f'{dir_name}/Turb.hst', ncells, B_fl, cool_flag=True)     
                time, luminosity = lum_fn(hst, i)

                if i_plot<9:
                    x_data_list.append(time/si.t_KH[i_plot])
                    y_data_list.append(luminosity)

                    col_list.append(np.log10(si.box_width[i_plot]))
                    # label_list.append(f'Lbox = {si.box_width[i_plot]}, '+ r'$\Lambda_0$=' + f'{Lambda_fac[i_plot]}')


                # ax[i_plot].plot(time/ps.t_KH[i_plot], luminosity)#, color=col_list[plot_i], label=legend_list[plot_i])
                # ax.plot(time/ps.t_KH[i_plot], luminosity, label=label_list[i_plot])#, color=col_list[plot_i], label=legend_list[plot_i])
                # ax.plot(time/si.t_KH[i_plot], luminosity, label=f'Lbox = {si.box_width[i_plot]}, '+ r'$\Lambda_0$=' + f'{Lambda_fac[i_plot]}')#, color=col_list[plot_i], label=legend_list[plot_i])
                # ax.plot(time, luminosity)#, color=col_list[plot_i], label=legend_list[plot_i])


                if not B_fl and i_plot<9:

                    # L_avg = np.average(luminosity[-1250:-1000])
                    L_avg = np.average(luminosity[-250:])
                    print(f'L_avg: {L_avg}')

                    # L_avg_list.append([L_avg for i in range(len(luminosity))])
                    L_avg_list.append(L_avg)

                    # ax[i_plot].axhline(L_avg, linestyle='dashed')#,\
                    # ax.axhline(L_avg, linestyle='dashed', label=f'L_avg = {"%.4e" % L_avg}')
                          # color=col_list[plot_i],\
                        # label=r'L$_{\rm avg}$'+ f' = {np.round(L_avg,3)}')



        # ax.set_yscale('log')

        t_turb = si.box_width[i_plot]/si.v_shear
        t_cool = si.t_cool_Da

        Da = (t_turb/t_cool)[0]

        if i_plot<9:
            Da_list.append(Da)
            label_list.append(f'{Da = : .1e}')

        # if i_plot==0: 
        #     Da = (t_turb/t_cool)[0]

        # ax[i_plot].set_title(f'Box_width: {ps.box_width[i_plot]} kpc, Da = {Da}')
        # ax[i_plot].set_xlabel('time (Myr)')
        # ax[i_plot].set_ylabel('Luminosity')

        print(f'Box_width: {si.box_width[i_plot]} kpc, Da = {Da}')

        # ax.set_title(f'Box_width: {ps.box_width[0]} kpc, Da = {Da}')
        # ax.set_title(f'Da = {np.round(Da,3)}')

        # ax.set_xlabel('time (Myr)')
        # ax.set_ylabel('Luminosity')

        # ax[i,j].set_ylim(0.99,1)

        # ax[i].set_title(r"$\mathcal{M}_{\rm a}$"+f" = {ps.Ma[j]}; " + r"t$_{\rm cool}$/t$_{\rm KH}$" + f" = {tcool_tKH}" + f"; Da = {np.round(Da, 3)}")#+f"\n {setup_name}")
        
        # plt.legend(fontsize=12)


fig, ax  = p2l.plot_multiline(x_data_list, y_data_list,\
                              cmap='plasma',\
                              color_list=col_list, label_list=label_list)

# fig, ax  = p2l.plot_multiline(x_data_list, L_avg_list,\
#                               cmap='plasma', linestyle='dashed',\
#                               color_list=col_list, \
#                               new_fig=False, fig=fig, ax=ax)

ax.legend(loc='lower right')
ax.set_xlim(0,12)
# ax.set_ylim(0,1e-5)k

ax.set_yscale('log')

ax.set_xlabel(r'$t/t_{\rm KH}$')
ax.set_ylabel(r'$Q$ (code units)')

#%%

Da_list = np.array(Da_list)

plt.figure()

plt.scatter(Da_list, L_avg_list)
plt.plot(Da_list, 1.65e-6*Da_list**0.5 , linestyle='dashed', color='tab:orange', label=r'$\alpha=1/2$')
plt.plot(Da_list, 1.75e-6*Da_list**0.25, linestyle='dashed', color='tab:red'   , label=r'$\alpha=1/4$')

plt.xscale('log')
plt.yscale('log')

plt.xlabel('Da')
plt.ylabel('Q (code units)')

plt.legend()

plt.show()
# plt.savefig("test.png")

#%%
