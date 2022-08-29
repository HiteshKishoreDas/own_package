'''
Created Date: Thursday, August 25th 2022, 4:52:37 pm
Author: Hitesh
'''

#*_________________________________________________

# TODO: Add own clump finding script here!!

#*_________________________________________________

import matplotlib
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

def clump_finder_scipy(arr,arr_cut,above_cut):
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

    if interactive:
        %matplotlib qt 

    # matplotlib.interactive('True')

    n_blob_sp, label_arr_sp = clump_finder_scipy(arr, arr_cut, above_cut)
    print(f'No. of clumps: {n_blob_sp}')

    fig, ax  = pt.scatter_3d(arr, arr_cut, arr, cmap=cr.neon, above_cut=above_cut)#, interactive=interactive)
    plt.show()

    fig, ax  = pt.scatter_3d(label_arr_sp, 0, label_arr_sp, cmap=cr.neon, above_cut=True)#, interactive=interactive)
    # above_cut in this line will always be True
    plt.show()


# TODO: Function to calculate shear

#* Calculates shear on the clumps

def shear_calc (label_arr, v_arr):


    mask_arr = np.copy(label_arr).astype(bool)
    mask_arr = np.logical_not(mask_arr)

    temp_arr = np.zeros_like(label_arr)

    temp_arr += np.roll(label_arr,-1,axis=0)*mask_arr
    temp_arr += np.roll(label_arr, 1,axis=0)*mask_arr

    temp_arr += np.roll(label_arr,-1,axis=1)*mask_arr
    temp_arr += np.roll(label_arr, 1,axis=1)*mask_arr

    temp_arr += np.roll(label_arr,-1,axis=2)*mask_arr
    temp_arr += np.roll(label_arr, 1,axis=2)*mask_arr



    return temp_arr


    # shear_list = []


    # List of shear around each clump 
    # return shear_list





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

    cut = 8e4
    # clump_find_plot(test_arr, cut, above_cut=True)

    n_blob_sp, label_arr_sp = clump_finder_scipy(T, cut, above_cut=False)

    # clump_find_plot(T, cut, above_cut=False, interactive=True)

    v1 = np.load('data/v1.npy')
    v2 = np.load('data/v2.npy')
    v3 = np.load('data/v3.npy')

    v_arr = [v1,v2,v3]

    nbr_arr = shear_calc(label_arr_sp, v_arr)

    plt.imshow(nbr_arr[:,:,10])
    plt.show()


    # if True:
    #     %matplotlib qt

    plt.style.use('dark_background') 

    fig, ax  = pt.scatter_3d(nbr_arr, 0, nbr_arr, cmap=cr.neon, above_cut=True)