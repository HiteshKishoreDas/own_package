'''
/*
 * @Author: Hitesh Kishore Das 
 * @Date: 2022-08-20 11:38:49 
 */
'''


#*_________________________________________________

# TODO: Add own clump finding script here!!

#*_________________________________________________

from importlib.resources import path
from re import I
from unittest import skip
import matplotlib
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
# import scipy.ndimage.measurements as sm
import scipy.ndimage as sm
import networkx as nx
import sklearn.metrics as skm
import time
import gc


import cmasher as cr 
import sys
import os
from own_package.plot.plot_3d import new_plot

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt

#*_________________________________________________

if __debug__:
    print("clump_analysis.py::Debug ON")
else:
    print("clump_analysis.py::Debug OFF")


#* Clump finder from scipy 
def clump_finder_scipy(arr,arr_cut, above_cut=False):
    # arr      : Input array
    # arr_cut  : Cutoff for defining clumps
    # above_cut: True if values above arr_cut are clumps, False otherwise

    if above_cut:
        inp_arr = np.array(np.copy((arr>arr_cut)*arr)).astype(bool)
    else:
        inp_arr = np.array(np.copy((arr<arr_cut)*arr)).astype(bool)

    label_arr, n_blob = sm.label(inp_arr)

    return n_blob,label_arr

#* Parent function for all clump finder functions
#* Returns number of clumps and label array for any given array
def clump_finder(arr,arr_cut, method='scipy', above_cut=False):
    if __debug__:
        print("clump_analysis.py::clump_finder(): clump finder called ...")

    if method=='scipy':
        return clump_finder_scipy(arr,arr_cut, above_cut=False)
    else:
        print('clump_analysis.py::clump_finder(): Invalid "method", using default("scipy")... ')
        return clump_finder_scipy(arr,arr_cut, above_cut=False)

#* Returns label array after selecting the specific clump
def clump_select(clump_num, label_arr):

    label_arr_cp = np.copy(label_arr)
    label_arr_cp[label_arr_cp!=clump_num] = 0
    label_arr_cp[label_arr_cp==clump_num] = 1

    return label_arr_cp

def clump_center(label_arr):

    label_arr_cp = np.copy(label_arr)
    label_arr_cp[label_arr>0] = 1
    L = np.shape(label_arr)
    if __debug__:
        print("clump_analysis.py::clump_center(): label_arr copy capped at 1 ...")

    grid_arr = np.indices(np.shape(label_arr))

    com = [0,0,0]
    com[0] = int(L[0]/2) - int(np.average(grid_arr[0][label_arr_cp==1]))
    com[1] = int(L[1]/2) - int(np.average(grid_arr[1][label_arr_cp==1]))
    com[2] = int(L[2]/2) - int(np.average(grid_arr[2][label_arr_cp==1]))
    # com[0] = int(np.average(grid_arr[0][label_arr_cp==1]))
    # com[1] = int(np.average(grid_arr[1][label_arr_cp==1]))
    # com[2] = int(np.average(grid_arr[2][label_arr_cp==1]))

    label_arr_cp = np.roll(label_arr_cp, shift=tuple(com), axis=(0,1,2))

    com = [0,0,0]
    com[0] = int(np.average(grid_arr[0][label_arr_cp==1]))
    com[1] = int(np.average(grid_arr[1][label_arr_cp==1]))
    com[2] = int(np.average(grid_arr[2][label_arr_cp==1]))

    return label_arr_cp

def clump_flatten (label_arr):

    label_arr_cp = np.copy(label_arr)
    label_arr_cp[label_arr>0] = 1
    L = np.shape(label_arr)
    if __debug__:
        print("clump_analysis.py::clump_flatten(): label_arr copy capped at 1 ...")

    grid_arr = np.indices(L)

    label_arr_cp = np.ravel(label_arr_cp) 

    i_arr = (np.ravel(grid_arr[0]))[label_arr_cp==1]
    j_arr = (np.ravel(grid_arr[1]))[label_arr_cp==1]
    k_arr = (np.ravel(grid_arr[2]))[label_arr_cp==1]

    return np.stack((i_arr,j_arr,k_arr))

