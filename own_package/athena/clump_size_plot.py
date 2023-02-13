'''
Created Date: 2023-02-06 16:25:16
Author: Hitesh Das

To plot clump size plot 
'''

import numpy as np
import scipy as sp
import sys
import os
import gc
import pickle as pk

import matplotlib as mt
import matplotlib.pyplot as plt

import own_package.plot.plot_2d_line as p2l
import own_package.plot.plot_histogram as ph
import own_package.plot.legend as leg

import own_package.utils.units as un


import own_package
from sympy import O
package_path = os.path.dirname(own_package.__file__)
print(f"own_package path: {package_path}")


file_path = os.path.dirname(__file__)
print(f'{file_path = }')

sim_list   = []
label_list = []
dx_lsh_list = []

sim_list += ['Rlsh_1000_res_256_M_0.5_hydro/']
sim_list += ['Rlsh_1000_res_256_M_0.5_beta_100/']

dx_lsh_list += [1000*40/256] * 2

label_list += [r'R/$l_{\rm shatter}$ = 1000, $\mathcal{M}$ = 0.5']
label_list += [r'R/$l_{\rm shatter}$ = 1000, $\mathcal{M}$ = 0.5, MHD']

sim_list += ['Rlsh_250_res_256_M_0.5_hydro/']
sim_list += ['Rlsh_250_res_256_M_0.5_beta_100/']

dx_lsh_list += [250*40/256] * 2

label_list += [r'R/$l_{\rm shatter}$ = 250, $\mathcal{M}$ = 0.5']
label_list += [r'R/$l_{\rm shatter}$ = 250, $\mathcal{M}$ = 0.5, MHD']

sim_list += ['Rlsh_250_res_256_M_0.25_hydro/']
sim_list += ['Rlsh_250_res_256_M_0.25_beta_100/']

dx_lsh_list += [250*40/256] * 2

label_list += [r'R/$l_{\rm shatter}$ = 250, $\mathcal{M}$ = 0.25']
label_list += [r'R/$l_{\rm shatter}$ = 250, $\mathcal{M}$ = 0.25, MHD']

# N_snap = 501
N_snap = 600
Tcut = 8e4

def clump_elongation_hist(fig, ax, file_ind = 0, theme='bright', norm=False, kwargs={}, bar_args={}):

    style_lib  = f'{package_path}/plot/style_lib/' 

    if theme=='dark':
        pallette   = style_lib + 'dark_pallette.mplstyle'
    else:
        pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'
    
    plt.style.use([pallette, plot_style, text_style])
    
    line_border_color = mt.rcParams['lines.color']
    fig_face_color = mt.rcParams['figure.facecolor']


    bin_elongation_arr = np.linspace(1, 7, num=50)

    #* Read the saved plot_dict for vturb values
    with open(f'{file_path}/save_arr/clump_size/{sim_list[file_ind]}clump_Tcut_{int(Tcut)}_Nsnap_{N_snap}.pkl', 'rb') as f:
        clump_dict = pk.load(f)

    elongation = []

    for i in range(clump_dict['n_blob']):
        if len(clump_dict['clump_dict'][i])!=0:
            clump_size = clump_dict['clump_dict'][i]['clump_size']
            clump_size = np.sort(np.array(clump_size))
        else:
            clump_size = np.array([0,0,0])

        elongation.append((clump_size[2]+1)/(clump_size[1]+1))

    elongation = np.array(elongation)

    norm = clump_dict['n_blob']

    bar_args0 = dict(bar_args, **{'color':f'C{file_ind%2 + 4}', 'alpha': 0.3, 'label': bar_args['label']+r': $N_{\rm blob} = $' + f"{clump_dict['n_blob']}"}); 
    fig, ax = ph.plot_histogram_1d(elongation, norm=norm, bins=bin_elongation_arr, \
                                    fig=fig, ax=ax, new_fig=False, \
                                    bar_args = bar_args0, kwargs=kwargs )
 
    ax.set_yscale('log')

    ax.set_xlim(0.8,7.1)
    ax.set_ylim(1e-3,1)

    if __name__=='__main__':

        ax.legend(loc='upper right')
        # leg.add_legend([{'linestyle' : 'solid', 'label' : r'$N_{clump} = $'+f'{clump_dict["n_blob"]}' }], ax=ax,
        #                 legend_loc  = 'upper right' , \
        #                 legend_type = 'line'      , \
        #                 default_plot_args = {'color' : fig_face_color})

    return ax

