import numpy as np
import cmasher as cr
import matplotlib
import matplotlib.pyplot as plt
import os
import sys

from structure_tensor import eig_special_3d, structure_tensor_3d, parallel_structure_tensor_analysis
import structure_tensor_own as sto

import array_operations as ao

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import array_operations as ao

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer

# plt.style.use('../plot/plot_style.mplstyle')
plt.style.use('dark_background')


def coherence(inp_arr, sigma=1.5, window=5.5, algo_select='package'):
    """
    Returns array of 2d coherence values along each pair of axes
    Let Li and Lj be any two eigenvalues
    This returns an array of ( (Li-Lj) / (Li+Lj) )^2

    Args:
        inp_arr (numpy array): Input array for coherence calculation
        sigma (float, optional): Standard deviation for smoothening. Defaults to 1.5.
        window (float, optional): Window for the calculation. Defaults to 5.5.
        algo_select (str, optional): Which structure_tensor function to use. Defaults to 'package'.

    Returns:
        Numpy array of arrays (3xNxNxN): coherence array calculated for each unique pair of axes
    """

    L = np.shape(inp_arr)
    dim = len(L)

    if algo_select=='own':
        S_arr = sto.structure_tensor(inp_arr)
        S_eval, S_evec = sto.S_eig(S_arr)
    elif algo_select=='package':
        S_arr = structure_tensor_3d(inp_arr, sigma=sigma, rho=window)
        S_eval, S_evec = eig_special_3d(S_arr, full=True)

    coh = [0]*dim
    for i in range(dim):
        j = np.mod(i+1, dim)

        coh[i]  = (S_eval[i]-S_eval[j])**2
        coh[i] /= (S_eval[i]+S_eval[j])**2

    return np.array(coh)

def fractional_anisotropy(inp_arr, sigma=1.5, window=5.5, algo_select='package', parallel_flag=False, devices=None):
    """
    Returns fractional anisotropy values
    Let Li be any two eigenvalues
    This returns the square root of sum( (Li-Lj)^2 ) / (2*sum(Li^2))

    Args:
        inp_arr (numpy array): Input array for coherence calculation
        sigma (float, optional): Standard deviation for smoothening. Defaults to 1.5.
        window (float, optional): Window for the calculation. Defaults to 5.5.
        algo_select (str, optional): Which structure_tensor function to use. Defaults to 'package'.

    Returns:
        float: fractional anisotropy values
    """

    L = np.shape(inp_arr)
    dim = len(L)
    if dim not in [2,3]:
        raise ValueError("coherence.py::fractional_anisotropy(): Input array can only be 2 or 3-dimensional...")

    if algo_select=='own':
        if parallel_flag:
            print('coherence.py::fractional_anisotropy(): Provided "algo_select" is not compatible with parallel_flag=True...')
            print('Calculation is proceeding with single core...')
        S_arr = sto.structure_tensor(inp_arr)
        S_eval, S_evec = sto.S_eig(S_arr)
    elif algo_select=='package':

        if dim==3:
            if parallel_flag:
                if devices is None:
                    print('coherence.py::fractional_anisotropy(): "devices" is needed for parallel_flag=True...')
                    print("Proceeding with devices=2*['cpu']...")
                    devices = 2*['cpu']

                cores = len(devices)
                # block_size = int((np.prod(L)/cores)**(1/3))
                block_size = L[0]
                print(f'All good at {block_size = }')

                S_evec, S_eval = parallel_structure_tensor_analysis(inp_arr, sigma=sigma, rho=window, devices=devices, block_size=block_size)
                print(f'All good at S_evec and s_eval')

            else:
                S_arr = structure_tensor_3d(inp_arr, sigma=sigma, rho=window)
                S_eval, S_evec = eig_special_3d(S_arr, full=True)
                

        elif dim==2:
            if parallel_flag:
                print('coherence.py::fractional_anisotropy(): Provided "algo_select" is not compatible with 2D input array and parallel_flag=True...')
                print('Calculation is proceeding with single core...')

            S_arr = structure_tensor_3d(inp_arr, sigma=sigma, rho=window)
            S_eval, S_evec = eig_special_3d(S_arr, full=True)

    frac_an_num = 0
    frac_an_den = 0

    for i in range(dim):
        j = np.mod(i+1, dim)

        frac_an_num += (S_eval[i]-S_eval[j])**2
        frac_an_den += S_eval[i]**2

    print(f'All good at {len(frac_an_num) = }')
        
    return np.sqrt(0.5*frac_an_num/frac_an_den)


