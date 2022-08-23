import numpy as np
import yt

def get_array(fn, MHD_flag = False):

    ds = yt.load(fn)

    all_data_level_0_hyd = ds.covering_grid(
        level=0, left_edge=[0, 0.0, 0.0], dims=ds.domain_dimensions
    )

    out_dict = {}

    x_arr = np.array(all_data_level_0_hyd[('gas','x')])
    y_arr = np.array(all_data_level_0_hyd[('gas','y')])
    z_arr = np.array(all_data_level_0_hyd[('gas','z')])

    r_arr = [x_arr,y_arr,z_arr]

    out_dict['coord'] = r_arr

    rho_arr  = np.array(all_data_level_0_hyd["density"])
    P_arr    = np.array(all_data_level_0_hyd["press"])
    T_arr    = np.array(all_data_level_0_hyd["temp"])
    
    out_dict['rho'] = rho_arr
    out_dict['T']   = T_arr
    out_dict['P']   = P_arr

    vel1_arr = np.array(all_data_level_0_hyd["vel1"])
    vel2_arr = np.array(all_data_level_0_hyd["vel2"])
    vel3_arr = np.array(all_data_level_0_hyd["vel3"])

    vel = [vel1_arr, vel2_arr, vel3_arr]

    out_dict['vel'] = vel

    if MHD_flag:
        Bcc1 = np.array(all_data_level_0_hyd["Bcc1"])
        Bcc2 = np.array(all_data_level_0_hyd["Bcc2"])
        Bcc3 = np.array(all_data_level_0_hyd["Bcc3"])

        Bcc = [Bcc1,Bcc2,Bcc3]

        out_dict['B'] = Bcc

    return out_dict

def get_array_user_var(fn, MHD_flag = False):

    ds = yt.load(fn)

    all_data_level_0_hyd = ds.covering_grid(
        level=0, left_edge=[0, 0.0, 0.0], dims=ds.domain_dimensions
    )

    out_dict = {}

    out_dict['user_out_var'] = np.array(all_data_level_0_hyd["user_out_var"])

    return 