def clump_elongation_calculation(file_ind = 0, volume_cut = 0.0, pair_flag=True):

    elongation = [[],[]]

    for rep in range(pair_flag+1):

        #* Read the saved plot_dict for vturb values
        with open(f'{file_path}/save_arr/clump_size/{sim_list[file_ind+rep]}clump_Tcut_{int(Tcut)}_Nsnap_{N_snap}.pkl', 'rb') as f:
            clump_dict = pk.load(f)

        # Loop over the clumps
        for i in range(clump_dict['n_blob']):

            if clump_dict['clump_dict'][i]['clump_volume']>volume_cut:

                clump_size = clump_dict['clump_dict'][i]['clump_size']
                clump_size = np.sort(np.array(clump_size))

                # Calculate elongation
                elongation[rep].append(clump_size[2]/clump_size[1])

        elongation[rep] = np.array(elongation[rep])

    return elongation

def clump_volume_deficit(file_ind = 0, volume_cut = 0.0):

    volume_deficit = []


    #* Read the saved plot_dict for vturb values
    with open(f'{file_path}/save_arr/clump_size/{sim_list[file_ind]}clump_Tcut_{int(Tcut)}_Nsnap_{N_snap}.pkl', 'rb') as f:
        clump_dict = pk.load(f)

    # Loop over the clumps
    for i in range(clump_dict['n_blob']):

        if clump_dict['clump_dict'][i]['clump_volume']>volume_cut:

            # Volume of the ellipsoid around the clump
            ellipsoid_vol = clump_dict['clump_dict'][i]['clump_size']
            ellipsoid_vol = np.product(np.array(ellipsoid_vol)) * (4/3) * np.pi

            # Actual clump volume
            clump_vol = clump_dict['clump_dict'][i]['clump_volume']

            # Calculate volume deficit
            volume_deficit.append((ellipsoid_vol - clump_vol)/ellipsoid_vol)

    volume_deficit = np.array(volume_deficit)

    return volume_deficit

def clump_network_length(file_ind = 0):

    length_list = []

    #* Read the saved plot_dict for vturb values
    with open(f'{file_path}/save_arr/clump_size/{sim_list[file_ind]}clump_network_Nsnap_{N_snap}.pkl', 'rb') as f:
        clump_dict = pk.load(f)

    # Loop over the clumps
    # for i in range(clump_dict['n_blob']):

    #         length_list.append(clump_dict['clump_dict'][i])

    return np.array(clump_dict['clump_dict'])
    
def clump_elongation_percentile(fig, ax, file_ind = 0, volume_cut=0.0, **kwargs):

    bin_elongation_arr = np.linspace(1, 7, num=50)

    elongation = clump_elongation_calculation(file_ind, volume_cut=volume_cut)

    hst_0 = ph.plot_histogram_1d(elongation[0], bins=bin_elongation_arr, return_hist=True, with_fig=False)
    hst_1 = ph.plot_histogram_1d(elongation[1], bins=bin_elongation_arr, return_hist=True, with_fig=False)

    bin_a = 0

    ax.plot(hst_0[1][bin_a:-1], np.cumsum(hst_0[0][bin_a:])/np.sum(hst_0[0][bin_a:]), label='HD ', **kwargs)
    ax.plot(hst_1[1][bin_a:-1], np.cumsum(hst_1[0][bin_a:])/np.sum(hst_1[0][bin_a:]), label='MHD', **kwargs)

    ax.set_xlabel('Anisotropy')
    ax.set_ylabel('Cumulative/N_clumps')

    ax.legend()

    return ax

