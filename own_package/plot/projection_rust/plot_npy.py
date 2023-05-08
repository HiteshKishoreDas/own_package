# %%
import numpy as np
import matplotlib.pyplot as plt

rho_full = np.load("array.npy")

print(np.shape(rho_full))

plt.figure()
plt.imshow(np.log10(rho_full[:, :, 128]))
plt.colorbar()

# plt.savefig("Test_rust.png")

# %%


def project(points, plane_normal):
    # Ensure points and plane_normal are numpy arrays
    points = np.asarray(points).astype(float)
    plane_normal = np.asarray(plane_normal).astype(float)

    # Ensure plane_normal is a unit vector
    plane_normal /= np.linalg.norm(plane_normal)

    # Calculate the projection matrix
    projection_matrix = np.eye(3) - np.outer(plane_normal, plane_normal)

    # Project each point onto the plane
    projected_points = np.matmul(projection_matrix, points.T).T

    # Create an orthonormal basis for the plane
    # Choose an arbitrary vector perpendicular to the plane normal
    v1 = np.array([1, 0, 0])
    if np.abs(np.dot(v1, plane_normal)) > 0.9:
        v1 = np.array([0, 1, 0])
    # Calculate the second basis vector by taking the cross product
    v2 = np.cross(plane_normal, v1)
    # Normalize the second basis vector
    v2 /= np.linalg.norm(v2)
    # Calculate the third basis vector by taking the cross product of the first two
    v3 = np.cross(v1, v2)

    # # Convert the projected points to the plane coordinate system
    # plane_coordinates = np.matmul(np.vstack((v1, v2, v3)), projected_points.T).T

    # Convert the projected points to the plane coordinate system
    plane_coordinates = np.empty((projected_points.shape[0], 2))
    for i in range(projected_points.shape[0]):
        plane_coordinates[i] = np.array(
            [np.dot(v1, projected_points[i]), np.dot(v2, projected_points[i])]
        )

    return plane_coordinates


# Define some 3D points
grid_shape = np.shape(rho_full)
grid = np.mgrid[0 : grid_shape[0], 0 : grid_shape[1], 0 : grid_shape[2]]

# points =  np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
points = np.vstack(
    (
        grid[0].ravel(),
        grid[1].ravel(),
        grid[2].ravel(),
    )
).T

# Define the normal vector for the plane (in this case, the z-axis)
plane_normal = np.array([0, 0, 1])

# Project the points onto the plane
projected_points = project(points, plane_normal)

# Print the projected points
print(projected_points)


# %%
