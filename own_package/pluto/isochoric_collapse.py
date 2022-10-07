#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 19:41:20 2021

@author: prateek
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

def yprime(x,y):
    return [ y[1]/(fV*(1-y[0]**dim)), -fA*y[0]**(dim-1) ]


eps = 0.0001
tend = 1
t = np.linspace(eps,tend,10000); reltol = 1e-8
global dim, fV, fA
dim = 3; fV = 4*np.pi/3; fA = 4*np.pi

# Xi = 100
# Xf = 600

method_ODE = "DOP853"; 
sol = solve_ivp(yprime, [eps,tend], [1-np.sqrt(fA/(fV*dim))*eps,-fA*eps], t_eval=t, method=method_ODE, rtol=reltol)
R_3 = sol.y[0]; Pm_3 = sol.y[1]; M_3 = fV*(1-R_3**dim)

# save_arr = np.zeros((len(R),2),dtype=float)
# save_arr[:,0] = np.array(t)
# save_arr[:,1] = np.array(R)
# np.savetxt("isochoric_collapse/R_collapse", save_arr)

dim = 2; fV = np.pi; fA = 2*np.pi

method_ODE = "DOP853"; 
sol = solve_ivp(yprime, [eps,tend], [1-np.sqrt(fA/(fV*dim))*eps,-fA*eps], t_eval=t, method=method_ODE, rtol=reltol)
R_2 = sol.y[0]; Pm_2 = sol.y[1]; M_2 = fV*(1-R_2**dim)
save_arr = np.zeros((len(R_2),2),dtype=float)
save_arr[:,0] = np.array(t)
save_arr[:,1] = np.array(R_2)
# np.savetxt("isochoric_collapse/R_collapse", save_arr)

plt.figure(figsize=(10,10))

plt.axhline(0.0, color = 'k',linewidth = 5, linestyle='dotted')
plt.plot(t, R_2, '-', label='2D shell radius',color = 'tab:orange', linewidth = 3)
plt.plot(t, M_2,'-', label='2D shell mass', color = 'tab:blue',linewidth = 5)
plt.plot(t,Pm_2, '-', label='2D shell momentum', color = 'tab:green',linewidth = 5)
plt.plot(t, R_3, '--', label='3D variables', color = 'tab:orange',linewidth = 5)
plt.plot(t, M_3,'--', color = 'tab:blue',linewidth = 5)
plt.plot(t,Pm_3, '--', color = 'tab:green',linewidth = 5)
plt.legend(fontsize=15)
plt.title(r'Collapse of a 2D and 3D shell in isochoric regime',fontsize=18)
plt.xlabel(r'$\tilde{t}$',fontsize=18)
plt.tick_params(labelsize=18)
plt.ylabel('Dimensionless shell variables',fontsize=18)
# plt.grid()

# plt.ylim(-1.0,1.0)

# plt.savefig("shell_collapse.png")
# plt.show()
