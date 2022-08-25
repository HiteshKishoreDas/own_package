import numpy as np
import cmasher as cr
import matplotlib.pyplot as plt

import array_operations as ao

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt



if __name__ == "__main__":

    rho = np.load('data/rho.npy')

    grad_rho = ao.gradient(rho)

    grad_cut = 30

    fig, ax  = pt.scatter_3d(rho, 25, grad_rho[0], cmap=cr.neon, above_cut=True)
    plt.show()

    grad_mag  = grad_rho[0]*grad_rho[0]
    grad_mag += grad_rho[1]*grad_rho[1]
    grad_mag += grad_rho[2]*grad_rho[2]
    grad_mag  = np.sqrt(grad_mag)

    fig, ax  = pt.scatter_3d(grad_mag, grad_cut, grad_mag, cmap=cr.neon, above_cut=True)
    fig, ax  = pt.scatter_3d(grad_mag, -grad_cut, grad_mag, cmap=cr.neon, above_cut=False,\
        new_fig=False, fig=fig, ax=ax)
    plt.show()