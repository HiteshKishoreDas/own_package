# %%

import numpy as np
import matplotlib.pyplot as plt
import h5py

import skspatial.objects as so

# %%
filename = (
    "/home/mpaadmin/files/data/Rlsh_1000_res_256_M_0.5_hydro/Turb.out2.00650.athdf"
    # "/home/mpaadmin/files/data/Rlsh_1000_res_256_M_0.5_beta_100/Turb.out2.00650.athdf"
)

with h5py.File(filename, "r") as f:
    print(f"Keys: {f.keys()} \n")
    print(f"Attributes: {f.attrs.keys()} \n")

    prim = f["prim"][()]

    rho = prim[0]
    prs = prim[1]
    vel1 = prim[2]
    vel2 = prim[3]
    vel3 = prim[4]

    x1 = f["x1v"][()]
    x2 = f["x2v"][()]
    x3 = f["x3v"][()]

    LogicalLocations = f["LogicalLocations"][()]

    print(f"{np.shape(LogicalLocations) = }")
    print(f"{np.shape(rho) = }")
    print(f"{np.shape(x1) = }")
    print(f"{np.shape(x2) = }")
    print(f"{np.shape(x3) = }\n")

    MeshBlockSize = f.attrs["MeshBlockSize"]
    print(f"{MeshBlockSize = }")

    RootGridSize = f.attrs["RootGridSize"]
    print(f"{RootGridSize = }")

    NumMeshBlocks = f.attrs["NumMeshBlocks"]
    print(f"{NumMeshBlocks = }")

# %%

rho_0 = rho[10]
x1_0 = x1[10]

print(f"{np.shape(rho_0) = }")
print(f"{np.shape(x1_0) = }")
print(f"{LogicalLocations[10] = }")

rho_full = np.zeros(tuple(RootGridSize), dtype=float)
prs_full = np.zeros(tuple(RootGridSize), dtype=float)

x1_full = np.zeros(np.product(np.shape(x1)), dtype=float)
x2_full = np.zeros(np.product(np.shape(x2)), dtype=float)
x3_full = np.zeros(np.product(np.shape(x3)), dtype=float)

for i in range(NumMeshBlocks):
    start1 = MeshBlockSize[0] * LogicalLocations[i][0]
    end1 = start1 + MeshBlockSize[0]

    start2 = MeshBlockSize[1] * LogicalLocations[i][1]
    end2 = start2 + MeshBlockSize[1]

    start3 = MeshBlockSize[2] * LogicalLocations[i][2]
    end3 = start3 + MeshBlockSize[2]

    rho_full[start3:end3, start2:end2, start1:end1] = rho[i]
    prs_full[start3:end3, start2:end2, start1:end1] = prs[i]

    x1_full[start1:end1] = x1[i]
    x2_full[start2:end2] = x2[i]
    x3_full[start3:end3] = x3[i]

T = prs_full / rho_full

# %%

plt.figure()
# plt.imshow(np.sum(np.log10(T), axis=0))
plt.imshow(np.log10(rho_full)[:, :, 128])
plt.colorbar()
plt.savefig("Test_python.png")

# %%
