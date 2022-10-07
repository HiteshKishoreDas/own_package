import numpy as np

# import sys
import os

import sys

cwd = os.path.dirname(__file__)
tail_cut = len(cwd.split('/')[-1])+len(cwd.split('/')[-2])+1
package_abs_path = cwd[:-tail_cut]

sys.path.insert(0, f'{package_abs_path}cooling/')
import cooling_fn as cf

sys.path.insert(0, f'{package_abs_path}utils/')
import v_turb as vt
import units as g


chi_cold = 100

# Relevant temperature
T_floor   = 40000                       # No cooling below T_floor
T_ceil    = 100000000                   # No gas above T_ceil
T_hot     = T_floor*chi_cold            # Required T_hot
T_cold    = 2*T_floor                   # For cold gas mass calculation
T_cut_mul = 0.5                         # For cooling cutoff
T_cut     = T_cut_mul*T_hot             # For cooling cutoff

amb_rho   = np.array([1.6e-4])
# Lambda_fac = np.array([1e4,5000,1000.0,500.0,100.0, 50.0, 10.0, 5.0, 1.0, 0.5, 0.1]) 
Lambda_fac = np.array([1.0])

# Density of the ambient medium

# Pressure floor
P_floor = 1e-15*np.ones_like(amb_rho)  #5*1e-4*np.array(amb_rho/1.0)

# Chemical composition
Xsol = 1.0;
Zsol = 1.0;

X = Xsol * 0.7381;
Z = Zsol * 0.0134;
Y = 1 - X - Z;

mu  = 1.0/(2.*X+ 3.*(1.-X-Z)/4.+ Z/2.)
mue = 2.0/(1.0+X)
muH = 1.0/X
mH  = 1.0


# R_lsh = np.array([100,250,500,1000,2500])
R_lsh = np.array([2500])

t_cool_cloud = cf.tcool_calc(amb_rho*chi_cold,T_floor,Z, Lambda_fac=Lambda_fac)
t_cool_floor = cf.tcool_calc(amb_rho,T_floor,Z, Lambda_fac=Lambda_fac)
t_cool_mix   = cf.tcool_calc(amb_rho*np.sqrt(chi_cold),np.sqrt(T_floor*T_hot),Z, Lambda_fac=Lambda_fac)
t_cool_amb   = cf.tcool_calc(amb_rho,T_hot,Z, Lambda_fac=Lambda_fac)
t_cool_cut   = cf.tcool_calc(amb_rho/T_cut_mul,T_cut_mul*T_hot,Z, Lambda_fac=Lambda_fac)

t_cool_Da   = cf.tcool_calc(amb_rho*np.sqrt(chi_cold), 2e5 ,Z, Lambda_fac=Lambda_fac)

amb_rho_fix = 1.0
t_cool_cloud_fix = cf.tcool_calc(amb_rho_fix*chi_cold,T_floor,Z, Lambda_fac=Lambda_fac)
l_sh = vt.cs_calc(T_floor,mu)*t_cool_cloud_fix


cs_hot  = vt.cs_calc(T_floor, mu)
cs_cold = vt.cs_calc(T_hot, mu)

cloud_radius = R_lsh*l_sh

# box_width  = np.array([0.1])  # 0.1 kpc = 100 pc # cloud_radius*2
# box_length = np.array([1.0])  # 0.3 kpc = 300 pc # box_width*10

# box_width  = 0.1 * np.array([100000.0, 50000.0, 10000.0, 5000.0, 1000.0, 500.0, 100.0, 50.0, 10.0, 5.0, 1.0, 0.5, 0.1])
# box_width  = 0.1 * np.array([10000.0, 1000.0, 100.0, 10.0, 1.0, 0.1, 0.01, 0.001, 0.0001])

box_width  = 0.1 * np.array([10000.0, 10000.0, \
                             100.0  , 100.0  , \
                             1.0    , 1.0    , \
                             0.001  , 0.001  , \
                             0.0001 , 0.0001   ])

shift_flag = np.array([1, 0, \
                       1, 0, \
                       1, 0, \
                       1, 0, \
                       1, 0  ])

box_length = 10*box_width

# Cooling flag
cooling_flag = 1  # 1 for cooling and 0 for no cooling
                  # Cooling() is added(not added) to Source() depending on the flag 

