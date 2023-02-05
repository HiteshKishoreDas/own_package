import numpy as np
import cmasher as cr
import matplotlib
import matplotlib.pyplot as plt
import os
import sys


import array_operations as ao

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]


sys.path.insert(0, f'{package_abs_path}data_analysis/')
import array_operations as ao

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer

sys.path.insert(0, f'{package_abs_path}utils/structure_tensor_fork/')
from structure_tensor import eig_special_3d, structure_tensor_3d, parallel_structure_tensor_analysis
import structure_tensor_own as sto

# plt.style.use('../plot/plot_style.mplstyle')
plt.style.use('dark_background')


def coherence(inp_arr, sigma=1.5, window=5.5, mode='wrap', algo_select='package'):
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
        S_arr = structure_tensor_3d(inp_arr, sigma=sigma, rho=window, mode=mode)
        S_eval, S_evec = eig_special_3d(S_arr, full=True)

    coh = [0]*dim
    for i in range(dim):
        j = np.mod(i+1, dim)

        coh[i]  = (S_eval[i]-S_eval[j])**2
        coh[i] /= (S_eval[i]+S_eval[j])**2

    return np.array(coh)

def fractional_anisotropy(inp_arr, sigma=1.5, window=5.5, mode='wrap', algo_select='package', parallel_flag=False, devices=None):
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
        Array: ND array with fractional anisotropy values
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
                block_size = int(np.ceil((np.prod(L)/cores)**(1/3)))
                print(f'All good at {block_size = }')

                S_evec, S_eval = parallel_structure_tensor_analysis(inp_arr, sigma=sigma, rho=window, mode=mode, devices=devices, block_size=block_size)
                print(f'All good at S_evec and s_eval')

            else:
                S_arr = structure_tensor_3d(inp_arr, sigma=sigma, rho=window, mode=mode)
                S_eval, S_evec = eig_special_3d(S_arr, full=True)
                

        elif dim==2:
            if parallel_flag:
                print('coherence.py::fractional_anisotropy(): Provided "algo_select" is not compatible with 2D input array and parallel_flag=True...')
                print('Calculation is proceeding with single core...')

            S_arr = structure_tensor_3d(inp_arr, sigma=sigma, rho=window)
            S_eval, S_evec = eig_special_3d(S_arr, full=True)

    # These variables are elongation and flatness in the inp_arr
    # Elongation in the inp_arr corresponds to flatness of eigen-ellipsoid
    elongation = S_eval[1]/S_eval[0]
    # Flatness in the inp_arr corresponds to elongation of eigen-ellipsoid
    flatness = S_eval[2]/S_eval[1]

    # filamentariness in the inp_arr
    filamentariness = elongation/flatness

    if __name__=='__main__':
        return S_eval
    else:
        return filamentariness


def frac_aniso_window_variation(inp_arr, sigma_start=1.5, sigma_wnd_mul=3.0, mode='wrap', \
                                avg_mask=None, window_list=None, \
                                weights=None, num=None, \
                                algo_select='package', parallel_flag=False, devices=None):
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


    if avg_mask is None:
        avg_mask = np.ones_like(inp_arr)

    if window_list is None:
        if num is None:
            print('coherence.py::frac_aniso_window_variation(): "num" should be provided if "window_list" is not...')
            print('Proceeding with "num" is set to 25 ...')
            num = 25

        # Sets window from sigma to 1/4th of half of box
        # The division of 2.0 is explained in data_analysis.array_operations.gaussian_filter()
        window_list = np.logspace(np.log10(3*sigma_start), np.log10(int(np.min(L)/2) + 0.5), num=num)

    for i_wnd, wnd in enumerate(window_list):

        print(f'i_wnd  : {i_wnd}')
        print(f'wnd    : {wnd}'  )

        coh_avg  =  np.average(
                            fractional_anisotropy(inp_arr, sigma=wnd/sigma_wnd_mul, window=wnd, \
                                         algo_select=algo_select, \
                                         parallel_flag=parallel_flag, mode=mode,devices=devices)*avg_mask,
                    weights=weights)

        print(f'coh_avg: {coh_avg}')

        coh_list.append(coh_avg)

    return [coh_list, window_list]