def clump_length_hist(fig, ax, file_ind = 0, theme='bright', norm=False, bar_args={}):


    style_lib  = f'{package_path}/plot/style_lib/' 

    if theme=='dark':
        pallette   = style_lib + 'dark_pallette.mplstyle'
    else:
        pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'
    
    plt.style.use([pallette, plot_style, text_style])
    
    line_border_color = mt.rcParams['lines.color']
    fig_face_color = mt.rcParams['figure.facecolor']

    bin_arr = np.logspace(1, np.log10(400), num=25) #*dx_lsh_list[file_ind]
    # bin_arr = np.linspace(0, 400, num=50) #*dx_lsh_list[file_ind]

    clump_length = (clump_network_length(file_ind)+1) #*dx_lsh_list[file_ind]

    # bar_args0 = dict(bar_args, **{'color':f'C1', 'alpha': 0.2, 'label': bar_args['label']+': Shortest'}) 
    fig, ax = ph.plot_histogram_1d(clump_length, bins=bin_arr,\
                                    fig=fig, ax=ax, new_fig=False, bar_args=bar_args) # h, \
                                    # bar_args = bar_args0, kwargs=kwargs)

 
    # ax.set_yscale('log')
    ax.set_xscale('log')

    ax.set_ylim(5e-1, 1e2)
    # if file_ind in [0,1]:
    #     ax.set_xlim(1e2 , 1e5)
    # elif file_ind in [2,3]:
    #     ax.set_xlim(1e1 , 1e4)
    # else:
    #     ax.set_xlim(1e1 , 5e4)


    if __name__=='__main__':
        ax.legend()
    #     leg.add_legend([{'linestyle' : 'solid', 'label' : r'$N_{clump} = $'+f'{clump_dict["n_blob"]}' }], ax=ax,
    #                     legend_loc  = 'upper left' , \
    #                     legend_type = 'line'      , \
    #                     default_plot_args = {'color' : fig_face_color}, \
    #                     frameon = False , bbox_to_anchor=(0.275 , 1.04))

    return ax

