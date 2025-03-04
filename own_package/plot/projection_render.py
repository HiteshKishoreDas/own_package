import numpy as np


# TODO: Add ray-casting (pin-hole camera) to this
def project_on_plane(points, camera_view):
    """
    Projects a set of 3D points onto a plane defined by a camera view.

    Parameters:
    points (array-like): An array of shape (n, n, n, 3) representing the 3D points to be projected.
    camera_view (array-like): A tuple or list containing two angles (theta, phi) that define the camera view.

    Returns:
    numpy.ndarray: An array of shape (n, n, n, 2) representing the 2D coordinates of the projected points on the plane.
    """
    # * Ensure points and plane_normal are numpy arrays
    camera_view = np.asarray(camera_view).astype(float)

    points = np.asarray(points).astype(float)

    theta, phi = camera_view

    plane_normal = np.array(
        [
            np.sin(phi),
            np.cos(phi) * np.sin(theta),
            np.cos(phi) * np.cos(theta),
        ]
    )

    # * Ensure plane_normal is a unit vector
    plane_normal /= np.linalg.norm(plane_normal)

    # * Calculate the projection matrix
    projection_matrix = np.eye(3) - np.outer(plane_normal, plane_normal)

    # * Project each point onto the plane
    projected_points = np.matmul(projection_matrix, points.T).T

    # * Create an orthonormal basis for the plane
    # * Choose an arbitrary vector perpendicular to the plane normal
    # * Let plane normal be [a,b,c], and the perp. one be [x, y, z]
    # * Then perpendicular vector follows: a*x + b*y + c*z = 0
    # *  Take x=1, y=1, => a + b + cz = 0 => z = -a/c
    v1 = np.array(
        [
            -np.cos(phi),
            np.sin(phi) * np.sin(theta),
            np.sin(phi) * np.cos(theta),
        ]
    )
    v1 /= np.linalg.norm(v1)

    # * Calculate the second basis vector by taking the cross product
    v2 = np.cross(plane_normal, v1)
    v2 /= np.linalg.norm(v2)

    # * Calculate the third basis vector by taking the cross product of the first two
    v3 = np.cross(v1, v2)

    # * Convert the projected points to the plane coordinate system
    # * plane_coordinates = np.matmul(np.vstack((v1, v2, v3)), projected_points.T).T

    # * Convert the projected points to the plane coordinate system
    plane_coordinates = np.empty((projected_points.shape[0], 2))
    for i in range(projected_points.shape[0]):
        plane_coordinates[i] = np.array(
            [np.dot(v1, projected_points[i]), np.dot(v2, projected_points[i])]
        )

    return plane_coordinates


def project_along_normal(arr, points, camera_view, assign_type="nearest", alpha=None):
    """
    Projects the given points onto a plane and assigns values from the array `arr` to the projected points.

    Parameters:
    arr (numpy.ndarray): The array containing values to be projected.
    points (numpy.ndarray): The points to be projected onto the plane.
    camera_view (numpy.ndarray): The camera view matrix used for projection.
    assign_type (str, optional): The type of assignment to use for the projection.
                                 Options are "nearest" (default) and "CIC" (Cloud-In-Cell).
    alpha (numpy.ndarray, optional): An optional alpha array to scale the values in `arr`.

    Returns:
    numpy.ndarray: A 2D array representing the projected values.
    """
    # * Project the points onto the plane
    projected_points = project_on_plane(points, camera_view)

    # * Calculate the origin of the projected points
    origin = np.min(projected_points, axis=0)

    # * Shift the projected points to start from the origin
    projected_points -= origin
    projected_index = projected_points.astype(int)

    # * Calculate the actual size of the projected array
    proj_size_actual = np.max(projected_index, axis=0) + 1
    proj_size = int(np.sqrt(3) * np.max(np.shape(arr)))

    # * Center the projected points in the array
    projected_index += ((proj_size - proj_size_actual) / 2).astype(int)
    projected_points += ((proj_size - proj_size_actual) / 2).astype(int).astype(float)

    # * Initialize the projected array
    arr_proj = np.zeros((proj_size, proj_size), dtype=float)

    # * Determine the array to plot
    if alpha is None:
        plot_arr = arr
    else:
        plot_arr = arr * alpha

    # * Assign values to the projected array based on the assignment type
    if assign_type == "CIC":
        for i in range(np.shape(projected_index)[0]):
            a = np.abs(np.round(projected_points[i, :]) - projected_points[i, :])
            a_sign = np.sign(
                np.round(projected_points[i, :]) - projected_points[i, :]
            ).astype(int)

            arr_proj[tuple(projected_index[i, :])] += (
                (a[0] + 0.5) * (a[1] + 0.5) * plot_arr[tuple(points[i, :])]
            )
            arr_proj[
                tuple([projected_index[i, 0] - a_sign[0], projected_index[i, 1]])
            ] += ((0.5 - a[0]) * (a[1] + 0.5) * plot_arr[tuple(points[i, :])])
            arr_proj[
                tuple([projected_index[i, 0], projected_index[i, 1] - a_sign[1]])
            ] += ((a[0] + 0.5) * (0.5 - a[1]) * plot_arr[tuple(points[i, :])])
            arr_proj[tuple(projected_index[i, :] - a_sign)] += (
                (0.5 - a[0]) * (0.5 - a[1]) * plot_arr[tuple(points[i, :])]
            )
    elif assign_type == "nearest":
        for i in range(np.shape(projected_index)[0]):
            arr_proj[tuple(projected_index[i, :])] += plot_arr[tuple(points[i, :])]

    return arr_proj


# TODO: Add some test here, maybe
if __name__ == "__main__":
    print("Check out render_example.py for an example script!")
