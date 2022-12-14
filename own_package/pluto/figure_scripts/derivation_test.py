'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-20 16:03:09 
'''

import numpy as np
import pickle as pk
import os
import sys
import gc

import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

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


# x_data_list   = []
# y_data_list   = []

fitx_data_list = []
fity_data_list = []

col_data_list = []
label_list    = []

m_dot_data    = []
time_data     = []

xfit = np.linspace(0.25,2.0,num=100)

for i_wd, wd in enumerate(si.wdir_list):

    try:
        with open(f'{package_abs_path}pluto/save_arr/{si.file_list[i_wd]}/{si.file_list[i_wd]}_evolution.pkl', 'rb') as f:
            sim_data = pk.load(f)
    except:
        continue

    x_data = sim_data['time']/si.t0[i_wd]    
    # y_data = sim_data['cold_gas']/si.M0[i_wd] - 1.0
    y_data = (sim_data['cold_gas'] - si.M0[i_wd])/si.V[i_wd]
    # y_data /= si.Chi_f[i_wd]**(1/2)
    # y_data /= si.R_list[i_wd] ** (1/12)

    bound  = x_data>0.25
    bound *= x_data<3.25
    bound  = np.argwhere(bound)


    fit = np.polyfit(x_data[bound][:,0],y_data[bound][:,0], deg=5)




    fitx_data_list.append(xfit)
    fity_data_list.append(np.polyval(fit,xfit))

    # x_data_list.append(x_data[1:])
    # y_data_list.append(y_data[1:])
    # col_data_list.append(np.log10(si.R_list[i_wd]))
    col_data_list.append(si.N_list[i_wd])
    label_list.append(si.label_list[i_wd])

    # t_fit.append(np.linspace(0,3.0,num=50))
    # m_dot_fit.append( mdot[i_wd]*(t_fit[i_wd]-0.25) + mb[i_wd] )

    # m_dot = np.roll(y_data_list[i_wd],-1) - y_data_list[i_wd]
    # m_dot /= (np.roll(x_data_list[i_wd],-1) - x_data_list[i_wd])

    # m_dot_data.append(m_dot*si.M0[i_wd]/si.t0[i_wd])
    # time_data.append(x_data_list[i_wd])


# fig, ax = p2l.plot_multiline(x_data_list, y_data_list, \
#                              color_list=col_data_list, \
#                              label_list=label_list, \
#                              cmap='viridis')#, mark_flag = True, markevery=5)

# fig, ax = p2l.plot_multiline(fitx_data_list, fity_data_list, \
#                              color_list=col_data_list, \
#                             #  label_list=label_list, \
#                              cmap='viridis', linestyle='dashed', \
#                              new_fig=False, fig=fig, ax=ax)

fig, ax = p2l.plot_multiline(fitx_data_list, fity_data_list, \
                             color_list=col_data_list, \
                             label_list=label_list, \
                             cmap='viridis', linestyle='solid')


ax.set_xlim(0.5, 3.0 )
ax.set_ylim(-0.1,2)
# ax.set_ylim(0,0.05)

# ax.set_yscale('log')
# ax.set_xscale('log')

ax.axvline(si.t_collapse, linestyle='dotted', color='k')

ax.set_xlabel(r'$\tilde{t}$')
ax.set_ylabel(r'$\Delta M_{\rm cold}/V_{\rm 0,cloud}$')

ax.legend()
plt.show()



plt.figure()

for i_t, t_arr in enumerate(fitx_data_list):


    if i_t not in [0,4]:
        plt.scatter(si.R_list[i_t]*g.ul*np.ones_like(fity_data_list[i_t]), fity_data_list[i_t]/fity_data_list[0],  \
                # color=col_data_list[i_t], \
                label=f'{label_list[i_t]}')


R_arr = np.logspace(-5,0, num=50)

plt.plot(R_arr*g.ul, 4.5 * ((R_arr*g.ul)**(1/12)), color='tab:red', linestyle='dashed',\
         label=r'$R^{1/12}$')

plt.yscale('log')
plt.xscale('log')

plt.xlabel(r'$R_{\rm cloud}$ (kpc)')
plt.ylabel(r'$\frac{\Delta M/V}{(\Delta M/V)_{R1}}$', rotation=0)

plt.ylim(2,10)

plt.legend()


plt.figure()

for i_t, t_arr in enumerate(fitx_data_list):


    if i_t in [1,4]:
        plt.scatter(si.Chi_list[i_t]*np.ones_like(fity_data_list[i_t]), fity_data_list[i_t]/fity_data_list[0],  \
                # color=col_data_list[i_t], \
                label=f'{label_list[i_t]}')


Chi_arr = np.logspace(1, 2.5, num=50)

plt.plot(Chi_arr, 0.3 * (Chi_arr**(1/2)), color='tab:red', linestyle='dashed', label=r'$\chi_{\rm f}^{1/2}$')

plt.yscale('log')
plt.xscale('log')

plt.ylabel(r'$\frac{\Delta M/V}{(\Delta M/V)_{R1}}$', rotation=0)
plt.xlabel(r'$\chi_{\rm f}$')

plt.legend()



def yprime(x,y):
    return [ y[1]/(fV*(1-y[0]**dim)), -fA*y[0]**(dim-1) ]
eps = 0.0001
tend = 2
t = np.linspace(eps,tend,10000); reltol = 1e-8
dim = 2; fV = np.pi; fA = 2*np.pi

method_ODE = "DOP853"; 
sol = solve_ivp(yprime, [eps,tend], [1-np.sqrt(fA/(fV*dim))*eps,-fA*eps], t_eval=t, method=method_ODE, rtol=reltol)
R_2 = sol.y[0]; Pm_2 = sol.y[1]; M_2 = fV*(1-R_2**dim)

Rp_fit = np.polyfit(t,R_2, deg=1)
Rp_arr = np.abs(np.polyval(Rp_fit,xfit))


H2_list = []
K_list = []
Kdot_list = []

dt = xfit[1] - xfit[0]

alpha = 0.1

plt.figure()
for i_t, t_arr in enumerate(fitx_data_list):

    K = fity_data_list[i_t]/(si.R_list[i_t]**(1/12))
    K /= si.Chi_list[i_t]**(1/2)

    Kdot = np.diff(K)/dt
    # Kdot = np.abs(Kdot)

    H = Kdot * (Rp_arr[:-1]**(1-dim)) / (fA*fV*si.rho_amb)
    H /= alpha
    H2 = H**2

    H2_list.append(H2)
    K_list.append(K)
    Kdot_list.append(Kdot)

    plt.plot(xfit[:-1], H2, label = si.label_list[i_t])
    # plt.plot(xfit, K, label = si.label_list[i_t])

plt.yscale('log')

plt.xlim(0.25, 1.5)
plt.ylim(1e-3, 1e3)

plt.legend()

