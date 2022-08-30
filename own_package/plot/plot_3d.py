import numpy as np
import matplotlib
import matplotlib as mt



import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import cmasher as cr

def new_plot():

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection='3d')

    return fig,ax

def const_alpha (x, cut=0.0, cut_above=False, log_flag=False):

    alpha_0 = 0.5
    return np.ones_like(x)*alpha_0

def poly_alpha(c_arr, order=2, log_flag=False, cut=0.0, cut_above=False):

    alpha0 = 1.0

    if log_flag:
        log_c_arr = np.log10(c_arr)
        alp = alpha0 * (log_c_arr-log_c_arr.min())/(log_c_arr.max()-log_c_arr.min())
    else:
        alp = alpha0 * (c_arr-c_arr.min())**order/(c_arr.max()-c_arr.min())**order

    if cut_above:
        alp[c_arr>(c_arr.min()+cut)] = 0.0
    else:
        alp[c_arr<(c_arr.min()+cut)] = 0.0

    alp[c_arr==0] = 0.0

    return alp

def lin_alpha(c_arr, log_flag=False, cut=0.0, cut_above=False):

    alpha0 = 1.0

    if log_flag:
        log_c_arr = np.log10(c_arr)
        alp = alpha0 * (log_c_arr-log_c_arr.min())/(log_c_arr.max()-log_c_arr.min())
    else:
        alp = alpha0 * (c_arr-c_arr.min())/(c_arr.max()-c_arr.min())

    if cut_above:
        alp[c_arr>(c_arr.min()+cut)] = 0.0
    else:
        alp[c_arr<(c_arr.min()+cut)] = 0.0

    alp[c_arr==0] = 0.0

    return alp

def make_color (c_arr, alpha_arr, cmap_name, log_flag = False):

    cmap = mt.cm.get_cmap(cmap_name)
    
    if log_flag:
        cb_qnt = np.copy(np.log10(c_arr))
    else:
        cb_qnt = np.copy(c_arr)

    line_col = cmap(cb_qnt/cb_qnt.max())

    line_col[:,3] = alpha_arr

    return line_col

def make_plot_list (inp_arr, col_data, cond_arr):

    L = np.shape(inp_arr)

    plot_list = []

    for i in range(L[0]):
        for j in range(L[1]):
            for k in range(L[2]):

                if cond_arr[i,j,k]:
                    plot_list.append([\
                                      i, j, k,         \
                                      col_data[i,j,k]
                                     ])

    return plot_list


# TODO: Add the interactive feature in this function instead

# TODO: Add the feature to plot using voxel plot instead of scatter

def scatter_3d ( inp_arr, cut, col_data,             \
                 cmap=cr.rainforest, above_cut=True, \
                 alpha_fn = const_alpha,             \
                 pnt_size = 50,                      \
                 log_flag = False,                   \
                 view = [30, -60],                   \
                 new_fig=True, fig=None, ax=None):

    if new_fig:
        fig, ax = new_plot()

    if above_cut:
        cond_arr = inp_arr>cut
    else:
        cond_arr = inp_arr<cut

    plot_list = make_plot_list(inp_arr, col_data, cond_arr)
    plot_list = np.array(plot_list)

    i_arr = plot_list[:,0]
    j_arr = plot_list[:,1]
    k_arr = plot_list[:,2]

    c_arr     = plot_list[:,3]
    alpha_arr = alpha_fn(c_arr)

    color = make_color(c_arr,alpha_arr, cmap, log_flag=log_flag)

    sc = ax.scatter3D(i_arr, j_arr, k_arr,\
                 c=color,            \
                 s=pnt_size, edgecolors='None',\
                 cmap=cmap,          \
                 depthshade=True)

    ax.view_init(elev=view[0], azim=view[1])

    return fig, ax, sc

def render_scatter_3d ( inp_arr,          \
                 cmap=cr.rainforest,      \
                 alpha_fn = const_alpha,  \
                 pnt_size = 50,           \
                 log_flag = False,        \
                 view = [30, -60],        \
                 coord = [None, None, None], new_fig=True, fig=None, ax=None):       
                 
    if new_fig:
        fig, ax = new_plot()

    if None in coord:
        L = np.shape(inp_arr)
        i = np.array(range(L[0]))
        j = np.array(range(L[1]))
        k = np.array(range(L[2]))

        i_arr, j_arr, k_arr = np.meshgrid(i,j,k)

        i_arr = np.ravel(i_arr, order='C')
        j_arr = np.ravel(j_arr, order='C')
        k_arr = np.ravel(k_arr, order='C')
    else:

        i_arr = coord[0]
        j_arr = coord[1]
        k_arr = coord[2]

        i_arr = np.ravel(i_arr, order='C')
        j_arr = np.ravel(j_arr, order='C')
        k_arr = np.ravel(k_arr, order='C')

    c_arr = np.ravel(inp_arr, order='C') 

    # TODO: Add log scaling in alpha_fn
    alpha_arr = alpha_fn(c_arr, log_flag=log_flag)

    color = make_color(c_arr, alpha_arr, cmap, log_flag=log_flag)

    sc = ax.scatter3D(i_arr, j_arr, k_arr,          \
                 c=color,                      \
                 s=pnt_size, edgecolors='None',\
                 cmap=cmap,                    \
                 depthshade=True)

    ax.view_init(elev=view[0], azim=view[1])

    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    return fig, ax, sc