def clump_size_hist(fig, ax, file_ind = 0, theme='bright', norm=False, kwargs={}, bar_args={}):


    style_lib  = f'{package_path}/plot/style_lib/' 

    if theme=='dark':
        pallette   = style_lib + 'dark_pallette.mplstyle'
    else:
        pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'
    
    plt.style.use([pallette, plot_style, text_style])
    
    line_border_color = mt.rcParams['lines.color']
    fig_face_color = mt.rcParams['figure.facecolor']

    bin_arr = np.logspace(0, np.log10(500), num=50)*dx_lsh_list[file_ind]

    #* Read the saved plot_dict for vturb values
    with open(f'{file_path}/save_arr/clump_size/{sim_list[file_ind]}clump_Tcut_{int(Tcut)}_Nsnap_{N_snap}.pkl', 'rb') as f:
        clump_dict = pk.load(f)

    clump_list_0 = []
    clump_list_1 = []
    clump_list_2 = []

    for i in range(clump_dict['n_blob']):
        if len(clump_dict['clump_dict'][i])!=0:
            clump_size = clump_dict['clump_dict'][i]['clump_size']
            clump_size = np.sort(np.array(clump_size))
        else:
            clump_size = np.array([0,0,0])

        clump_list_0.append(clump_size[0]+1)
        clump_list_1.append(clump_size[1]+1)
        clump_list_2.append(clump_size[2]+1)

    clump_list_0 = np.array(clump_list_0)*dx_lsh_list[file_ind]
    clump_list_1 = np.array(clump_list_1)*dx_lsh_list[file_ind]
    clump_list_2 = np.array(clump_list_2)*dx_lsh_list[file_ind]

    bar_args0 = dict(bar_args, **{'color':f'C1', 'alpha': 0.2, 'label': bar_args['label']+': Shortest'}) 
    fig, ax = ph.plot_histogram_1d(clump_list_0, bins=bin_arr,\
                                    fig=fig, ax=ax, new_fig=False, \
                                    bar_args = bar_args0, kwargs=kwargs)

    bar_args1 = dict(bar_args, **{'color':f'C2', 'alpha': 0.4, 'label': bar_args['label']+': Intermediate'}) 
    fig, ax = ph.plot_histogram_1d(clump_list_1, bins=bin_arr,\
                                    fig=fig, ax=ax, new_fig=False, \
                                    bar_args = bar_args1, kwargs=kwargs)

    bar_args2 = dict(bar_args, **{'color':f'C3', 'alpha': 0.6, 'label': bar_args['label']+': Longest'})  
    fig, ax = ph.plot_histogram_1d(clump_list_2, bins=bin_arr,\
                                    fig=fig, ax=ax, new_fig=False, \
                                    bar_args = bar_args2, kwargs=kwargs)
 
    ax.set_yscale('log')
    ax.set_xscale('log')

    # ax.set_ylim(5e-4, 1e-1)
    if file_ind in [0,1]:
        ax.set_xlim(1e2 , 1e5)
    elif file_ind in [2,3]:
        ax.set_xlim(1e1 , 1e4)
    else:
        ax.set_xlim(1e1 , 5e4)


    if __name__=='__main__':
        ax.legend()
        leg.add_legend([{'linestyle' : 'solid', 'label' : r'$N_{clump} = $'+f'{clump_dict["n_blob"]}' }], ax=ax,
                        legend_loc  = 'upper left' , \
                        legend_type = 'line'      , \
                        default_plot_args = {'color' : fig_face_color}, \
                        frameon = False , bbox_to_anchor=(0.275 , 1.04))

    return ax

def clump_size_2D_hist(fig, ax, file_ind = 0, theme='bright', norm=False, kwargs={}, bar_args={}):


    style_lib  = f'{package_path}/plot/style_lib/' 

    if theme=='dark':
        pallette   = style_lib + 'dark_pallette.mplstyle'
    else:
        pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'
    
    plt.style.use([pallette, plot_style, text_style])
    
    line_border_color = mt.rcParams['lines.color']
    fig_face_color = mt.rcParams['figure.facecolor']

    bin_arr = np.logspace(0, np.log10(500), num=30)*dx_lsh_list[file_ind]

    #* Read the saved plot_dict for vturb values
    with open(f'{file_path}/save_arr/clump_size/{sim_list[file_ind]}clump_Tcut_{int(Tcut)}_Nsnap_{N_snap}.pkl', 'rb') as f:
        clump_dict = pk.load(f)

    clump_list_ab = []

    for i in range(clump_dict['n_blob']):
        if len(clump_dict['clump_dict'][i])!=0:
            clump_size = clump_dict['clump_dict'][i]['clump_size']
            clump_size = np.sort(np.array(clump_size))
        else:
            clump_size = np.array([0,0,0])

        clump_list_ab.append([clump_size[1]+1, clump_size[2]+1])

    clump_list_ab = np.array(clump_list_ab)*dx_lsh_list[file_ind]

    norm = clump_dict['n_blob']

    # bar_args1 = dict(bar_args, **{'color':f'C2', 'alpha': 0.4, 'label': bar_args['label']+': Intermediate'}) 
    fig, ax = ph.plot_histogram_2d(clump_list_ab[:,0],clump_list_ab[:,1], bins=bin_arr,\
                                    fig=fig, ax=ax, new_fig=False, hist_log=True,\
                                    kwargs=kwargs, color_range=[1e0, 1e3])

    ax.plot(bin_arr, bin_arr, color='gray', linestyle='dashed')

    ax.set_xlabel('Intermediate axis length')
    ax.set_ylabel('Longest axis length')
 
    ax.set_yscale('log')
    ax.set_xscale('log')