def clump_covariance (label_arr, only_cov=False):
    if __debug__:
        print(f"clump_analysis.py::clump_covariance(): clump_covariance called with {only_cov = }...")

    label_arr_cp = np.copy(label_arr)
    L = np.shape(label_arr)

    grid_arr = np.indices(L)

    label_arr_cp = np.ravel(label_arr_cp) 

    r_list  = np.stack( 
                        ( 
                            (np.ravel(grid_arr[0]))[label_arr_cp>0],
                            (np.ravel(grid_arr[1]))[label_arr_cp>0],
                            (np.ravel(grid_arr[2]))[label_arr_cp>0]
                        )
                      )

    return_dict = {}

    if only_cov:
        return_dict['cov'] = np.cov(r_list)
    else:
        return_dict['cov'] = np.cov(r_list)
        return_dict['r_list'] = r_list

    return return_dict

# ! DOES NOT WORK PROPERLY! DO NOT USE THIS METHOD!
def clump_size (clump_num, label_arr, clump_centering=False):

    label_arr_shifted = clump_select(clump_num, label_arr)

    clump_vol = np.sum(label_arr_shifted)

    #* Calculate covariance matrix for the isolated clump
    cov_dict = clump_covariance(label_arr_shifted)

    #* Check if NaN in covariance matrix
    #* Happens if the clump has only one cell
    if np.isnan(np.sum(cov_dict['cov'])):
        print("clump_analysis.py::clump_size(): Insufficient number of cells (need >1) in the clump for covariance calculation...")
        print(" Skipping covariance matrix calculation and diagonalisation ...")
        return {'clump_size':[1.0,1.0,1.0], 'clump_volume': 1.0}

    #* Calculate the principal axes, i.e. eigevectors of covariance matrix
    eval, evec = np.linalg.eig(cov_dict['cov'])

    #* Calculate size of clump
    #* Using the extent of the projection of points on the principal axes
    clump_size = [0]*3
    for i in range(3):

        norm_ev = np.sqrt(np.sum(evec[i]**2))
        proj_arr = np.dot(cov_dict['r_list'].T, evec[i])
        print(f"{np.shape(proj_arr)=}")
        print(f"{np.shape(cov_dict['r_list'])=}")

        dproj = np.abs(proj_arr.max()-proj_arr.min())/norm_ev

        clump_size[i] = dproj + 1
        
    #* Return a dictionary with different values
    return_dict = {}
    return_dict['clump_size']   = clump_size        # List with clump sizes
    return_dict['clump_volume'] = clump_vol         # List with clump sizes
    return_dict['evec'] =  evec                     # Eigenvectors (Principal axes)
    return_dict['eval'] =  eval                     # Eigenvalues

    return return_dict


#* Find clump length using neighbourhood graph
#* While high skip_data, the filament length might jump small gaps.

# TODO: Add a weight to the graph edges, with weight being the difference in
# TODO: the density between the points. Maybe the difference is higher across the gap

