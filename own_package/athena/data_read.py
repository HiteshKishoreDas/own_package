import numpy as np
import yt
import sys
import os

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}athena/athena_vis_code/')
import athena_read as ar

sys.path.insert(0, f'{package_abs_path}utils/')
import units as un

def get_array_yt(fn, fields, MHD_flag = False):

    ds = yt.load(fn)

    all_data_level_0_hyd = ds.covering_grid(
        level=0, left_edge=[0, 0.0, 0.0], dims=ds.domain_dimensions
    )

    out_dict = {}

    if "coord" or "all" in fields:
        x_arr = np.array(all_data_level_0_hyd[('gas','x')])
        y_arr = np.array(all_data_level_0_hyd[('gas','y')])
        z_arr = np.array(all_data_level_0_hyd[('gas','z')])

        r_arr = [x_arr,y_arr,z_arr]

        out_dict['coord'] = r_arr

    if "rho" or "all" in fields:
        rho_arr  = np.array(all_data_level_0_hyd["density"])
        out_dict['rho'] = rho_arr

    if "prs" or "all" in fields:
        P_arr    = np.array(all_data_level_0_hyd["press"])
        out_dict['prs']   = P_arr

    if "T" or "logT" or "all" in fields:
        rho_arr  = np.array(all_data_level_0_hyd["density"])
        P_arr    = np.array(all_data_level_0_hyd["press"])
        T_arr    = (P_arr/rho_arr) * un.KELVIN * un.mu

        if "T" or "all" in fields:
            out_dict['T'] = T_arr
        if "logT" or "all" in fields:
            out_dict['logT'] = np.log10(T_arr)

    if "vel" or "all" in fields:
        vel1_arr = np.array(all_data_level_0_hyd["vel1"])
        vel2_arr = np.array(all_data_level_0_hyd["vel2"])
        vel3_arr = np.array(all_data_level_0_hyd["vel3"])

        vel = [vel1_arr, vel2_arr, vel3_arr]

        out_dict['vel'] = vel

    if MHD_flag and ("B" or "all" in fields):
        Bcc1 = np.array(all_data_level_0_hyd["Bcc1"])
        Bcc2 = np.array(all_data_level_0_hyd["Bcc2"])
        Bcc3 = np.array(all_data_level_0_hyd["Bcc3"])

        Bcc = [Bcc1,Bcc2,Bcc3]

        out_dict['B'] = Bcc

    return out_dict

def get_array_uservar_yt(fn, MHD_flag = False):

    ds = yt.load(fn)

    all_data_level_0_hyd = ds.covering_grid(
        level=0, left_edge=[0, 0.0, 0.0], dims=ds.domain_dimensions
    )

    out_dict = {}

    out_dict['user_out_var'] = np.array(all_data_level_0_hyd["user_out_var"])

    return out_dict


def get_array_athena(fn, fields, MHD_flag = False):

    ds = ar.athdf(fn)
    out_dict = {}

    out_dict['time'] = ds['Time']

    if "coord" or "all" in fields:
        x_arr = ds['x1v']
        y_arr = ds['x2v']
        z_arr = ds['x3v']

        r_arr = [x_arr,y_arr,z_arr]

        out_dict['coord'] = r_arr

    if "rho" or "all" in fields:
        rho_arr  = ds['rho']
        out_dict['rho'] = rho_arr

    if "prs" or "all" in fields:
        P_arr    = ds['press']
        out_dict['prs']   = P_arr
    
    # T_arr    = np.array(all_data_level_0_hyd["temp"])
    # out_dict['T']   = T_arr

    if "vel" or "all" in fields:
        vel1_arr = ds["vel1"]
        vel2_arr = ds["vel2"]
        vel3_arr = ds["vel3"]

        vel = [vel1_arr, vel2_arr, vel3_arr]

        out_dict['vel'] = vel

    if MHD_flag and ("B" or "all" in fields):
        Bcc1 = ds["Bcc1"]
        Bcc2 = ds["Bcc2"]
        Bcc3 = ds["Bcc3"]

        Bcc = [Bcc1,Bcc2,Bcc3]

        out_dict['B'] = Bcc

    return out_dict

def get_array_uservar_athena(fn, MHD_flag = False):

    ds = ar.athdf(fn)

    out_dict = {}

    out_dict['user_out_var'] = ds["user_out_var0"]

    return out_dict