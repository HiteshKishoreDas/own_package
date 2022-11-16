
import numpy as np
import yt
import sys
import os
import gc

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}athena/athena_vis_code/')
import athena_read as ar

sys.path.insert(0, f'{package_abs_path}pluto/')
import pyPLUTO
import pyPLUTO.pload as pp

sys.path.insert(0, f'{package_abs_path}utils/')
import units as un


def get_array ( fn:str = None, N:int = None,  
                dir_name:str = None, 
                fields:list = ['all'],  
                dim:int = None, 
                method:str = 'athena', 
                MHD_flag:bool = False, 
                trc_flag:bool = False, 
                trc_N:int = 1,
                user_var_N:int = 1          ):
    """
    Function to read simulation data

    Args:
        fn (str, optional): Path to the file to read, used for method 'athena' and 'yt'. Defaults to None.
        N (int, optional): Number of the snapshot to read, used for method 'pluto'. Defaults to None.
        dir_name (str, optional): Path to the output directory with snapshots, used for method 'pluto'. Defaults to None.
        fields (list, optional): List of fields that need to be read. Defaults to ['all'].
        dim (int, optional): Dimensions of the output, used in method 'pluto'. Defaults to None.
        method (str, optional): Method of data reading. Available methods: 'athena', 'yt', 'pluto'. Defaults to 'athena'.
        MHD_flag (bool, optional): True for MHD simulation data. Defaults to False.
        trc_flag (bool, optional): True for presence of tracer quantity. Defaults to False.
        trc_N (int, optional): Number of tracers. Defaults to 1.
        user_var_N (int, optional): Number of user-defined variables. Defaults to 1.

    Returns:
        Dict: Dictionary with the required fields
    """

    out_dict = {}


    if method=='athena':
        if fn is None:
            print("get_array(): fn required for method 'athena' ... ")
            exit()

        ds = ar.athdf(fn)
        out_dict['time'] = ds['Time']

    if method=='yt':
        if fn is None:
            print("get_array(): fn required for method 'athena' ... ")
            exit()

        ds = yt.load(fn)
      
        all_data_level_0_hyd = ds.covering_grid(
            level=0, left_edge=[0, 0.0, 0.0], dims=ds.domain_dimensions

        )

        out_dict['time'] = ds.current_time

    elif method=='pluto':
        if (N is None):
            print("get_array(): N required for method 'pluto' ... ")
            exit()
        elif (dir_name is None):
            print("get_array(): dir_name required for method 'pluto' ... ")
            exit()
        elif (dim is None):
            print("get_array(): dim not provided for method 'pluto' ... ")
            print("get_array(): dim has defaulted to 3              ... ")

        nlinf = pyPLUTO.nlast_info(w_dir=dir_name)
        D = pp.pload(N, w_dir=dir_name)

        out_dict['time'] = D.SimTime
        out_dict['nlast'] = nlinf.get('nlast')

        # Define scope for eval(), uses global scope by default
        scope=locals()

        x_dim = {1 : ['x1'], 
                 2 : ['x1', 'x2'], 
                 3 : ['x1', 'x2', 'x3'] }

    else:
        print("get_array(): Invalid method, method has be one of 'athena', 'yt' or 'pluto' ... ")
        exit()


    if 'coord' or 'all' in fields:
        
        if method == 'athena':
            out_dict['coord'] = [ds['x1v'], ds['x2v'], ds['x3v']]

        elif method == 'yt':
            out_dict['coord'] = [ np.array(all_data_level_0_hyd[('gas','x')]) ,
                                  np.array(all_data_level_0_hyd[('gas','y')]) ,
                                  np.array(all_data_level_0_hyd[('gas','z')]) ] 

        elif method == 'pluto':
            coord_dim = ['D.' +xd for xd in x_dim[dim]]
            dx_dim    = ['D.d'+xd for xd in x_dim[dim]]

            out_dict['coord'] = [ eval(cd, scope) for cd in coord_dim]
            out_dict['dx']    = [ eval(dd, scope) for dd in dx_dim   ]

    if 'rho' or 'all' in fields:
        if method == 'athena':
            out_dict['rho'] = ds['rho']

        elif method == 'yt':
            out_dict['rho'] = np.array(all_data_level_0_hyd["density"])

        elif method == 'pluto':
            out_dict['rho'] = D.rho

    if 'prs' or 'all' in fields:
        if method == 'athena':
            out_dict['prs']   = ds['press']

        elif method == 'yt':
            out_dict['prs']   = np.array(all_data_level_0_hyd["press"])

        elif method == 'pluto':
            out_dict['prs']   = D.prs


    if 'T' or 'logT' or 'all' in fields:
        if method == 'athena':
            rho_arr  = ds['rho']
            P_arr    = ds['press']

        elif method == 'yt':
            rho_arr  = np.array(all_data_level_0_hyd["density"])
            P_arr    = np.array(all_data_level_0_hyd["press"])

        if method == 'pluto':
            P_arr    = D.prs
            rho_arr  = D.rho

        T_arr    = (P_arr/rho_arr) * un.KELVIN * un.mu

        if 'T' or 'all' in fields:
            out_dict['T'] = T_arr
        if 'logT' or 'all' in fields:
            out_dict['logT'] = np.log10(T_arr)

        del P_arr
        del rho_arr
        del T_arr
        gc.collect()


    if 'vel' or 'all' in fields:
        if method == 'athena':
            out_dict['vel'] = [ds["vel1"], ds["vel2"], ds["vel3"]]

        if method == 'yt':
            out_dict['vel'] = [ np.array(all_data_level_0_hyd["vel1"]),
                                np.array(all_data_level_0_hyd["vel2"]), 
                                np.array(all_data_level_0_hyd["vel3"])  ]

        elif method == 'pluto':
            v_dim = ['D.v'+xd for xd in x_dim[dim]]
            out_dict['vel'] = [eval(vd, scope) for vd in v_dim]


    if MHD_flag and ('B' or 'all' in fields):
        if method == 'athena':
            out_dict['B'] = [ds["Bcc1"], ds["Bcc2"], ds["Bcc3"]]

        elif method == 'yt':
            out_dict['B'] = [ np.array(all_data_level_0_hyd["Bcc1"]) , 
                              np.array(all_data_level_0_hyd["Bcc2"]) ,
                              np.array(all_data_level_0_hyd["Bcc3"]) ]

        elif method == 'pluto':
            B_dim = ['D.b'+xd for xd in x_dim[dim]]
            out_dict['B'] = [eval(bd, scope) for bd in B_dim]

    if 'user_var' in fields:
        if method == 'athena':
            out_dict['user_out_var'] = [ds[f"user_out_var{i}"] for i in range(user_var_N)]

    if trc_flag and ('trc' or 'all' in fields):
        if method == 'athena':
            out_dict['trc'] = [ds[f"r{i}"] for i in range(trc_N)]

        if method == 'pluto':
            trc_list = [f'D.trc{ti}' for ti in range(trc_N)]
            out_dict['trc'] = [eval(tl, scope) for tl in trc_list]

    return out_dict