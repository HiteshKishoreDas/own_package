'''
/*
 * @Author: Hitesh Kishore Das 
 * @Date: 2022-08-20 11:38:49 
 */
'''


#*_________________________________________________

# TODO: Add own clump finding script here!!

#*_________________________________________________

import matplotlib
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage.measurements as sm

import cmasher as cr 
import sys
import os

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt

#*_________________________________________________




#* Returns number of clumps and label array for any given array

def clump_finder_scipy(arr,arr_cut,above_cut=False):
    # arr      : Input array
    # arr_cut  : Cutoff for defining clumps
    # above_cut: True if values above arr_cut are clumps, False otherwise

    if above_cut:
        inp_arr = np.array(np.copy((arr>arr_cut)*arr)).astype(bool)
    else:
        inp_arr = np.array(np.copy((arr<arr_cut)*arr)).astype(bool)

    label_arr, n_blob = sm.label(inp_arr)

    return n_blob,label_arr




#* Plots the label arr of clumps for any given array

def clump_find_plot(arr, arr_cut, above_cut, interactive=False):
    # arr      : Input array
    # arr_cut  : Cutoff for defining clumps
    # above_cut: True if values above arr_cut are clumps, False otherwise

    # if interactive:
        # %matplotlib qt 

    # matplotlib.interactive('True')

    n_blob_sp, label_arr_sp = clump_finder_scipy(arr, arr_cut, above_cut)
    print(f'No. of clumps: {n_blob_sp}')

    fig, ax  = pt.scatter_3d(arr, arr_cut, arr, cmap=cr.neon, above_cut=above_cut)#, interactive=interactive)
    plt.show()

    fig, ax  = pt.scatter_3d(label_arr_sp, 0, label_arr_sp, cmap=cr.neon, above_cut=True)#, interactive=interactive)
    # above_cut in this line will always be True
    plt.show()


# TODO: Function to calculate shear

#* Labels the boundaries around the clumps
def boundary_detect (label_arr):

    # To mask out the clouds
    mask_arr = np.copy(label_arr).astype(bool)
    mask_arr = np.logical_not(mask_arr)

    temp_arr = np.zeros_like(label_arr)

    temp_arr += np.roll(label_arr,-1,axis=0) * mask_arr
    temp_arr += np.roll(label_arr, 1,axis=0) * mask_arr

    # To mask out the previously labeled cells
    temp_mask = np.copy(temp_arr).astype(bool)
    temp_mask = np.logical_not(temp_mask)

    temp_arr += np.roll(label_arr,-1,axis=1) * mask_arr * temp_mask
    temp_arr += np.roll(label_arr, 1,axis=1) * mask_arr * temp_mask

    temp_mask = np.copy(temp_arr).astype(bool)
    temp_mask = np.logical_not(temp_mask)

    temp_arr += np.roll(label_arr,-1,axis=2) * mask_arr * temp_mask
    temp_arr += np.roll(label_arr, 1,axis=2) * mask_arr * temp_mask

    return temp_arr


#* Calculates shear on the clumps

def shear_calc (label_arr, v_arr):

    nbr_arr = boundary_detect(label_arr)

    L = np.shape(label_arr)
    n_blob = np.max(label_arr)

    v1 = v_arr[0]
    v2 = v_arr[1]
    v3 = v_arr[2]

    shear_map = np.copy(label_arr).astype(float)

    shear_dict= {}
    shear_dict['clump_vel']  = []
    shear_dict['nbr_vel']    = []
    shear_dict['shear_vel']  = []
    shear_dict['shear_vmag'] = []
    shear_dict['clump_vol']  = []

    for i in range(1,n_blob+1):

        clump_vol = np.sum(label_arr[label_arr==i])/float(i)

        v1_clump = np.average(v1[label_arr==i])
        v2_clump = np.average(v2[label_arr==i])
        v3_clump = np.average(v3[label_arr==i])

        clump_vel  = np.array([v1_clump, v2_clump, v3_clump])

        v1_nbr   = np.average(v1[nbr_arr==i])
        v2_nbr   = np.average(v2[nbr_arr==i])
        v3_nbr   = np.average(v3[nbr_arr==i])

        nbr_vel  = np.array([v1_nbr, v2_nbr, v3_nbr])

        shear_v   = nbr_vel - clump_vel 
        shear_mag = np.linalg.norm(shear_v)


        if np.isnan(shear_mag):
            print(f"!! NaN encountered for clump number {i} ...")
            print(f"!! Surrounding velocity: {nbr_vel}")
            print(f"!! Clump       velocity: {clump_vel}")
        else:
            shear_map[shear_map==i] = shear_mag

            shear_dict['clump_vel'] .append(clump_vel)
            shear_dict['nbr_vel']   .append(nbr_vel)
            shear_dict['shear_vel'] .append(shear_v)
            shear_dict['shear_vmag'].append(shear_mag)
            shear_dict['clump_vol'] .append(clump_vol)

    # List of shear around each clump 
    return shear_dict, shear_map


