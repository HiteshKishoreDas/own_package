import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import gc

import yt
from yt.units import Mpc
from yt.visualization.api import Streamlines


def array_to_ds(arr_list, field_list, bbox=None):
    """
    Converts a list of array and corresponding
    list of fields into yt dataset

    Args:
        arr_list (list): List of data arrays
        field_list (list): List of field names for the data arrays
        bbox ((3x2) numpy array, optional): Box limits, set (-0.5, 0.5) if None. Defaults to None.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if len(arr_list) != len(field_list):
        raise ValueError(
            "streamlines.py::array_to_ds(): arr_list and field_list do not have the same size..."
        )

    data = {field_list[i]: arr_list[i] for i in range(len(field_list))}

    if bbox is None:
        bbox = np.array([[-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5]])

    ds = yt.load_uniform_grid(data, arr_list[0].shape, 3.08e21, bbox=bbox)

    return ds


def streamline_length(
    ds,
    fields=[("Bcc1"), ("Bcc2"), ("Bcc3")],
    N_streams=100,
    streamline_ratio=0.25,
    parallel_flag=False,
    periodic=False,
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
        print("yt parallelism enabled...")

    # print(f"{ds[('athena_pp',fields[0])].size}")

    # # Load the dataset
    # ds = yt.load(file_name)
    # # ds.force_periodicity()

    # Define c: the center of the box, N: the number of streamlines,
    # scale: the spatial scale of the streamlines relative to the boxsize,
    # and then pos: the random positions of the streamlines.
    c = ds.domain_center

    if periodic:
        scale = ds.domain_width[0] / 3
        streamline_ratio /= 3
    else:
        scale = ds.domain_width[0]

    pos_dx = np.random.random((N_streams, 3)) * scale - scale / 2.0
    pos = c + pos_dx

    # Create streamlines of the 3D vector velocity and integrate them through
    # the box defined above

    stream_length = float(
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

    count = 0

    for stream in streamlines.streamlines:
        stream = stream[np.all(stream != 0.0, axis=1)]

        # Choose for streamlines that do not cross the boundaries
        if np.shape(stream)[0] in [streamlength_i, streamlength_i + 1]:
            stream_return.append(np.array(stream))

            ax.plot3D(stream[:, 0], stream[:, 1], stream[:, 2], alpha=0.5)

            count += 1

    plt.show()

    print(f"{count = }")

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


if __name__ == "__main__":
    import sys
    import os

    cwd = os.path.dirname(__file__)
    package_abs_path = cwd[: -len(cwd.split("/")[-1])]

    sys.path.insert(0, f"{package_abs_path}data_analysis/")
    import array_operations as ao

    v1 = np.load("data/v1.npy")
    v2 = np.load("data/v2.npy")
    v3 = np.load("data/v3.npy")

    print(f"{np.shape(v1) = }")

    plt.figure()
    plt.imshow(v1[:, :, 10])
    plt.title("Non-periodic")
    plt.show()

    v1 = ao.make_array_periodic(v1)
    v2 = ao.make_array_periodic(v2)
    v3 = ao.make_array_periodic(v3)

    plt.figure()
    plt.imshow(v1[:, :, 10])
    plt.title("Periodic")
    plt.show()

    print(f"{np.shape(v1) = }")

    ds = array_to_ds([v1, v2, v3], ["v1", "v2", "v3"])

    streamline_length(
        ds,
        fields=[("v1"), ("v2"), ("v3")],
        N_streams=100,
        streamline_ratio=1.0,
    )

    streamline_length(
        ds,
        fields=[("v1"), ("v2"), ("v3")],
        N_streams=100,
        streamline_ratio=1.0,
        periodic=True,
    )
