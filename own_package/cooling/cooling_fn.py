'''
Author: Hitesh Kishore Das 
Date: 2021-10-18 14:23:49 
Last Modified by:   Hitesh Kishore Das 
Last Modified time: 2021-10-18 14:23:49 
'''


import numpy as np

import os
import sys

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}utils/')
import units as un

cwd = os.getcwd()
repo_abs_path = cwd[:-len(cwd.split('/')[-1])]

cooling_dir = f'{package_abs_path}cooling/'

def Lam_fn (T,Z=1.0, Lambda_fac = 1.0):

    Lam_file = np.loadtxt(cooling_dir+"CT_WSS09.dat")
    
    T_min = np.min(Lam_file[:,0])
    T_max = np.max(Lam_file[:,0])

    N = np.shape(Lam_file)[0]

    if T<T_min or T>T_max:
        return 0.0

    else:

        i_a = 0
        i_b = N-1

        while i_a!=i_b-1:

            mid = int((i_a+i_b)/2)

            if T>Lam_file[mid,0]:
                i_a = mid
            else:
                i_b = mid

        T_a = Lam_file[i_a,0]
        T_b = Lam_file[i_b,0]

        LamH_a = Lam_file[i_a,1]
        LamH_b = Lam_file[i_b,1]

        LamZ_a = Lam_file[i_a,2]
        LamZ_b = Lam_file[i_b,2]

        dT = T_b-T_a

        LamH = LamH_a*(T_b-T)/dT + LamH_b*(T-T_a)/dT
        LamZ = LamZ_a*(T_b-T)/dT + LamZ_b*(T-T_a)/dT

    return (LamH + LamZ*Z) * Lambda_fac

def Lam_fn_powerlaw(T, Lambda_fac=1.0):

    Lam_file = np.loadtxt(cooling_dir+"power_law_fit_Z_1.0.txt")
    
    T_min = np.min(Lam_file[:,0])
    T_max = np.max(Lam_file[:,0])

    N = np.shape(Lam_file)[0]

    if T<T_min or T>T_max:
        return 0.0

    else:

        i_a = 0
        i_b = N-1

        while i_a!=i_b-1:

            mid = int((i_a+i_b)/2)

            if T>Lam_file[mid,0]:
                i_a = mid
            else:
                i_b = mid

        T_a = Lam_file[i_a,0]
        T_b = Lam_file[i_b,0]

        Lam = Lam_file[i_a,1]* (T/Lam_file[i_a,0])**Lam_file[i_a,2]

        return Lam*Lambda_fac

def Lam_range():

    Lam_file = np.loadtxt("CT_WSS09.dat")
    
    T_min = np.min(Lam_file[:,0])
    T_max = np.max(Lam_file[:,0])

    return T_min, T_max


def tcool_calc(rho,T,Z=1.0, Lambda_fac = 1.0,actual_flag=False):

    n_H = rho*un.unit_density/(un.muH*un.CONST_amu)

    if actual_flag:
        lam_arr = Lam_fn(T,Z,Lambda_fac)
    else:
        lam_arr = Lam_fn_powerlaw(T,Lambda_fac)

    p = rho*T/(un.KELVIN*un.mu)  # in code units

    q = n_H*n_H*lam_arr/un.unit_q  # in code units 

    tc = p/(q*(un.g - 1))       # in code units

    return tc;  # in code units


if __name__=="__main__":

    T = 1e5
    print(Lam_fn(T))
    print(tcool_calc(1,T))