'''
Created Date: 2022-11-08 14:17:07
Author: Hitesh Das
'''

def plot_dict_create(field_list, )

    if 'rho' or 'all' in field_list:
        quant_dict['rho'] = {}
        quant_dict['rho']['title'] = 'Log_10 Density'
        quant_dict['rho']['save_loc'] = f"{sim_loc}Plots/slices/rho/rho_{str(n_snap).zfill(5)}.png"

        quant_dict['rho']['arg_dict'] = {}
        quant_dict['rho']['arg_dict']['img_data'] = np.log10(out_dict['rho'])
        quant_dict['rho']['arg_dict']['color_range'] = [-5,-1]
        quant_dict['rho']['arg_dict']['cmap'] = cmap
        quant_dict['rho']['arg_dict']['view_dir'] = 1 

    if 'prs' or 'all' in field_list:
        quant_dict['prs'] = {}
        quant_dict['prs']['title'] = 'Pressure'
        quant_dict['prs']['save_loc'] = f"{sim_loc}Plots/slices/prs/prs_{str(n_snap).zfill(5)}.png"

        quant_dict['prs']['arg_dict'] = {}
        quant_dict['prs']['arg_dict']['img_data'] = np.log10(out_dict['rho'])
        quant_dict['prs']['arg_dict']['cmap'] = cmap
        quant_dict['prs']['arg_dict']['view_dir'] = 1 

    if 'logT' or 'all' in field_list:
        quant_dict['logT'] = {}
        quant_dict['logT']['title'] = 'log_10 T'
        quant_dict['logT']['save_loc'] = f"{sim_loc}Plots/slices/logT/logT_{str(n_snap).zfill(5)}.png"

        quant_dict['logT']['arg_dict'] = {}
        quant_dict['logT']['arg_dict']['img_data'] = out_dict['logT']
        quant_dict['logT']['arg_dict']['cmap'] = cmap
        quant_dict['logT']['arg_dict']['view_dir'] = 1 

    if 'vx' or 'all' in field_list:
        quant_dict['vx'] = {}
        quant_dict['vx']['title'] = 'v_x'
        quant_dict['vx']['save_loc'] = f"{sim_loc}Plots/slices/vx/vx_{str(n_snap).zfill(5)}.png"

        quant_dict['vx']['arg_dict'] = {}
        quant_dict['vx']['arg_dict']['img_data'] = out_dict['vel'][0]
        quant_dict['vx']['arg_dict']['cmap'] = cmap
        quant_dict['vx']['arg_dict']['view_dir'] = 1 

    if 'vy' or 'all' in field_list:
        quant_dict['vy'] = {}
        quant_dict['vy']['title'] = 'v_y'
        quant_dict['vy']['save_loc'] = f"{sim_loc}Plots/slices/vy/vy_{str(n_snap).zfill(5)}.png"

        quant_dict['vy']['arg_dict'] = {}
        quant_dict['vy']['arg_dict']['img_data'] = out_dict['vel'][1]
        quant_dict['vy']['arg_dict']['cmap'] = cmap
        quant_dict['vy']['arg_dict']['view_dir'] = 1 

    if 'vz' or 'all' in field_list:
        quant_dict['vz'] = {}
        quant_dict['vz']['title'] = 'v_z'
        quant_dict['vz']['save_loc'] = f"{sim_loc}Plots/slices/vz/vz_{str(n_snap).zfill(5)}.png"

        quant_dict['vz']['arg_dict'] = {}
        quant_dict['vz']['arg_dict']['img_data'] = out_dict['vel'][2]
        quant_dict['vz']['arg_dict']['cmap'] = cmap
        quant_dict['vz']['arg_dict']['view_dir'] = 1 

    if MHD_flag and ('Bx' or 'all' in field_list):
        quant_dict['Bx'] = {}
        quant_dict['Bx']['title'] = 'B_x'
        quant_dict['Bx']['save_loc'] = f"{sim_loc}Plots/slices/Bx/Bx_{str(n_snap).zfill(5)}.png"

        quant_dict['Bx']['arg_dict'] = {}
        quant_dict['Bx']['arg_dict']['img_data'] = out_dict['B'][0]
        quant_dict['Bx']['arg_dict']['cmap'] = cmap
        quant_dict['Bx']['arg_dict']['view_dir'] = 1 

    if MHD_flag and ('By' or 'all' in field_list):
        quant_dict['By'] = {}
        quant_dict['By']['title'] = 'B_y'
        quant_dict['By']['save_loc'] = f"{sim_loc}Plots/slices/By/By_{str(n_snap).zfill(5)}.png"

        quant_dict['By']['arg_dict'] = {}
        quant_dict['By']['arg_dict']['img_data'] = out_dict['B'][1]
        quant_dict['By']['arg_dict']['cmap'] = cmap
        quant_dict['By']['arg_dict']['view_dir'] = 1 

    if MHD_flag and ('Bz' or 'all' in field_list):
        quant_dict['Bz'] = {}
        quant_dict['Bz']['title'] = 'B_z'
        quant_dict['Bz']['save_loc'] = f"{sim_loc}Plots/slices/Bz/Bz_{str(n_snap).zfill(5)}.png"

        quant_dict['Bz']['arg_dict'] = {}
        quant_dict['Bz']['arg_dict']['img_data'] = out_dict['B'][2]
        quant_dict['Bz']['arg_dict']['cmap'] = cmap
        quant_dict['Bz']['arg_dict']['view_dir'] = 1 