# 
    ax.set_ylim(None, 1e3)
    # if file_ind in [0,1]:
    #     ax.set_xlim(1e2 , 1e5)
    # elif file_ind in [2,3]:
    #     ax.set_xlim(1e1 , 1e4)
    # else:
    #     ax.set_xlim(1e1 , 5e4)


    if __name__=='__main__':
        # ax.legend()
        leg.add_legend([{'linestyle' : 'solid', 'label' : bar_args['label']+r': $N_{clump} = $'+f'{clump_dict["n_blob"]}' }], ax=ax,
                        legend_loc  = 'lower right' , \
                        legend_type = 'line'      , \
                        default_plot_args = {'color' : fig_face_color}, \
                        frameon = False )

    return ax

def clump_elongation_volume_2D_hist(fig, ax, file_ind = 0, num=20, volume_cut=0.0, theme='bright', **kwargs):


    style_lib  = f'{package_path}/plot/style_lib/' 

    if theme=='dark':
        pallette   = style_lib + 'dark_pallette.mplstyle'
    else:
        pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'
    
    plt.style.use([pallette, plot_style, text_style])
    
    line_border_color = mt.rcParams['lines.color']
    fig_face_color = mt.rcParams['figure.facecolor']

    elongation = clump_elongation_calculation(file_ind, volume_cut=volume_cut, pair_flag=False)

    clump_volume = []

    #* Read the saved plot_dict for vturb values
    with open(f'{file_path}/save_arr/clump_size/{sim_list[file_ind]}clump_Tcut_{int(Tcut)}_Nsnap_{N_snap}.pkl', 'rb') as f:
        clump_dict = pk.load(f)

    for i in range(clump_dict['n_blob']):
        clump_vol = clump_dict['clump_dict'][i]['clump_volume']
        if clump_vol>volume_cut:
            clump_volume.append(clump_vol)

    clump_volume = np.array(clump_volume) # *(dx_lsh_list[file_ind]**3)
    # print(f"{clump_volume = }")
    # print(f"{elongation[0] = }")

    elong_bins = np.linspace(1,7, num=num)
    vol_bins   = np.logspace(np.log10(volume_cut),5, num=num)

    fig, ax = ph.plot_histogram_2d(clump_volume, elongation[0], bins=[vol_bins, elong_bins],\
                                    fig=fig, ax=ax, new_fig=False, \
                                    **kwargs)

    # ax.plot(bin_arr, bin_arr, color='gray', linestyle='dashed')

    ax.set_xlabel('Clump volume')
    ax.set_ylabel('Elongation')
 
    # ax.set_yscale('log')
    ax.set_xscale('log')
# 
    # ax.set_ylim(None, 1e3)
    # if file_ind in [0,1]:
    #     ax.set_xlim(1e2 , 1e5)
    # elif file_ind in [2,3]:
    #     ax.set_xlim(1e1 , 1e4)
    # else:
    #     ax.set_xlim(1e1 , 5e4)



    return ax

if __name__=='__main__':

    # theme='dark'
    theme='bright'
