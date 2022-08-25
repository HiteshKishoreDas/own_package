import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import cmasher as cr

def new_plot():

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection='3d')

    return fig,ax


# TODO: Add feature to give transfer function
# TODO: That is, a function to calculate the alpha of each point
# TODO: This will full on rendering, so maybe make a different function for that.

def scatter_3d ( inp_arr, cut, col_data, cmap, above_cut=True, new_fig=True, fig=None, ax=None):

    if new_fig:
        fig, ax = new_plot()

    if above_cut:
        cond_arr = inp_arr>cut
    else:
        cond_arr = inp_arr<cut

    L = np.shape(inp_arr)
    # print(L)

    plot_list = []

    alpha0 = 0.25

    for i in range(L[0]):
        for j in range(L[1]):
            for k in range(L[2]):

                if cond_arr[i,j,k]:
                    plot_list.append([i,j,k,col_data[i,j,k]])

    plot_list = np.array(plot_list)

    ax.scatter3D(plot_list[:,0],plot_list[:,1],plot_list[:,2],\
                 c=plot_list[:,3], s=100, alpha=0.25, edgecolors='None',\
                 cmap=cmap)

    return fig,ax
