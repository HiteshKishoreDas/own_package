# Import the class
import kmapper as km
import scipy.ndimage as sm
import numpy as np
import clump_analysis as ca
import os
import sys
import matplotlib.pyplot as plt
import networkx as nx
import sklearn

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt


CONST_pc  = 3.086e18
CONST_yr  = 3.154e7
CONST_amu = 1.66053886e-24
CONST_kB  = 1.3806505e-16

unit_length = CONST_pc*1e3  # 1 kpc
unit_time   = CONST_yr*1e6  # 1 Myr
unit_density = CONST_amu    # 1 mp/cm-3
unit_velocity = unit_length/unit_time

KELVIN = unit_velocity*unit_velocity*CONST_amu/CONST_kB

Xsol = 1.0
Zsol = 1.0

X = Xsol * 0.7381
Z = Zsol * 0.0134
Y = 1 - X - Z

mu  = 1.0/(2.*X+ 3.*(1.-X-Z)/4.+ Z/2.);
mue = 2.0/(1.0+X);
muH = 1.0/X;

mH = 1.0

rho = np.load('data/rho.npy')
prs = np.load('data/prs.npy')
T = (prs/rho) * KELVIN * mu
cut = 5e4

n_blob_sp, label_arr_sp = ca.clump_finder(T, cut, above_cut=False)

clump_num = 8 

def alpha_plot(c_arr, log_flag=False):
    return pt.poly_alpha(c_arr,log_flag=log_flag, order=1, cut=0)#,cut=np.sqrt(frac_aniso.min()*frac_aniso.max()))


fig, ax, sc  = pt.render_scatter_3d(inp_arr = ca.clump_select(clump_num, label_arr_sp), \
                         alpha_fn = alpha_plot,\
                         cmap="Paired")
plt.show()

label_clump = ca.clump_select(clump_num, label_arr_sp)
data = ((ca.clump_flatten(label_clump).astype(float)).T)#/54.0

adj_mat = np.zeros((len(data),len(data)), dtype=float)


import time

# TODO:Convert to numpy array operation

# for i in range(len(data)):
#     for j in range(i+1, len(data)):
#         if np.sum((data[i]-data[j])**2)<=dist_cut**2:

#             adj_mat[i,j] = 1
#             adj_mat[j,i] = 1

# for i in range(len(data)):
#     r_i_sq = np.sum((data - data[i])**2, axis=1)
#     adj_mat[i,:] = (r_i_sq<=(dist_cut**2)).astype(int)
#     adj_mat[i,i] = 0

a = time.time()

skip_data = 1

x_arr = data[::skip_data, 0]/skip_data
y_arr = data[::skip_data, 1]/skip_data
z_arr = data[::skip_data, 2]/skip_data

dist_cut = 1.5 # np.sqrt(4.0)*1.1

dx1_arr = sklearn.metrics.pairwise_distances(x_arr.reshape(-1,1), n_jobs=2)
dy1_arr = sklearn.metrics.pairwise_distances(y_arr.reshape(-1,1), n_jobs=2)
dz1_arr = sklearn.metrics.pairwise_distances(z_arr.reshape(-1,1), n_jobs=2)

dx2_arr = (np.abs(sklearn.metrics.pairwise_distances(x_arr.reshape(-1,1), n_jobs=2))<=1).astype(int)
dy2_arr = (np.abs(sklearn.metrics.pairwise_distances(y_arr.reshape(-1,1), n_jobs=2))<=1).astype(int)
dz2_arr = (np.abs(sklearn.metrics.pairwise_distances(z_arr.reshape(-1,1), n_jobs=2))<=1).astype(int)

adj_mat1 = ((dx1_arr**2 + dy1_arr**2 + dz1_arr**2)<=(dist_cut**2)).astype(int)
np.fill_diagonal(adj_mat1, 0)
# adj_mat = np.logical_or(np.logical_or(dx_arr, dy_arr), dz_arr)
adj_mat2 = dx2_arr & dy2_arr & dz2_arr
np.fill_diagonal(adj_mat2, 0)

b = time.time()

print(f"Calculating adjucency matrix: {b-a} s")

plt.figure()
plt.imshow(adj_mat1)
plt.title('adj_mat1')
plt.show()

plt.figure()
plt.imshow(adj_mat2)
plt.title('adj_mat2')
plt.show()

a = time.time()

graph_nx = nx.from_numpy_array(adj_mat2)

b = time.time()

print(f"Creating graph: {b-a} s")


# a = time.time()
# plt.figure()
# plt.imshow(adj_mat)
# plt.show()
# b = time.time()
# print(f"{b-a} ms")

# mapper = km.KeplerMapper(verbose=1)

# lens = mapper.fit_transform(data)

# # lens = mapper.project( data, distance_matrix="euclidean")

# # Project by first two PCA components
# lens = mapper.project( data, projection=sklearn.decomposition.PCA() )

# # lens = mapper.project( data, projection="sum" )

# graph_dict = mapper.map(
#     lens,
#     data,
#     clusterer=sklearn.cluster.DBSCAN(eps=0.1, min_samples=1),
#     cover=km.Cover(n_cubes=10, perc_overlap=0.6),
#     remove_duplicate_nodes=True,
# )

# mapper.visualize(graph_dict, path_html="output/cat.html")

# km.draw_matplotlib(graph_dict)
# plt.show()

# graph_nx = km.adapter.to_networkx(graph_dict)

a = time.time()
path_length = dict(nx.all_pairs_shortest_path_length(graph_nx))
b = time.time()
print(f"Calculating path lengths: {b-a} s")

a = time.time()
max_path_length = 0
for k1 in path_length.keys():
    for k2 in path_length[k1].keys():
        if path_length[k1][k2]>max_path_length:
            max_path_length = path_length[k1][k2]

b = time.time()
print(f"Finding longest length: {b-a} s")
print(f"Longest path: {max_path_length}")
print(f"Longest path after skip correction: {max_path_length*skip_data}")
