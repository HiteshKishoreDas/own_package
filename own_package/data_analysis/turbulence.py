'''
Created Date: 2022-11-17 12:21:46
Author: Hitesh Das
'''

import numpy as np
import os
import sys

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import array_operations as ao


def turbulent_field (A_list, weights=None, mode='gauss', sigma=None, gauss_axis=None, axis=(1,2)):

    if weights is None:
        weights = np.ones_like(A_list[0])

    if mode=='average':

        #* Average profile in z-direction
        A_bulk = []
        A_bulk.append(np.average(A_list[0], weights=weights, axis=axis))
        A_bulk.append(np.average(A_list[1], weights=weights, axis=axis))
        A_bulk.append(np.average(A_list[2], weights=weights, axis=axis))

        #* Turbulent velocity field

        temp_slice = [slice(None) for i in range(3)]
        for ax in axis:
            temp_slice[ax] = np.newaxis
        temp_slice = tuple(temp_slice)

        A_turb = []
        A_turb.append(A_list[0] - A_bulk[0][temp_slice])
        A_turb.append(A_list[1] - A_bulk[1][temp_slice])
        A_turb.append(A_list[2] - A_bulk[2][temp_slice])


    elif mode=='gauss':

        if sigma is None:

            if gauss_axis is None:
                # main_axis = list(set([0,1,2]) - set(axis))            
                # N_main = np.shape(A_list[0])[main_axis[0]]
                gauss_axis= axis[-1]

            N_gauss= np.shape(A_list[0])[gauss_axis]
            sigma = N_gauss/8.0

            print("turbulence.py::turbulence_field()- No sigma provided for 'gauss' mode ...")
            print(f"turbulence.py::turbulence_field()- Setting sigma to N/8 = {sigma}...")

        #* Gaussian-filtered velocity field
        A_bulk = [0] * 3
        A_bulk[0] = ao.gaussian_filter(A_list[0], sigma=sigma)
        A_bulk[1] = ao.gaussian_filter(A_list[1], sigma=sigma)
        A_bulk[2] = ao.gaussian_filter(A_list[2], sigma=sigma)

        #* Turbulent velocity field
        A_turb = [0] * 3
        A_turb[0] = A_list[0] - A_bulk[0]
        A_turb[1] = A_list[1] - A_bulk[1]
        A_turb[2] = A_list[2] - A_bulk[2]

    else:
        print("!! turbulence.py::turbulence_field() !! Invalid 'mode'... ")
        print("!! turbulence.py::turbulence_field() !! Valid modes- 'gauss', 'average'... ")


    A_turb_prof = [0] * 3
    A_turb_prof[0] = np.sqrt(np.average(A_turb[0]**2, weights=weights,axis=axis))
    A_turb_prof[1] = np.sqrt(np.average(A_turb[1]**2, weights=weights,axis=axis))
    A_turb_prof[2] = np.sqrt(np.average(A_turb[2]**2, weights=weights,axis=axis))

    return_dict = {}

    return_dict['turb']      = A_turb
    return_dict['bulk']      = A_bulk
    return_dict['turb_prof'] = A_turb_prof

    
    return return_dict



if __name__=='__main__':

    import matplotlib.pyplot as plt

    A = []
    A.append(np.random.random((10,20,30)) + 0.5 )
    A.append(np.random.random((10,20,30)) + 0.45)
    A.append(np.random.random((10,20,30)) + 0.25)

    r1_dict = turbulent_field(A, mode='average')
    r2_dict = turbulent_field(A, mode='gauss')

    plt.figure()
    plt.imshow(A[0][:,:,12], vmin=-2, vmax=2, cmap='bwr')
    plt.title("Original array")
    plt.colorbar()

    plt.figure()
    plt.imshow(r1_dict['turb'][0][:,:,15], vmin=-2, vmax=2, cmap='bwr')
    plt.title("Average mode")
    plt.colorbar()

    plt.figure()
    plt.imshow(r2_dict['turb'][0][:,:,15], vmin=-2, vmax=2, cmap='bwr')
    plt.title("Gauss mode")
    plt.colorbar()

    plt.figure()
    plt.imshow(r1_dict['turb'][0][:,:,15] - r2_dict['turb'][0][:,:,15], cmap='bwr')
    plt.title("Difference between the modes")
    plt.colorbar()