'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-20 15:58:36 
'''


import numpy as np
import sys
import os

cwd = os.path.dirname(__file__)
tail_cut = len(cwd.split('/')[-1])+len(cwd.split('/')[-2])+1
package_abs_path = cwd[:-tail_cut]

sys.path.insert(0, f'{package_abs_path}pluto/')
import data_read as dr
import lamfn as lf
import units as g 

#*_________________________________

wdir_dir  = "/afs/mpa/temp/hitesh/NAS"
wdir_dir2 = "/afs/mpa/home/hitesh/remote/freya/PLUTO/TI"

wdir_R1 = f"{wdir_dir}/2D_nl_parascan_MG21_R1/output/"
wdir_R2 = f"{wdir_dir}/2D_nl_parascan_MG21_R2/output/"
wdir_R3 = f"{wdir_dir}/2D_nl_parascan_MG21_R3/output/"
wdir_R4 = f"{wdir_dir}/2D_nl_parascan_MG21_R4/output/"

wdir_R2_lowChif = f"{wdir_dir2}/2D_nl_parascan_MG21_R2_Chif_96/output/"

#*_________________________________

# wdir_list =          [wdir_R1  , wdir_R2  , wdir_R3  , wdir_R4 , wdir_R2_lowChif  ]
# dt_list   = np.array([5.0*1e-4 , 1.0*1e-3 , 5.0*1e-2 , 5.0     , 1.0*1e-3         ])
# file_list =          ['R1'     , 'R2'     , 'R3'     , 'R4'    , 'R2_low_Chi'     ]
# box_list  = np.array([0.0004   , 0.004    , 0.04     , 4.0     , 0.004            ])
# R_list    = np.array([0.00005  , 0.0005   , 0.005    , 0.5     , 0.0005           ])
# res_list  =          [2048     , 2048     , 2048     , 2048    , 2048             ]
# N_list    =          [1        , 2        , 3        , 4       , 5                ]
# Chi_list  = np.array([100      , 100      , 100      , 100     , 16               ])
# label_list =          ['R1'     , 'R2'     , 'R3'     , 'R4'    , 'R2_low_Chi'     ]

# wdir_list =          [wdir_R1  , wdir_R2  , wdir_R3  , wdir_R4 ]  #, wdir_R2_lowChif  ] 
# dt_list   = np.array([5.0*1e-4 , 1.0*1e-3 , 5.0*1e-2 , 5.0     ]) #, 1.0*1e-3         ])
# file_list =          ['R1'     , 'R2'     , 'R3'     , 'R4'    ]  #, 'R2_low_Chi'     ] 
# box_list  = np.array([0.0004   , 0.004    , 0.04     , 4.0     ]) #, 0.004            ])
# R_list    = np.array([0.00005  , 0.0005   , 0.005    , 0.5     ]) #, 0.0005           ])
# res_list  =          [2048     , 2048     , 2048     , 2048    ]  #, 2048             ] 
# N_list    =          [1        , 2        , 3        , 4       ]  #, 5                ] 
# Chi_list  = np.array([100      , 100      , 100      , 100     ]) #, 16               ])
# label_list =          ['R1'     , 'R2'     , 'R3'     , 'R4'    ]  #, 'R2_low_Chi'     ] 

wdir_list =          [wdir_R2  , wdir_R2_lowChif  , wdir_R4 ] 
dt_list   = np.array([1.0*1e-3 , 1.0*1e-3         , 5.0     ])
file_list =          ['R2'     , 'R2_low_Chi'     , 'R4'    ] 
box_list  = np.array([0.004    , 0.004            , 4.0     ])
R_list    = np.array([0.0005   , 0.0005           , 0.5     ])
res_list  =          [2048     , 2048             , 2048    ] 
N_list    =          [2        , 3                , 4       ] 
Chi_list  = np.array([100      , 16               , 100     ])
label_list =         [r'R2, $\chi_{\rm f} = 600$' \
                     ,r'R2, $\chi_{\rm f} = 96$'  \
                     ,r'R4, $\chi_{\rm f} = 600$' ] 

#*_________________________________

gamma = 5/3
Chi_i = Chi_list
rho_amb = 0.062
rho_cl = rho_amb * Chi_i
T_cl = 6e4
T_fl = 1e4

P = (T_cl*Chi_i*rho_amb)/(g.KELVIN*g.mu)

Chi_f = Chi_i*(T_cl/T_fl)
v0 = np.sqrt( (1-Chi_i/Chi_f) * P / rho_cl )

V   = np.pi*(R_list**2)
A   = 2*np.pi*R_list
M0  = rho_cl * V
KE0 = 0.5* M0 * (v0**2) 

TE0 = P*V/(gamma-1)

t0  = R_list/v0

cs_cold = lf.cs(rho_amb*Chi_f,T_fl,1.01,0.6)
cs_hot  = lf.cs(rho_amb,T_fl*Chi_f,1.01,0.6)

mdot = [0.015 , 0.035, 0.055, 0.07 ]
mb   = [0.002, 0.007, 0.0145, 0.018]

t_collapse = 1.25