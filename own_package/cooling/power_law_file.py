'''
Author: Hitesh Kishore Das 
Date: 2021-10-18 13:48:12 
Last Modified by: Hitesh Kishore Das
Last Modified time: 2021-10-18 13:49:06
'''

import numpy as np
import cooling_fit_gen as cfg


def pow_file_write(filename,Lam_arr,alp_arr,T_arr):

    np.savetxt(filename,np.stack([T_arr, Lam_arr, alp_arr],axis=1))

def T_scale (lam0_fit, alp_fit, T_breaks, sim_scaling_para):

    T_min,T_max = T_breaks[0],T_breaks[-1]
    Lam_min,Lam_max = np.min(lam0_fit), np.max(lam0_fit)

    alp_new_fit = alp_fit * np.log10( sim_scaling_para[3]/sim_scaling_para[2] ) \
        /np.log10(Lam_max/Lam_min)

    alp_new_fit = alp_fit * np.log10(T_min/T_max)  \
        / np.log10( sim_scaling_para[1]/sim_scaling_para[0] )

    lam0_new_fit = np.log10( sim_scaling_para[3]/sim_scaling_para[2] )\
        * np.log10(lam0_fit/Lam_min)/np.log10(Lam_max/Lam_min)\
        + np.log10(sim_scaling_para[2])

    lam0_new_fit = 10**lam0_new_fit

    T_new_fit = np.log10( sim_scaling_para[1]/sim_scaling_para[0] )\
        * np.log10(T_breaks/T_min)/np.log10(T_max/T_min)\
        + np.log10(sim_scaling_para[0])

    T_new_fit = 10**T_new_fit

    return lam0_new_fit,alp_new_fit,T_new_fit

if __name__=='__main__':

    from matplotlib import pyplot as plt

    N_bin = 5
    bin_n = 100
    Z = 1.0

    T_floor_sim = 0.1
    T_max_sim = 1.0

    alp = -0.46
    Lam_max_sim = 100
    Lam_floor_sim = Lam_max_sim*(T_max_sim/T_floor_sim)**alp

    sim_scaling_para = np.array([T_floor_sim,T_max_sim,Lam_floor_sim,Lam_max_sim])

    lam0_fit, alp_fit, T_breaks = cfg.power_fit_cont(N_bin,bin_n,Z)

    # lam0_new_fit,alp_new_fit,T_new_fit = T_scale (lam0_fit, alp_fit, T_breaks, sim_scaling_para)
    lam0_new_fit,alp_new_fit,T_new_fit = lam0_fit,alp_fit,T_breaks

    # Turn the lam0 value into log scale

    # lam0_new_fit = np.log10(lam0_new_fit)

    plt.figure()
    plt.xscale('log')
    plt.yscale('log')
    
    # plt.plot(T_new_fit,10**lam0_new_fit)
    plt.plot(T_new_fit,lam0_new_fit)

    for T in T_new_fit:
        plt.axvline(T)

    pow_file_write("power_law_fit_Z_"+str(Z)+".txt",lam0_new_fit,alp_new_fit,T_new_fit)

