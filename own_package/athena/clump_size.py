"""
Created Date: 2023-02-06 18:26:22
Author: Hitesh Kishore Das

Code to calculate the clump sizes
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cmr
import sys
import os
import gc
import pickle as pk

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]

sys.path.insert(0, f"{package_abs_path}data_analysis/")
import clump_analysis as ca

sys.path.insert(0, f"{package_abs_path}athena/")
import data_read as dr

sys.path.insert(0, f"{package_abs_path}utils/")
from timer import timer
from units import KELVIN, mu

N_procs_default = 1
file_ind_default = 0
test_array_type_default = None

n_arg = len(sys.argv) - 1
if n_arg == 0:
    print(f"Need atleast one argument. None were provided.")
    print(f"N_procs set to default: {N_procs_default}...")
    print(f"file_int set to default: {file_ind_default}...")
    print(f"test_array_type set to default: {test_array_type_default}...")
    file_ind = file_ind_default
    test_array_type = test_array_type_default
    N_procs = N_procs_default

elif n_arg == 1:
    file_ind = int(sys.argv[1])
    N_procs = N_procs_default
    test_array_type = test_array_type_default
    print(f"Only one argument was provided.")
    print(f"N_procs set to default: {N_procs_default}...")
    print(f"file_int set : {file_ind}...")
    print(f"test_array_type set to default: {test_array_type}...")

elif n_arg == 2:
    file_ind = int(sys.argv[1])
    N_procs = int(sys.argv[2])
    test_array_type = test_array_type_default
    print(f"N_procs set to: {N_procs}...")
    print(f"file_int set : {file_ind}...")
    print(f"test_array_type : {test_array_type}...")

elif n_arg == 3:
    file_ind = int(sys.argv[1])
    N_procs = int(sys.argv[2])
    test_array_type = int(sys.argv[3])
    print(f"N_procs set to: {N_procs}...")
    print(f"file_int set : {file_ind}...")
    print(f"test_array_type : {test_array_type}...")

else:
    print(f"Too many arguments provided...")
    print(f"N_procs set to default: {N_procs_default}...")
    print(f"file_int set to default: {file_ind_default}...")
    print(f"test_array_type set to: {test_array_type_default}...")
    N_procs = N_procs_default
    file_ind = file_ind_default
    test_array_type = test_array_type_default


data_dir = "/ptmp/mpa/hitesh/data/"
save_dir = "./save_arr/clump_size"

sim_list = []

sim_list += ["Rlsh_1000_res_256_M_0.5_hydro/"]
sim_list += ["Rlsh_1000_res_256_M_0.5_beta_100/"]

sim_list += ["Rlsh_250_res_256_M_0.5_hydro/"]
sim_list += ["Rlsh_250_res_256_M_0.5_beta_100/"]

sim_list += ["Rlsh_250_res_256_M_0.25_hydro/"]
sim_list += ["Rlsh_250_res_256_M_0.25_beta_100/"]

N_sim = len(sim_list)
file_loc_list = N_sim * [data_dir]

N_snap = 600
file_name = f"Turb.out2.{str(N_snap).zfill(5)}.athdf"

for i in range(N_sim):
    file_loc_list[i] += sim_list[i] + file_name


MHD_flag = False

out_dict = dr.get_array_athena(file_loc_list[file_ind], fields=["T"], MHD_flag=MHD_flag)

T = out_dict["T"]
T_max = T.max()
T_min = T.min()


if test_array_type == "random":
    save_loc = f"{save_dir}/random_array/"

    np.random.seed(file_ind)
    T = np.random.rand(*np.shape(T))  # Uniform random num between 0 to 1

    T = T_min + (T_max - T_min) * T  # Uniform random num between T_min to T_max

elif test_array_type == "blob":
    save_loc = f"{save_dir}/blob_test/"

    k = 5
    L = np.shape(T)
    r = np.indices(L)
    T = np.sin(2 * np.pi * k * (file_ind + 1) * r[0] / L[0])
    T += np.sin(2 * np.pi * k * (file_ind + 1) * r[1] / L[1])
    T += np.sin(2 * np.pi * k * (file_ind + 1) * r[2] / L[2])
    T -= T.min()
    T /= T.max()  # Blob between 0 to 1

    T = T_min + (T_max - T_min) * T  # Filament between T_min to T_max


elif test_array_type == "filament":
    save_loc = f"{save_dir}/filament_test/"

    k = 5
    L = np.shape(T)
    r = np.indices(L)
    T = np.sin(2 * np.pi * k * (file_ind + 1) * r[0] / L[0])
    T += np.sin(2 * np.pi * k * (file_ind + 1) * r[1] / L[1])
    T += 0.1 * np.sin(2 * np.pi * r[2] / L[2])
    T -= T.min()
    T /= T.max()  # Filament between 0 to 1

    T = T_min + (T_max - T_min) * T  # Filament between T_min to T_max

else:
    save_loc = f"{save_dir}/{sim_list[file_ind]}"
T_floor = 4e4
Tcut = 2 * T_floor
n_blob, label_arr = ca.clump_finder(T, arr_cut=Tcut, above_cut=False)

print(f"clump_size.py:: {n_blob} clumps found .. \n")

save_dict = {}
save_dict["clump_dict"] = []
save_dict["n_blob"] = n_blob
save_dict["label_arr"] = label_arr

for i_clump in range(1, n_blob + 1):
    print(f"clump_size.py:: Analysing clump number {i_clump} ..")
    save_dict["clump_dict"].append(
        ca.clump_length(i_clump, label_arr, skip_data=4, n_jobs=N_procs)
    )


# * Save the input array for test cases, for later analysis
if test_array_type in ["random", "filament", "blob"]:
    save_dict["inp_arr"] = T


if test_array_type == "random":
    with open(f"{save_loc}/clump_network_random_test_rseed_{file_ind}.pkl", "wb") as f:
        pk.dump(save_dict, f)
elif test_array_type == "blob":
    with open(f"{save_loc}/clump_network_blob_test_kmul_{file_ind}.pkl", "wb") as f:
        pk.dump(save_dict, f)
elif test_array_type == "filament":
    with open(f"{save_loc}/clump_network_filament_test_kmul_{file_ind}.pkl", "wb") as f:
        pk.dump(save_dict, f)
else:
    with open(f"{save_loc}/clump_network_Nsnap_{N_snap}.pkl", "wb") as f:
        pk.dump(save_dict, f)


del label_arr
del save_dict
gc.collect()