#* Calculates surface area of the clumps

def surface_area (label_arr):

    nbr_arr = boundary_detect(label_arr)

    L = np.shape(label_arr)
    n_blob = np.max(label_arr)

    surface_dict= {}
    surface_dict['clump_vol']           = []
    surface_dict['clump_surface_area']  = []

    for i in range(1,n_blob+1):
        
        clump_vol = np.sum(label_arr[label_arr==i])/float(i)
        clump_sa  = np.sum(nbr_arr[nbr_arr==i])/float(i)

        surface_dict['clump_vol'] .append(clump_vol)
        surface_dict['clump_surface_area'] .append(clump_sa)

    # List of shear around each clump 
    return surface_dict



#* Returns the size and mass histogram for a given label array
#* and property arrays

def clump_hist (label_arr, dx, rho, T, n_bins, dim=3):
    # label_arr : Label array
    # dx        : Cell size
    # rho       : Density array for mass calculation
    # T         : Temperature array for clump definition
    # nbins     : Number o f bins for the histograms
    # dim       : # of dimension for the box (Default: 3)
    
    n_blob = np.max(label_arr)+1
    N,M = np.shape(label_arr)

    cloud_size = np.zeros(n_blob,dtype=float)
    cloud_mass = np.zeros(n_blob,dtype=float)

    for i in range(N):
        for j in range(M):

            cloud_size[label_arr[i,j]] += 1
            cloud_mass[label_arr[i,j]] += rho[i,j]*(dx**3)

    cloud_size = (cloud_size**(1/dim))*dx

    size_bin = np.logspace(np.log10(np.min(cloud_size)/2),np.log10(np.max(cloud_size)*2),num=n_bins)
    mass_bin = np.logspace(np.log10(np.min(cloud_mass)/2),np.log10(np.max(cloud_mass)*2),num=n_bins)

    size_hist = np.histogram(cloud_size,bins=size_bin)
    mass_hist = np.histogram(cloud_mass,bins=mass_bin)

    size_list = []
    size_list.append(list(size_hist[0].astype(float)))
    size_list.append(list(size_hist[1].astype(float)))

    mass_list = []
    mass_list.append(list(mass_hist[0].astype(float)))
    mass_list.append(list(mass_hist[1].astype(float)))

    return size_list, mass_list



#*_________________________________________________

if __name__ == "__main__":

    CONST_pc  = 3.086e18
    CONST_yr  = 3.154e7
    CONST_amu = 1.66053886e-24
    CONST_kB  = 1.3806505e-16

    unit_length = CONST_pc*1e3  # 1 kpc
    unit_time   = CONST_yr*1e6  # 1 Myr
    unit_density = CONST_amu    # 1 mp/cm-3
    unit_velocity = unit_length/unit_time

    KELVIN = unit_velocity*unit_velocity*CONST_amu/CONST_kB

    Xsol = 1.0
    Zsol = 1.0

    X = Xsol * 0.7381
    Z = Zsol * 0.0134
    Y = 1 - X - Z

    mu  = 1.0/(2.*X+ 3.*(1.-X-Z)/4.+ Z/2.);
    mue = 2.0/(1.0+X);
    muH = 1.0/X;

    mH = 1.0

    # test_arr = np.load('data/rho.npy')
    rho = np.load('data/rho.npy')
    prs = np.load('data/prs.npy')
    T = (prs/rho) * KELVIN * mu

    cut = 5e4
    # clump_find_plot(test_arr, cut, above_cut=True)

    n_blob_sp, label_arr_sp = clump_finder_scipy(T, cut, above_cut=False)

    # clump_find_plot(T, cut, above_cut=False)#, interactive=True)
    plt.style.use('dark_background') 

    v1 = np.load('data/v1.npy')
    v2 = np.load('data/v2.npy')
    v3 = np.load('data/v3.npy')

    v_arr = [v1,v2,v3]

    nbr_arr = boundary_detect(label_arr_sp)

    shear_dict, shear_map = shear_calc(label_arr_sp, v_arr)

    def grad_alpha(c_arr):

        alpha0 = 1.0
        alp = alpha0 * (c_arr-c_arr.min())/(c_arr.max()-c_arr.min())
        alp[c_arr==0] = 0.0
        return alp

    plt.hist(np.array(shear_dict['shear_vmag']))
    plt.show()

    # %matplotlib qt 

    fig, ax, sc  = pt.render_scatter_3d(inp_arr = shear_map, \
                             alpha_fn = grad_alpha,\
                             cmap=cr.neon)
    norm = mt.colors.Normalize(vmin=shear_map.min(), vmax=shear_map.max())
    fig.colorbar(mt.cm.ScalarMappable(norm=norm, cmap=cr.neon), ax=ax)
    plt.show()