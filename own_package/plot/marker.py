import matplotlib as mt
from matplotlib import scale
from matplotlib.markers import MarkerStyle
# from matplotlib.lines import Line2D
from matplotlib.transforms import Affine2D
import matplotlib.path as mpath
import numpy as np


def get_unfilled_marker (marker_type = 'o',\
                         transform=Affine2D().rotate_deg(0) ):

    mark = MarkerStyle(marker_type).get_path()
    theta = 0

    scale_factor = 0.5
    hole_vert = mark.vertices * scale_factor
    mark_vert  = np.copy(mark.vertices)

    if marker_type in ['D', 'd']:
        hole_vert  = mark.vertices-0.5

        if marker_type in ['d']:
            mark_vert[0,0] = (mark_vert[0,0] - 0.5)*0.5
            mark_vert[2,0] = (mark_vert[2,0] - 0.5)*0.5 

            hole_vert[0,0] = (hole_vert[0,0] - 0.5)*0.5*scale_factor + 0.5
            hole_vert[2,0] = (hole_vert[2,0] - 0.5)*0.5*scale_factor + 0.5 

        hole_vert *= scale_factor
        hole_vert += 0.5

        mark_vert -= 0.5
        hole_vert -= 0.5


        theta = -45

    elif marker_type in ['X']:
        scale_factor = 0.4
        hole_vert = mark.vertices * scale_factor

        vert_ind_1 = (2,6,8,12)
        vert_ind_2 = (3,5,9,11)

        hole_vert[vert_ind_1,0] *= 1/scale_factor
        hole_vert[vert_ind_1,1] *= 0.7/scale_factor

        hole_vert[vert_ind_2,0] *= 0.7/scale_factor
        hole_vert[vert_ind_2,1] *= 1/scale_factor

        # print(hole_vert)

    elif marker_type in ['^']:
        # mark_vert[:,1]  += 0.1 + 0.15
        # hole_vert[:,1]  += 0.1 
        hole_vert[:,1]  -= 0.15

    elif marker_type in ['>']:
        theta = -90

    elif marker_type in ['<']:
        theta = 90

    hole = mpath.Path(hole_vert, mark.codes)
    mark = mpath.Path(mark_vert, mark.codes)

    # concatenate the circle with an internal cutout of the star
    cut_mark = mpath.Path(
        vertices=np.concatenate([mark.vertices, hole.vertices[::-1, ...]]),
        codes=np.concatenate([mark.codes, hole.codes]))

    cut_mark = cut_mark.transformed(Affine2D().rotate_deg(theta) )

    return cut_mark.transformed(transform=transform)

if __name__=="__main__":

    import matplotlib.pyplot as plt

    def format_axes(ax):
        ax.margins(0.2)
        ax.set_axis_off()
        ax.invert_yaxis()


    def split_list(a_list):
        i_half = len(a_list) // 2
        return a_list[:i_half], a_list[i_half:]

    text_style = dict(horizontalalignment='right', verticalalignment='center',
                      fontsize=12, fontfamily='monospace')
    marker_style = dict(linestyle=':', color='0.8', markersize=40,
                        markerfacecolor="tab:blue", markeredgecolor="k")

    marker = 'X'
    # marker = marker.transformed(mt.transforms.Affine2D().rotate_deg(45))   
    # t = Affine2D().rotate_deg(45)

    # hole = marker
    # print(hole.vertices)
    # mark = marker
    # print(mark.vertices)

    cut_mark = get_unfilled_marker(marker)
    fig, ax = plt.subplots()
    fig.suptitle('Path markers', fontsize=14)
    fig.subplots_adjust(left=0.4)

    markers = {'Hole': marker, 'Marker': marker, 'Custom': cut_mark}

    for y, (name, marker) in enumerate(markers.items()):
        ax.text(-0.5, y, name, **text_style)
        ax.plot([y] * 3, marker=marker, **marker_style)
    format_axes(ax)

    plt.show()