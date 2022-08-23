import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import cmasher as cmr

plt.style.use('../plot/plot_style.mplstyle')

# ! CONVERT THIS INTO A MULTI-FIGURE PLOT SCRIPT WITH ALL THE PROPERTIES

for d_create in dir_create_list:
    os.system(f"mkdir Plots/{dir_name}{d_create}")

#* Luminosity
plt.figure(figsize=(10,20))
plt.pcolormesh(ds_lum['x1f'],ds_lum['x3f'],np.average(ds_lum['user_out_var0'], axis=1) , cmap=cmr.sunburst)
plt.title(dir_name)
plt.axis('scaled')
plt.colorbar()
plt.savefig(f"Plots/{dir_name}/luminosity/luminosity_{str(N).zfill(5)}")
plt.close()

T = (ds_prm['press']/ds_prm['rho']) * g.KELVIN * g.mu
# T = np.log10(T)

# print(f"Min pressure: {np.min(ds_prm['press'])}")

#* Temperature
plt.figure(figsize=(10,20))
# plt.pcolormesh(ds_prm['x1f'],ds_prm['x3f'],T[:,32,:], vmin=np.log10(4e4), vmax = np.log10(4e6))
plt.pcolormesh(ds_prm['x1f'],ds_prm['x3f'],np.average(T, axis=1),\
    norm=clr.LogNorm( vmin=4e4, vmax=4e6) , cmap=cmr.bubblegum)
plt.title(dir_name)
plt.axis('scaled')
plt.colorbar()
plt.savefig(f"Plots/{dir_name}/T/T_{str(N).zfill(5)}")
plt.close()

#* Pressure
plt.figure(figsize=(10,20))
plt.pcolormesh(ds_prm['x1f'],ds_prm['x3f'],np.average(ds_prm['press'], axis=1))
plt.title(dir_name)
plt.axis('scaled')
plt.colorbar()
plt.savefig(f"Plots/{dir_name}/prs/prs_{str(N).zfill(5)}")
plt.close()

#* Density
plt.figure(figsize=(10,20))
plt.pcolormesh(ds_prm['x1f'],ds_prm['x3f'],np.average(ds_prm['rho'], axis=1), \
    norm=clr.LogNorm( vmin=ps.amb_rho[0], vmax=ps.chi_cold*ps.amb_rho[0]), cmap=cmr.rainforest_r )
plt.title(dir_name)
plt.axis('scaled')
plt.colorbar()
plt.savefig(f"Plots/{dir_name}/rho/rho_{str(N).zfill(5)}")
plt.close()

if B_fl:

    B_mag = ds_prm['Bcc1']**2 + ds_prm['Bcc2']**2 + ds_prm['Bcc3']**2
    B_mag = np.sqrt(B_mag)

    beta = ds_prm['press']/ (0.5* B_mag**2)

    #* Beta plot
    plt.figure(figsize=(10,20))
    plt.pcolormesh(ds_prm['x1f'],ds_prm['x3f'],beta[:,32,:])
    plt.title(dir_name)
    plt.axis('scaled')
    plt.colorbar()
    plt.savefig(f"Plots/{dir_name}/beta/beta_{str(N).zfill(5)}.png")
    plt.close()

    #* Bcc1
    plt.figure(figsize=(10,20))
    plt.pcolormesh(ds_prm['x1f'],ds_prm['x3f'],ds_prm['Bcc1'][:,32,:])
    plt.title(dir_name)
    plt.axis('scaled')
    plt.colorbar()
    plt.savefig(f"Plots/{dir_name}/Bx/Bx_{str(N).zfill(5)}.png")
    plt.close()

    #* Bcc2
    plt.figure(figsize=(10,20))
    plt.pcolormesh(ds_prm['x1f'],ds_prm['x3f'],ds_prm['Bcc2'][:,32,:])
    plt.title(dir_name)
    plt.axis('scaled')
    plt.colorbar()
    plt.savefig(f"Plots/{dir_name}/By/By_{str(N).zfill(5)}.png")
    plt.close()

    #* Bcc3
    plt.figure(figsize=(10,20))
    plt.pcolormesh(ds_prm['x1f'],ds_prm['x3f'],ds_prm['Bcc3'][:,32,:])
    plt.title(dir_name)
    plt.axis('scaled')
    plt.colorbar()
    plt.savefig(f"Plots/{dir_name}/Bz/Bz_{str(N).zfill(5)}.png")
    plt.close()