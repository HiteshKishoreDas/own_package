import matplotlib.pyplot as plt
import cmasher as cr
import os
import sys
import numpy as np

import projection_render as pr
import parallel as prl

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]

sys.path.insert(0, f"{package_abs_path}athena/")
import athena_hdf5_direct_read as hd

theme = "dark"
# theme = "bright"

# import plot_3d as p3d
# import video as vid

N_procs_default = 2

n_arg = len(sys.argv) - 1
if n_arg == 0:
    print(f"N_procs not provided...")
    print(f"N_procs set to default: {N_procs_default} processors..")
    N_procs = N_procs_default
elif n_arg == 1:
    N_procs = int(sys.argv[1])
    print(f"N_procs set to: {N_procs} processors..")
else:
    print(f"Too many arguments provided...")
    print(f"N_procs set to default: {N_procs_default} processors..")
    N_procs = N_procs_default

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]

style_lib = f"{package_abs_path}style_lib/"

if theme == "dark":
    pallette = style_lib + "dark_pallette.mplstyle"
elif theme == "bright":
    pallette = style_lib + "bright_pallette.mplstyle"

plot_style = style_lib + "plot_style.mplstyle"
text_style = style_lib + "text.mplstyle"

plt.style.use([pallette, plot_style, text_style])


# *_________________PARAMETERS___________________* #
# *______________________________________________* #

MHD_flag = True

# If true, the time is fixed at 650
# If false, the time is varied from 501 to 650
# The box is rotated in both cases
fixed_time = True

# Azimuthal angle
phi = np.pi / 4
if fixed_time:

    theta_arr = np.linspace(2 * np.pi, 0, num=360)
else:
    theta_arr = np.linspace((650 - 501) * (np.pi / 180), 0, num=(650 - 501))

# *______________________________________________* #


# * Read the initial file
if MHD_flag:
    rho_full0 = hd.read_hdf5(
        filename=f"/ptmp/mpa/hitesh/data/Rlsh_1000_res_256_M_0.5_beta_100/Turb.out2.00650.athdf",
    )
else:
    rho_full0 = hd.read_hdf5(
        filename=f"/ptmp/mpa/hitesh/data/Rlsh_1000_res_256_M_0.5_hydro/Turb.out2.00650.athdf",
    )

# * Read the file
N = 650
if MHD_flag:
    print(f"Read the file for {MHD_flag = }, and {N = }")
    rho_full = hd.read_hdf5(
        filename=f"/ptmp/mpa/hitesh/data/Rlsh_1000_res_256_M_0.5_beta_100/Turb.out2.{str(N).zfill(5)}.athdf",
    )
else:
    print(f"Read the file for {MHD_flag = }, and {N = }")
    rho_full = hd.read_hdf5(
        filename=f"/ptmp/mpa/hitesh/data/Rlsh_1000_res_256_M_0.5_hydro/Turb.out2.{str(N).zfill(5)}.athdf",
    )

# *______________________________________________* #


# * Transfer function
def alpha_func(x, x_0=0.5, rate=10.0):
    a = x - x.min()
    a /= a.max()
    return 1 / (1 + np.exp(rate * (x_0 - a)))


# * Define some 3D points
grid_shape = np.shape(rho_full0)
grid = np.mgrid[0 : grid_shape[0], 0 : grid_shape[1], 0 : grid_shape[2]]

points = np.vstack(
    (
        grid[0].ravel(),
        grid[1].ravel(),
        grid[2].ravel(),
    )
).T


# * Main function to calculate and save the render
def projection_render_fn(args):
    i, rho_full, alpha, theta_arr, phi = args
    print(i)
    if not fixed_time:
        if MHD_flag:
            print(f"Read the file for {MHD_flag = }, and {i = }")
            rho_full = hd.read_hdf5(
                filename=f"/ptmp/mpa/hitesh/data/Rlsh_1000_res_256_M_0.5_beta_100/Turb.out2.{str(i).zfill(5)}.athdf",
            )
        else:
            print(f"Read the file for {MHD_flag = }, and {i = }")
            rho_full = hd.read_hdf5(
                filename=f"/ptmp/mpa/hitesh/data/Rlsh_1000_res_256_M_0.5_hydro/Turb.out2.{str(i).zfill(5)}.athdf",
            )

    rho_proj = np.copy(rho_full)
    rho_proj[rho_full < 5] = 5

    # * Get projected image
    rho_proj = pr.project_along_normal(
        arr=np.log10(rho_proj),
        # arr=alpha,
        points=points,
        camera_view=[theta_arr[i], phi],
        # alpha=alpha,
    )

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

    colormap = cr.torch

    ax.imshow(
        # np.log10(rho_proj),
        rho_proj,
        cmap=colormap,
        interpolation="gaussian",
        # interpolation_stage="rgba",
        alpha=1.0,
        # vmin = np.sqrt(rho_proj.min()*rho_proj.max()),
        # vmin = np.sqrt(rho_proj.min()*rho_proj.max()),
        # vmax=rho_proj.max() * 0.8,
    )

    ax.grid(False)
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])

    if fixed_time:
        plt.savefig(f"rho_projection_{str(i+(650-501)).zfill(5)}.png", dpi=600)
    else:
        plt.savefig(f"rho_projection_{str(i).zfill(5)}.png", dpi=600)

    return i


# *______________________________________________* #

# * Parallelise the rendering

iter_list = [
    (
        i,
        rho_full,
        alpha_func(rho_full, x_0=0.9),
        theta_arr,
        phi,
    )
    for i in range(len(theta_arr))
]
processed = prl.parallelise(
    fn=projection_render_fn,
    iter_list=iter_list,
    processes=N_procs,
)

# vid.make_video(
#     image_path="rho_projection", video_path="rho_proj", framerate=10, theme=theme
# )