if __name__ == "__main__":

    sys.path.insert(0, f'{package_abs_path}plot/')
    import plot_3d as pt

    rho = np.load('data/rho.npy')
    T = np.load('data/prs.npy')/np.load('data/rho.npy')
    T_cut = np.sqrt(T.min()*T.max())

    L = np.shape(T)

    k = 5
    L = (128,128,128)     
    r = np.indices(L)
    T = np.sin(2*np.pi*k*r[0]/L[0]) + np.sin(2*np.pi*k*r[1]/L[1]) + 0.1*np.sin(2*np.pi*r[2]/L[2])
    # T = np.sin(2*np.pi*k*r[0]/L[0]) + np.sin(2*np.pi*k*r[1]/L[1]) + np.sin(2*np.pi*k*r[2]/L[2])
    T += 4.0
    T *= T_cut

    coh = coherence(rho)
    coh_sum = np.average(coh, axis=0)

    length_scale = 2.5 
    wnd = int(np.ceil(3*length_scale))

    frac_aniso = fractional_anisotropy(T, sigma=length_scale, mode='wrap',window=3*length_scale)
    frac_aniso[0][T>np.sqrt(T.min()*T.max())] = 0
    frac_aniso[1][T>np.sqrt(T.min()*T.max())] = 0
    frac_aniso[2][T>np.sqrt(T.min()*T.max())] = 0

    # plt.figure()
    # plt.imshow((frac_aniso[0])[:, int(L[0]/2), :])#, vmin=0, vmax=3.0)
    # plt.colorbar()
    # plt.show()

    # plt.figure()
    # plt.imshow((frac_aniso[1])[:, int(L[0]/2), :])#, vmin=0, vmax=3.0)
    # plt.colorbar()
    # plt.show()
    
    # plt.figure()
    # plt.imshow((frac_aniso[2])[:, int(L[0]/2), :])#, vmin=0, vmax=3.0)
    # plt.colorbar()
    # plt.show()

    plt.figure()
    elongation = (frac_aniso[1]/frac_aniso[0])
    plt.imshow(elongation[:, int(L[0]/2), :])#, vmin=0, vmax=3.0)
    plt.title('Elongation')
    plt.colorbar()
    plt.show()

    plt.figure()
    flatness = (frac_aniso[2]/frac_aniso[1])
    plt.imshow(flatness[:, int(L[0]/2), :])#, vmin=0, vmax=3.0)
    plt.title('Flatness')
    plt.colorbar()
    plt.show()

    plt.figure()
    filamentarines = elongation/flatness
    plt.imshow(filamentarines[:, int(L[0]/2), :])#, vmin=0, vmax=3.0)
    plt.title('Filamentariness')
    plt.colorbar()
    plt.show()

    # def alpha_plot(c_arr, log_flag=False):
    #     return pt.poly_alpha(c_arr,log_flag=log_flag, order=1, cut= 0.5 ,cut_above=True)  # np.sqrt(frac_aniso.min()*frac_aniso.max()))

    # fig, ax, sc  = pt.render_scatter_3d(inp_arr = frac_aniso, \
    #                          alpha_fn = alpha_plot,\
    #                          cmap=cr.neon)

    T[T>np.sqrt(T.min()*T.max())] = 100.0 

    plt.figure()
    # plt.imshow(T[:,:, int(L[0]/2)])
    plt.imshow(T[:,int(L[0]/2), :])
    plt.title(r"Temperature $(p/\rho)$ ($T>T_{\rm cut} = 100$)")
    plt.colorbar()
    plt.show()
    

    # def alpha_plot(c_arr, log_flag=False):
    #     # return pt.poly_alpha(c_arr,log_flag=log_flag, order=1,cut=np.sqrt(T.min()*T.max()), cut_above=True )
    #     return pt.lin_alpha(c_arr,log_flag=log_flag, cut=T_cut, cut_above=True)

    # fig, ax, sc  = pt.render_scatter_3d(inp_arr = T, \
    #                          alpha_fn = alpha_plot,\
    #                          cmap=cr.neon)

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
