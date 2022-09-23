#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:05:42 2019

@author: hitesh
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

import os
cwd = os.path.dirname(__file__)
repo_abs_path = cwd[:-len(cwd.split('/')[-1])]

CONST_amu = 1.66053886e-24
UNIT_DENSITY = 1.66053886e-24
UNIT_VELOCITY = 1.e8
UNIT_LENGTH = 3.0856775807e18  * 1.e5
unit_q = UNIT_DENSITY*np.power(UNIT_VELOCITY,3.0)
unit_q = unit_q / UNIT_LENGTH

CONST_kB = 1.3806505e-16
KELVIN = UNIT_VELOCITY*UNIT_VELOCITY*CONST_amu/CONST_kB

ul = 100 # in kpc
uv = 1.0E+8 # in cm/s
ut = ((ul * 3.086E+21)/uv)  # in s
ut = (ut / 3.154e+13)    # in Myr

uv = 1.022  # in kpc/Myr

# ut = 100 # in Myr
# t = 2.0 * ut  # in Myr
# dt = 1.0 # in Myr

gamma = 5./3.

CONST_kB = 1.3806505e-16
KELVIN = UNIT_VELOCITY*UNIT_VELOCITY*CONST_amu/CONST_kB

global T_tab, A, B, l


D = np.loadtxt(f'{repo_abs_path}cooling/CT_WSS09.dat')
T_tab = D[:,0]
A = D[:,1]
B = D[:,2]
l=np.size(T_tab)

def InterpAB(T):
    i=0; j=l-1
    while (i != (j-1)):
        mid = int((i+j)/2)
        T_mid = T_tab[mid]
        
        if (T > T_mid):
            i = mid
        if (T < T_mid):
            j = mid

    Ai = A[i]
    Aj = A[j]
    
    Bi = B[i]
    Bj = B[j]
    
    Ti = T_tab[i]
    Tj = T_tab[j]
    
    dT = T_tab[j] - T_tab[i]
    
    A_intp = Ai*(Tj-T)/dT + Aj*(T-Ti)/dT;
    B_intp = Bi*(Tj-T)/dT + Bj*(T-Ti)/dT;
    
    return A_intp,B_intp

def lam(T,Z):
    A, B = np.vectorize(InterpAB)(T)
    lam_fn = A + B*Z
    
    return lam_fn

def lamT(T,Z):
    dT = 0.15*T
    lam0 = lam(T, Z)
    lam0p = lam(T+dT, Z)
      
    dlam0 = lam0p-lam0
    lamT_fn = (T/lam0)*(dlam0/dT)
    
    return lamT_fn

def lamZ(T,Z):
    dZ = 0.001
    lam0 = lam(T, Z)
    lam0p = lam(T, Z+dZ)
      
    dlam0 = lam0p-lam0
    lamZ_fn = (Z/lam0)*(dlam0/dZ)
    
    return lamZ_fn

def MMWt_mu(ZbyZsun,XbyXsun):
    Xsol = 0.7065
    Ysol = 0.2806
    Zsol = 1.-Xsol-Ysol
    Z = Zsol*ZbyZsun
    X = Xsol*XbyXsun   #(1.-Z)*Xsol/(1.-Zsol)
    Y = (1.-Z)*Ysol/(1.-Zsol)
    
    return 1./(2.*X+0.75*Y+9.*Z/16.)

def MMWt_muH(ZbyZsun,XbyXsun):
    Xsol = 0.7065
#    Ysol = 0.2806
#    Zsol = 1.-Xsol-Ysol
    
#    Z = Zsol*ZbyZsun
    X = Xsol*XbyXsun#(1.-Z)*Xsol/(1.-Zsol);
    return 1./X

## c_s and t_cool from given density, temp and metallicity ##

def cs (rho0, T, X, Z):

    p0 = rho0*T/(KELVIN*MMWt_mu(Z,X))
    cs = np.sqrt(p0/rho0) 

    return cs*uv   # in kpc/Myr

def tcool (rho0, T, X, Z):
    n_H = rho0*UNIT_DENSITY/(MMWt_muH(Z,X)*CONST_amu)
    lam_arr = lam(T,Z)
    p0 = rho0*T/(KELVIN*MMWt_mu(Z,X))
    
    q = n_H*n_H*lam_arr/unit_q
    tc = p0/(q*(gamma - 1))

    return tc*ut


def cs_tcool (rho0, T, X, Z):   

    return cs(rho0,T,X,Z) * tcool(rho0,T,X,Z)



## c_s, t_cool and t_ti from data ##

def tcool_data (D):
    n_H = D.rho*UNIT_DENSITY/(MMWt_muH(D.tr1,D.tr2)*CONST_amu)
    T = D.prs/D.rho*KELVIN*MMWt_mu(D.tr1,D.tr2)

    lam_arr = lam(T,D.tr1)
    
    q = n_H*n_H*lam_arr/unit_q
    tc = D.prs/(q*(gamma - 1))
    
    return tc*ut

def tti_data (D):
    tcool_arr = tcool_data(D)
    T = D.prs/D.rho*KELVIN*MMWt_mu(D.tr1,D.tr2)
    gamma =5./3.
    
    lamT_arr = lamT(T,D.tr1)
    
    return gamma*tcool_arr/(2-lamT_arr)
    

def cs_data (D):
    cs = np.sqrt(D.prs/D.rho)
    
    return cs*uv    # in kpc/Myr


def calc_T (D):

    return D.prs/D.rho*KELVIN*MMWt_mu(D.tr1,D.tr2)
