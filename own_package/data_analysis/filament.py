import numpy as np
import cmasher as cr
import matplotlib
import matplotlib.pyplot as plt
import os
import sys

import array_operations as ao

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import array_operations as ao

# plt.style.use('../plot/plot_style.mplstyle')
plt.style.use('dark_background')

# TODO: Structure tensor

def gauss(r, sigma):

    gs  = 1/(np.sqrt(2*np.pi*sigma*sigma))
    gs *= np.exp(-(r**2)/(2*sigma**2)   )

    return gs

def radius_grid (L):

    x = [ np.array(range( -int(l/2), int(l/2)+1  )) for l in L   ]

    X = np.meshgrid(*x)

    R = np.sum(np.array(  [ x**2 for x in X ] ))
    R = np.sqrt(R)

    return R, X

def S0 (inp_arr):

    L = np.shape(inp_arr)
    dim = len(L)
    
    S0_arr = np.zeros((dim,dim,*L), dtype=float)

    grad = ao.gradient(inp_arr)

    for i in range(dim):
        for j in range(dim):

            S0_arr[i, j] = grad[i]*grad[j]

    return S0_arr

def structure_tensor(inp_arr, w_fn=gauss, window=5):


    if window%2 != 1:
        raise ValueError("!! window has to an odd number ...")
    else:
        win_hw = int(window/2)

    L = np.shape(inp_arr)
    dim = len(L)

    nbr_shape = [window for i in range(dim)]
    R, X_nbr = radius_grid(nbr_shape)

    x = [ np.array(range(l)) for l in L   ]
    X_inp = np.meshgrid(*x)

    # w(r) template, size = (window x window x window) for 3D
    w_arr = w_fn(R, win_hw)

    # S_0 for the input array, size = (N x N x N) for 3D
    S0_arr = S0(inp_arr)

    # Array of Sw values, size = (N x N x N)  for 3D
    # Sw_arr = np.zeros_like(inp_arr)
    # Sw_arr = np.zeros((*nbr_shape, *L,dim, dim), dtype=float)
    Snbr_arr = np.zeros((*nbr_shape, *L,dim, dim), dtype=float)
    print('Snbr_arr: ',np.shape(Snbr_arr))

    Snbr_arr[ :,:,:, X_inp[0], X_inp[1], X_inp[2],0,0] = S0_arr[0,0,X_inp[0], X_inp[1], X_inp[2]]




    # S1 = Sw_arr[:,:,:,  X_inp[0], X_inp[1], X_inp[2],0,0]
    S2 = S0_arr[0,0,np.mod(X_inp[0][:, :, :, np.newaxis, np.newaxis, np.newaxis]+X_nbr[0], L[0] ), \
                    np.mod(X_inp[1][:, :, :, np.newaxis, np.newaxis, np.newaxis]+X_nbr[1], L[1] ), \
                    np.mod(X_inp[2][:, :, :, np.newaxis, np.newaxis, np.newaxis]+X_nbr[2], L[2] )]

    

    # X_trial = X_inp[0][:, :, :, np.newaxis, np.newaxis, np.newaxis]+X_nbr[0]

    # print(np.shape(S1))
    print(np.shape(S2))
    # print(np.shape(X_trial))
    # print(X_trial[3,3,3,:,:,0])
    # print(Sw_arr[3,4,5,:,:,:])

    return Snbr_arr 


if __name__ == "__main__":

    rho = np.load('data/rho.npy')

    Sw_arr = structure_tensor(rho)




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
