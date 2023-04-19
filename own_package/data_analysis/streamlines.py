import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import gc

import yt
from yt.units import Mpc
from yt.visualization.api import Streamlines


def streamline_length(
    file_name,
    fields=[("Bcc1"), ("Bcc2"), ("Bcc3")],
    N_streams=100,
    streamline_ratio=0.25,
    parallel_flag = False,
):
    """_summary_

    Args:
        file_name (str): filename of the data file
        streamline_ratio (float, optional): Streamline length to box size ratio.
                        Use a value<1 for better results. Defaults to 0.25.

    Returns:
        _type_: _description_
    """

    if parallel_flag:
        yt.enable_parallelism()

    # Load the dataset
    ds = yt.load(file_name)
    ds.force_periodicity()

    # Define c: the center of the box, N: the number of streamlines,
    # scale: the spatial scale of the streamlines relative to the boxsize,
    # and then pos: the random positions of the streamlines.
    c = ds.domain_center
    scale = ds.domain_width[0]
    pos_dx = np.random.random((N_streams, 3)) * scale - scale / 2.0
    pos = c + pos_dx

    # Create streamlines of the 3D vector velocity and integrate them through
    # the box defined above

    stream_length = (
        np.max(ds.domain_right_edge - ds.domain_left_edge) * streamline_ratio
    )
    print(f"{stream_length = }")

    streamlines = Streamlines(
        ds,
        pos,
        fields[0],
        fields[1],
        fields[2],
        length=stream_length,
        get_magnitude=True,
    )
    streamlines.integrate_through_volume()

    # Create a 3D plot, trace the streamlines through the 3D volume of the plot
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)

    stream_return = []

    streamlength_i = int(ds.domain_dimensions[0] * streamline_ratio)

    for stream in streamlines.streamlines:
        stream = stream[np.all(stream != 0.0, axis=1)]

        # Choose for streamlines that do not cross the boundaries
        if np.shape(stream)[0] in [streamlength_i, streamlength_i + 1]:
            stream_return.append(stream)

            ax.plot3D(stream[:, 0], stream[:, 1], stream[:, 2], alpha=0.5)

    plt.show()

    del streamlines
    plt.cla()
    plt.clf()
    plt.close()
    del fig, ax

    gc.collect()

    return_dict = {}
    return_dict["streams"] = stream_return
    return_dict["streamline_length"] = stream_length
    return_dict["streamline_length_i"] = streamlength_i

    return return_dict