# 
    style_lib  = f'{package_path}/plot/style_lib/' 

    if theme=='dark':
        pallette   = style_lib + 'dark_pallette.mplstyle'
    else:
        pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'
    
    plt.style.use([pallette, plot_style, text_style])
    
    line_border_color = mt.rcParams['lines.color']
    fig_face_color = mt.rcParams['figure.facecolor']

    # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10,8) )

    # sim_type = 0

    # ax[0] = clump_size_hist(fig, ax[0], theme=theme, file_ind=sim_type  , bar_args={'label': 'HD'} )# , kwargs={'normed':True})
    # ax[1] = clump_size_hist(fig, ax[1], theme=theme, file_ind=sim_type+1, bar_args={'label': 'MHD'})# , kwargs={'normed':True})

    # ax[1].set_xlabel(r"Clump dimension (in $l_{\rm shatter}$)")
    # ax[0].set_ylabel(r"Frequency")
    # ax[1].set_ylabel(r"Frequency")

    # ax[0].set_title(label_list[sim_type])

    # plt.show()

    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8) )

    # sim_type = 0

    # ax = clump_elongation_hist(fig, ax, theme=theme, file_ind=sim_type  , bar_args={'label': 'HD  '})
    # ax = clump_elongation_hist(fig, ax, theme=theme, file_ind=sim_type+1, bar_args={'label': 'MHD'})

    # ax.set_xlabel(r"Elongation ($a/b$)")
    # ax.set_ylabel(r"Frequency/$N_{\rm clump}$")

    # ax.set_title(label_list[sim_type])

    # plt.show()

    # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,15) )

    # sim_type = 0

    # ax[0] = clump_size_2D_hist(fig, ax[0], theme=theme, file_ind=sim_type  , bar_args={'label': 'HD  '})
    # ax[1] = clump_size_2D_hist(fig, ax[1], theme=theme, file_ind=sim_type+1, bar_args={'label': 'MHD'})

    # plt.show()

    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8) )

    # sim_type = 1

    # if sim_type%2==0:
    #     ax = clump_size_2D_hist(fig, ax, theme=theme, file_ind=sim_type  , bar_args={'label': 'HD  '})
    # else:
    #     ax = clump_size_2D_hist(fig, ax, theme=theme, file_ind=sim_type  , bar_args={'label': 'MHD  '})

    # if sim_type%2==0:
    #     ax.set_title(label_list[sim_type]+', HD')
    # else:
    #     ax.set_title(label_list[sim_type]+', MHD')

    # plt.show()
    


    # elongation = clump_elongation_calculation(2)
    # kstest = sp.stats.kstest(elongation[0][:102],elongation[1][:41])
    # print(kstest)


    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8) )

    # sim_type = 0

    # ax = clump_elongation_percentile(fig, ax, file_ind=sim_type, volume_cut=64.0, linestyle='dotted' )
    # ax = clump_elongation_percentile(fig, ax, file_ind=sim_type, volume_cut=125.0, linestyle='dashed')
    # ax = clump_elongation_percentile(fig, ax, file_ind=sim_type, volume_cut=216.0, linestyle='solid')

    # plt.show()

    # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,15) )

    # sim_type = 0*2

    # ax[0] = clump_elongation_volume_2D_hist(fig, ax[0], num=25, volume_cut=10**3, file_ind=sim_type)
    # ax[1] = clump_elongation_volume_2D_hist(fig, ax[1], num=25, volume_cut=10**3, file_ind=sim_type+1)

    # plt.show()

    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8) )

    # ax.hist(clump_volume_deficit(file_ind=1, volume_cut=4**3), bins=25, density=True, alpha=0.3, label='MHD')
    # ax.hist(clump_volume_deficit(file_ind=0, volume_cut=4**3), bins=25, density=True, alpha=0.3, label='HD')

    # ax.set_yscale('log')
    # ax.legend()

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8) )

    sim_type = 0 * 2

    ax = clump_length_hist(fig, ax, file_ind=sim_type+1, bar_args={'color':'C1', 'alpha':0.5, 'label':'MHD'})
    ax = clump_length_hist(fig, ax, file_ind=sim_type  , bar_args={'color':'C2', 'alpha':0.5, 'label':'HD '})

    ax.set_yscale('log')

    ax.set_xlabel('Longest shortest path in nbrhood graph \n(in grid cells)')
    ax.set_ylabel('Frequency')

    ax.set_title(label_list[sim_type])

    ax.set_xlim(10, 400)

    ax.legend()

    plt.show()

    #TODO: Visualise the clumps!!
    #TODO: Everything seems mostly empty!