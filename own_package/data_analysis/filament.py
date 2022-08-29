import numpy as np
import cmasher as cr
import matplotlib
import matplotlib.pyplot as plt

import array_operations as ao

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt
# plt.style.use('../plot/plot_style.mplstyle')
plt.style.use('dark_background')

# TODO: Structure tensor

if __name__ == "__main__":

    rho = np.load('data/rho.npy')

    grad_rho = ao.gradient(rho)


    def grad_alpha(c_arr):

        alpha0 = 1.0
        return alpha0*c_arr/c_arr.max()


    fig, ax  = pt.scatter_3d(inp_arr = rho, \
                             cut = 25, \
                             col_data = grad_rho[0], \
                             cmap=cr.neon, \
                             above_cut=True)

    plt.show()

    grad_mag  = grad_rho[0]*grad_rho[0]
    grad_mag += grad_rho[1]*grad_rho[1]
    grad_mag += grad_rho[2]*grad_rho[2]
    grad_mag  = np.sqrt(grad_mag)

    grad_cut = np.max(grad_mag) + 1 

    if True:
        %matplotlib qt

    fig, ax  = pt.render_scatter_3d(inp_arr = grad_mag, \
                             col_data = grad_mag, \
                             alpha_fn = grad_alpha,\
                             cmap=cr.neon)

    # ax.get_yaxis().set_visible(False)

    plt.show()