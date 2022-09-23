'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-14 10:03:08 
'''

import numpy as np
import os
import sys
import gc


cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}pluto/')
import pyPLUTO
import pyPLUTO.pload as pp
import units as un


def get_array(N, dir_name, fields, \
              dim=2, MHD_flag = False  ,\
              nlast_flag=True):

    x_dim = {
                1 : ['x1'], 
                2 : ['x1', 'x2'], 
                3 : ['x1', 'x2', 'x3'] 
    }
    
    nlinf = pyPLUTO.nlast_info(w_dir=dir_name)
    D = pp.pload(N, w_dir=dir_name)

    # Define scope for eval(), uses global scope by default
    scope=locals()

    out_dict = {}

    out_dict['time'] = D.SimTime

    if nlast_flag:
        out_dict['nlast'] = nlinf.get('nlast')


    if "coord" in fields:

        coord_dim = ['D.' +xd for xd in x_dim[dim]]
        dx_dim    = ['D.d'+xd for xd in x_dim[dim]]

        out_dict['coord'] = [ eval(cd, scope) for cd in coord_dim]
        out_dict['dx']    = [ eval(dd, scope) for dd in dx_dim   ]

        # # x_arr = D.x1
        # # y_arr = D.x2
        # # z_arr = D.x3
        # r_arr = [x_arr,y_arr,z_arr]


    if "rho" in fields:
        out_dict['rho'] = D.rho

    if "prs" in fields:
        out_dict['prs']   = D.prs

    if "temp" in fields:
        prs_arr    = D.prs
        rho_arr    = D.rho

        out_dict['temp'] = (prs_arr/rho_arr) * un.KELVIN * un.mu

        del prs_arr
        del rho_arr
        gc.collect()
    
    if "vel" in fields:
        v_dim = ['D.v'+xd for xd in x_dim[dim]]
        out_dict['vel'] = [eval(vd, scope) for vd in v_dim]

    if MHD_flag and "B" in fields:
        B_dim = ['D.b'+xd for xd in x_dim[dim]]
        out_dict['B'] = [eval(bd, scope) for bd in B_dim]

    return out_dict

