'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-14 10:15:19 
'''

import numpy as np
import pickle as pk
import os
import sys
import gc

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import array_operations as ao

sys.path.insert(0, f'{package_abs_path}pluto/')
import data_read as dr
import lamfn as lf
import units as g 

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_2d_line as p2l

debug_flag = False
# debug_flag = True

#*_________________________________

# wdir_dir = "/afs/mpa/temp/hitesh/NAS"
wdir_dir = "/afs/mpa/home/hitesh/remote/freya/PLUTO/TI"

wdir_R1 = f"{wdir_dir}/2D_nl_parascan_MG21_R1/output/"
wdir_R2 = f"{wdir_dir}/2D_nl_parascan_MG21_R2/output/"
wdir_R3 = f"{wdir_dir}/2D_nl_parascan_MG21_R3/output/"
wdir_R4 = f"{wdir_dir}/2D_nl_parascan_MG21_R4/output/"

wdir_R2_lowChif = f"{wdir_dir}/2D_nl_parascan_MG21_R2_Chif_96/output/"

#*_________________________________

# wdir_list =          [wdir_R1  , wdir_R2  , wdir_R3  , wdir_R4 ]
# dt_list   = np.array([5.0*1e-4 , 1.0*1e-3 , 5.0*1e-2 , 5.0     ])
# file_list =          ['R1'     , 'R2'     , 'R3'     , 'R4'    ]
# box_list  = np.array([0.0004   , 0.004    , 0.04     , 4.0     ])
# R_list    = np.array([0.00005  , 0.0005   , 0.005    , 0.5     ])
# res_list  =          [2048     , 2048     , 2048     , 2048    ]
# N_list    =          [1        , 2        , 3        , 4       ]

wdir_list =          [wdir_R2_lowChif  ]
dt_list   = np.array([1.0*1e-3         ])
file_list =          ['R2_low_Chi'     ]
box_list  = np.array([0.004            ])
R_list    = np.array([0.0005           ])
res_list  =          [2048             ]
N_list    =          [5                ]
#*_________________________________


T_cut = 4e4
T_cloud = 6e4

for i_wd, wd in enumerate(wdir_list):

    print(file_list[i_wd])

    D0 = dr.get_array(0, wd, fields=['coord'])    

    dx = D0['dx'][0][0]
    dy = D0['dx'][1][0]

    sim_data         = {}
    sim_data['name'] = file_list[i_wd]
    sim_data['dV']   = dx*dy
    sim_data['cold_gas'] = []
    sim_data['v_rad']    = []
    sim_data['vol']      = []
    sim_data['KE_cold']  = []
    sim_data['KE_hot']   = []
    sim_data['time']     = []


    for n in range(D0['nlast']+1):
    # for n in range(1,2):

        print(n)

        D = dr.get_array(n, wd, fields=['rho','temp', 'vel']) 

        cold_gas = np.sum((D['rho'])[D['temp']<T_cut])*sim_data['dV']
        sim_data['cold_gas'].append(cold_gas)
        sim_data['time'].append(D['time'])

        v_rad = ao.radial_vector(D['vel'])   [ D['temp']>2*T_cloud ]
        v_rad = np.average(v_rad)
        sim_data['v_rad'].append(v_rad)

        volume = np.sum(D['temp']<T_cut)*sim_data['dV']
        sim_data['vol'].append(volume)

        KE = 0.5 * D['rho'] * ( ao.magnitude(D['vel'])**2 ) * sim_data['dV']

        sim_data['KE_cold'].append(  np.sum( KE[D['temp']<T_cut] )  )
        sim_data['KE_hot'] .append(  np.sum( KE[D['temp']>T_cut] )  )

        del(D)
        gc.collect()

    if not debug_flag:
        try:
            os.system(f"mkdir ./save_arr/{file_list[i_wd]}")
        except:
            print(f"pluto/snapshot_analysis.py: Error in creating directory {file_list[i_wd]}")

        with open(f'./save_arr/{file_list[i_wd]}/{file_list[i_wd]}_evolution.pkl', 'wb') as f:
            pk.dump(sim_data, f)

print("Done!")