# Cloud flag
cloud_flag   = 0  # 1 for a cloud and 0 for no cloud
                  # Cloud_init() is added(not added) to Source() depending on the flag 

# Magnetic field flag
B_flag       = 0  # 1 for adding magnetic fields

# Ma = np.array([0.1, 10])
Ma = np.array([10])

# Box sizes
x1max = box_width
x1min = np.zeros_like(box_width)

x2max = box_width
x2min = np.zeros_like(box_width)

x3max = box_length* 5/10  # 0.8
x3min = x3max - box_length

# Number of cells
nx1 = np.array([64 ])
nx2 = np.array([64 ])
nx3 = np.array([640])

# nx1 = np.array([128])
# nx2 = np.array([128])
# nx3 = np.array([1280])

nx1_mesh = np.array([32])
nx2_mesh = np.array([32])
nx3_mesh = np.array([32])

# Initial profile settings 

front_thickness = box_width/20
v_shear         = 0.1022   # M*vt.cs_calc(T_hot,mu)
# M  = 0.5     # Required Mach number
M = v_shear/vt.cs_calc(T_hot, g.mu)     # Required Mach number

v_m = 0.00238
v_b = 0.00390

# v_shift = -0.01 * (box_width/box_width[4])
# v_shift  = v_m*np.log10(box_width) + v_b
# v_shift *= -1.0
v_shift = 0.0

knx_KH = 1.0
kny_KH = 1.0
amp_KH = 0.01

t_KH = np.sqrt(chi_cold)*box_width/v_shear
tlim  =  20*t_KH  #np.max(np.array([5*t_eddy, 2*t_cool_amb]) )

# dt for history output from tlim
hst_dt_arr = tlim/2000

# dt for output files
out_dt_arr = tlim/200

# dt for restart files
rst_dt_arr = tlim/10

# rseed
rseed = 1


# Magnetic fields

beta_list = (2/g.g) * (Ma/M)**2

if B_flag:
    B_dir     = ['x','y','z']
else:
    B_dir     = ['h']

B_x = np.array([ [ [0.0] *len(B_dir) ] *len(Ma)] *len(box_width) )
B_y = np.array([ [ [0.0] *len(B_dir) ] *len(Ma)] *len(box_width) )
B_z = np.array([ [ [0.0] *len(B_dir) ] *len(Ma)] *len(box_width) )

if B_flag:

    for i_l, Lam_fac in enumerate(box_width):

        for i_b, beta in enumerate(beta_list):

            P_th  = (T_hot/(g.KELVIN*g.mu))*amb_rho[0]
            P_B = P_th/beta

            # Assuming that cgs relation between B_mag and P_B is used
            B_mag = np.sqrt(P_B * 2.0)

            for i_d, B_d in enumerate(B_dir):
               if B_d=='x':
                   B_x[i_l, i_b, i_d] = B_mag
               elif B_d=='y':
                   B_y[i_l, i_b, i_d] = B_mag
               elif B_d=='z':
                   B_z[i_l, i_b, i_d] = B_mag
               else:
                   print('! Invalid magnetic field direction (B_dir)! ... ')
                   exit


### FOR JOB SCRIPT

n_cores = (nx1*nx2*nx3)/(nx1_mesh*nx2_mesh*nx3_mesh)

queue = "p.24h"
ntasks_per_node = 40

nodes = (n_cores/ntasks_per_node).astype(int)

time_limit     = ["12:55:00"] #["03:00:00","12:00:00"]#,"23:49:00"]
time_limit_rst = ["12:52:00"] #["02:45:00","11:45:00"]#,"23:35:00"]



### FILE NAME

def filename_mix_add (i,j,k):

    if B_flag:
        return f'_L{i}_Ma{j}_B{k}_moving'
    else:
        return f'_L{i}_Ma{j}_Bnot_hydro_moving'
    # return f'_res_256_Rlsh_0'

#* For access to plotting scripts
def filename_mix_add_ext (i, j, k, MHD_flag):

    if MHD_flag:
        return f'_L{i}_Ma{j}_B{k}_moving'
    else:
        return f'_L{i}_Ma{j}_Bnot_hydro_moving'
