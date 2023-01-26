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

# plt.style.use('../plot/plot_style.mplstyle')
plt.style.use('dark_background')

# TODO: Maybe fix structure tensor

def gauss(r, sigma):

    gs  = 1/(np.sqrt(2*np.pi*sigma*sigma))
    gs *= np.exp(-(r**2)/(2*sigma**2)   )

    return gs

def radius_grid (L):

    x = [ np.array(range( -int(l/2), int(l/2)+1  )) for l in L   ]

    X = np.meshgrid(*x)

    R = np.sum(np.array(  [ x**2 for x in X ] ), axis=0)
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

@timer
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
    S_arr = np.zeros((dim, dim,*L), dtype=float)

    # tup = tuple(np.newaxis for i in range(dim))

    tup  = [ slice(None) for i in range(dim) ]
    tup += [ np.newaxis  for i in range(dim) ]
    tup  = tuple(tup)

    nbr_ind = [  np.mod( X_inp[i][tup] + X_nbr[i], L[i]  )  \
                    for i in range(dim) ]

    sum_tup = tuple(-i for i in range(1,dim+1))

    for i in range(dim):
        for j in range(dim):

            nbr_tup = tuple([i,j,*nbr_ind])

            S_temp = S0_arr[nbr_tup]
            S_arr[i,j] = np.sum(S_temp*w_arr, axis=sum_tup)

    print('S_arr: ',np.shape(S_arr))

    return S_arr

@timer
def S_eig (S_arr):

    L = np.shape(S_arr)[2:]
    dim = len(L)

    S_new    = np.zeros((*L,dim,dim), dtype=float )

    for i in range(dim):
        for j in range(dim):

            new_tup  = [slice(None) for i in range(dim)]
            new_tup += [i,j]
            new_tup  = tuple(new_tup)

            S_new[new_tup] = S_arr[i,j]

    S_eval, S_evec = np.linalg.eig(S_new)

    S_eval_new = np.zeros((dim,*L)    , dtype=float )
    S_evec_new = np.zeros((dim,dim,*L), dtype=float )

    new_tup = [slice(None) for i in range(dim)]

    for i in range(dim):
        
        new_tup_val = new_tup + [i]
        new_tup_val = tuple(new_tup_val)

        S_eval_new[i] = S_eval[new_tup_val]
        
        for j in range(dim):

            new_tup_vec = new_tup + [i,j]
            new_tup_vec = tuple(new_tup_vec)

            S_evec_new[i,j] = S_evec[new_tup_vec]

    return S_eval_new, S_evec_new