def frac_aniso_window_variation(inp_arr, sigma=1.5, window_list=None, num=None, algo_select='package', parallel_flag=False, devices=None):
    """
    Returns average fractional anisotropy values for different window sizes

    Args:
        inp_arr (numpy array): Input array for coherence calculation
        sigma (float, optional): Standard deviation for smoothening. Defaults to 1.5.
        window (float, optional): Window for the calculation. Defaults to 5.5.
        num (int, optional): Size of window_list, used only if window_list is not provided. Defaults to 25.
        algo_select (str, optional): Which structure_tensor function to use. Defaults to 'package'.

    Returns:
        list: List of two lists. First one is a list fractional anisotropy, and second is window_list
    """

    coh_list = []

    L = np.array(np.shape(inp_arr))

    if window_list is None:
        if num is None:
            print('coherence.py::frac_aniso_window_variation(): "num" should be provided if "window_list" is not...')
            print('Proceeding with "num" is set to 25 ...')
            num = 25

        # Sets window from sigma to 1/4th of half of box
        # The division of 2.0 is explained in data_analysis.array_operations.gaussian_filter()
        window_list = np.linspace(sigma, int(np.min(L)/2) + 0.5, num=num)

    for i_wnd, wnd in enumerate(window_list):

        print(f'i_wnd  : {i_wnd}')
        print(f'wnd    : {wnd}'  )

        coh_avg  =  np.sum(
                            fractional_anisotropy(inp_arr, sigma=sigma, window=wnd, \
                                         algo_select=algo_select, \
                                         parallel_flag=parallel_flag, devices=devices)
                    )
        coh_avg /= np.product(L)

        print(f'coh_avg: {coh_avg}')

        coh_list.append(coh_avg)

    return [coh_list, window_list]



if __name__ == "__main__":

    rho = np.load('data/rho.npy')

    coh = coherence(rho)
    coh_sum = np.sum(coh, axis=0)

    def alpha_plot(c_arr, log_flag=False):
        return pt.poly_alpha(c_arr,log_flag=log_flag, order=1,cut=10)

    fig, ax, sc  = pt.render_scatter_3d(inp_arr = coh_sum*rho, \
                             alpha_fn = alpha_plot,\
                             cmap=cr.neon)

    fig, ax, sc  = pt.render_scatter_3d(inp_arr = rho, \
                             alpha_fn = pt.lin_alpha,\
                             cmap=cr.neon)

#     grad_rho = ao.gradient(rho)


#     def grad_alpha(c_arr, log_flag=False):

#         alpha0 = 1.0
#         return alpha0*c_arr/c_arr.max()


#     fig, ax, sc  = pt.scatter_3d(inp_arr = rho, \
#                              cut = 25, \
#                              col_data = grad_rho[0], \
#                              cmap=cr.neon, \
#                              above_cut=True)

#     plt.show()

#     grad_mag  = grad_rho[0]*grad_rho[0]
#     grad_mag += grad_rho[1]*grad_rho[1]
#     grad_mag += grad_rho[2]*grad_rho[2]
#     grad_mag  = np.sqrt(grad_mag)

#     grad_cut = np.max(grad_mag) + 1 

# #    if True:
# #        %matplotlib qt

#     fig, ax, sc  = pt.render_scatter_3d(inp_arr = grad_mag, \
#                              alpha_fn = grad_alpha,\
#                              cmap=cr.neon)

#     # ax.get_yaxis().set_visible(False)

#     fig.savefig('filament_grad.png')
#     plt.show()