# TODO: Come up with a smarter way of decreasing the points
def clump_length(clump_num, label_arr, k_n=1, n_jobs=1, skip_data=1):
    """
    Find clump length using neighbourhood graph
    While high skip_data, the filament length might jump small gaps.

    Args:
        clump_num (int): Index number of the clump
        label_arr (numpy array): label array, output from clump_finder() 
        k_n (int, optional): kth neighbour to be considered for an edge. Defaults to 1.
        n_jobs (int, optional): number of threads to use for adjacency calculation. Defaults to 1.
        skip_data (int, optional): =n means every nth point will be used for creating the graph. Defaults to 1.

    Returns:
        int: Longest shortest path, corresponds to filament length
    """
    label_clump = clump_select(clump_num, label_arr)
    data = ((clump_flatten(label_clump).astype(float)).T)

    print(f"Points in the clump: {len(data)}")
    print(f"Running with {n_jobs} jobs")

    a = time.time()
    adj_mat = (np.abs(skm.pairwise_distances(data[::skip_data,0].reshape(-1,1) / skip_data, n_jobs=n_jobs))<=k_n) & \
              (np.abs(skm.pairwise_distances(data[::skip_data,1].reshape(-1,1) / skip_data, n_jobs=n_jobs))<=k_n) & \
              (np.abs(skm.pairwise_distances(data[::skip_data,2].reshape(-1,1) / skip_data, n_jobs=n_jobs))<=k_n)

    np.fill_diagonal(adj_mat, False)

    b = time.time()
    print(f"Calculating adjucency matrix: {b-a} s")

    a = time.time()
    graph_nx = nx.from_numpy_array(adj_mat.astype(int))
    b = time.time()
    print(f"Creating graph: {b-a} s")

    a = time.time()
    path_length = dict(nx.all_pairs_shortest_path_length(graph_nx))
    b = time.time()
    print(f"Calculating path lengths: {b-a} s")

    a = time.time()
    max_path_length = 0
    max_path_pair = [0]*2
    for k1 in path_length.keys():
        for k2 in path_length[k1].keys():
            if path_length[k1][k2]>max_path_length:
                max_path_length = path_length[k1][k2]
                max_path_pair = [k1,k2]

    b = time.time()
    print(f"Finding longest length: {b-a} s")
    print(f"Longest path: {max_path_length}")
    print(f"Longest path skip_data(={skip_data}): {max_path_length*skip_data}")
    print( "_______________________________________________")



    del (adj_mat)
    del(label_clump)

    if __name__=="__main__":
        gc.collect()
        return max_path_length*skip_data, max_path_pair, graph_nx, data
    else:
        del(graph_nx)
        del(path_length)
        del(data)
        gc.collect()
        return max_path_length*skip_data



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

    plt.style.use('dark_background') 

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

    #*_______________________________________________________________________________*#

    n_blob_sp, label_arr_sp = clump_finder(T, cut, above_cut=False)

    def alpha_plot(c_arr, log_flag=False):
        return pt.poly_alpha(c_arr,log_flag=log_flag, order=1, cut=0)#,cut=np.sqrt(frac_aniso.min()*frac_aniso.max()))

    clump_num = 8 
    rho_cut = 10

    label_arr_select = clump_select(clump_num, label_arr_sp)*(rho>rho_cut)
    L = np.shape(label_arr_select)

    fig, ax, sc  = pt.render_scatter_3d(inp_arr = label_arr_select, \
                             alpha_fn = alpha_plot,\
                             cmap="Paired")
    plt.show()

    #*_______________________________________________________________________________*#
    # Clump size from 

    clump_sz = clump_size(clump_num, label_arr_sp, clump_centering=False)    

    print("___________________________________________________")

    #*_______________________________________________________________________________*#

    skip_data = 4
    return_list = clump_length(clump_num, label_arr_sp, skip_data=skip_data)

    max_path_length = return_list[0]
    k1, k2          = return_list[1]
    graph_nx        = return_list[2]
    data            = return_list[3]

    max_path = nx.dijkstra_path(graph_nx, k1, k2)
    max_path = np.array(max_path)*skip_data 

    max_coord = data[max_path]

    fig, ax = new_plot()

    ax.scatter3D(data[::skip_data,0], data[::skip_data,1], data[::skip_data,2], alpha=0.5, color='C3', s=200)
    ax.plot(max_coord[:,0], max_coord[:,1], max_coord[:,2], zorder=5, linewidth=4)

    ax.set_title(f"skip_data={skip_data}, length={max_path_length}")

    plt.show()

    # #*_______________________________________________________________________________*#
    # v1 = np.load('data/v1.npy')
    # v2 = np.load('data/v2.npy')
    # v3 = np.load('data/v3.npy')

    # v_arr = [v1,v2,v3]

    # nbr_arr = boundary_detect(label_arr_sp)

    # shear_dict, shear_map = shear_calc(label_arr_sp, v_arr)

    # def grad_alpha(c_arr, log_flag=False):

    #     alpha0 = 1.0
    #     alp = alpha0 * (c_arr-c_arr.min())/(c_arr.max()-c_arr.min())
    #     alp[c_arr==0] = 0.0
    #     return alp

    # plt.hist(np.array(shear_dict['shear_vmag']))
    # plt.title('Shear histogram')
    # plt.show()

    # # %matplotlib qt 

    # fig, ax, sc  = pt.render_scatter_3d(inp_arr = shear_map, \
    #                          alpha_fn = grad_alpha,\
    #                          cmap=cr.neon)
    # norm = mt.colors.Normalize(vmin=shear_map.min(), vmax=shear_map.max())
    # fig.colorbar(mt.cm.ScalarMappable(norm=norm, cmap=cr.neon), ax=ax)

    # ax.set_title('Shear map')

    # plt.show()