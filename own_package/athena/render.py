import numpy as np
import cmasher as cr 
import sys
import os



cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as p3d
import video as vid 

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 

@timer
def render(field, file_loc, img_loc=None, MHD_flag=False,\
           fig=None, ax=None, new_fig=True, \
           cut=0.0, cut_above=False, 
           view = [30,-60], \
           log_flag=False, return_ax=True,\
           cmap='plasma'):

    out_dict = dr.get_array_athena(file_loc, fields=[field],MHD_flag=MHD_flag)

    try:
        plot_arr = out_dict[field]
    except KeyError:
        print(f"!! '{field}' not found in the data file... ")
        print(f"Available fields are:")
        print(f"{out_dict.keys()}")

    def alpha_plot(c_arr, log_flag):
        return p3d.lin_alpha(c_arr, cut=cut, cut_above=cut_above, log_flag=log_flag)

    fig, ax, sc = p3d.render_scatter_3d(inp_arr=out_dict[field],\
                                        alpha_fn = alpha_plot, \
                                        log_flag=log_flag,\
                                        view=view,\
                                        cmap=cmap,\
                                        fig=fig, ax=ax, new_fig=new_fig)

    if img_loc is not None:
        fig.savefig(img_loc)

    print('Render done ...')

    if return_ax:
        return ax

@timer
def render_rotate_video (field, file_list, img_list, MHD_flag,\
                         cut=0.0, cut_above=False, 
                         angle_start=0, angle_end=360,\
                         log_flag=False):

    import matplotlib
    matplotlib.use('Agg')

    N_angle = len(file_list)
    angle_arr = np.linspace(angle_start, angle_end, num=N_angle)

    for i_fl, fl in enumerate(file_list):

        i_view = [30, angle_arr[i_fl]]

        render(field, fl, img_list[i_fl], MHD_flag,\
               cut=cut, cut_above=cut_above,\
               view=i_view,\
               log_flag=log_flag, return_ax=False)  

    print('Rotating render done ...')

if __name__ == "__main__":

    file_loc  = '/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/turb_v2/'
    file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_beta_100/'
    # file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'
    file_loc += 'Turb.out2.00548.athdf'

    MHD_flag = True

    # img_loc = './render_test.png'

    # render('rho', file_loc, img_loc, MHD_flag, cut=9, log_flag=False)

    file_list = [file_loc] * 60
    img_list  = [f'./render_test_dir/test_{str(i).zfill(2)}.png' for i in range(60)]

    render_rotate_video('rho', file_list, img_list, MHD_flag, cut=9, angle_start=-40, angle_end=-100)