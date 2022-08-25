#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created Date: Wednesday, June 2nd 2021, 10:53:52 pm
Author: Hitesh
'''

#%%

from peak_recog import peak_recog_arr, peak_recog_seq
import numpy as np
import matplotlib
# matplotlib.use('Agg')   # Solution for memory leak in savefig
from matplotlib import pyplot as plt

import pyPLUTO
import pyPLUTO.pload as pp

import workdir_2 as wdir
# import workdir_2_dept as wdir
# import workdir_2_drish as wdir

import plot_fn as pf
import lamfn as lf
import curl as cl
import clump_reduce as cr
import peak_recog as pr

import time as tm

CONST_amu = 1.66053886e-24
UNIT_DENSITY = 1.66053886e-24
UNIT_VELOCITY = 1.e8
UNIT_LENGTH = 3.0856775807e18  * 1.e5
CONST_kB = 1.3806505e-16
KELVIN = UNIT_VELOCITY*UNIT_VELOCITY*CONST_amu/CONST_kB

ul = 100 # in kpc
uv = 1.0E+8 # in cm/s
ut = ((ul * 3.086E+21)/uv)  # in s
ut = (ut / 3.154e+13)    # in Myr

uv = 1.022  # in kpc/Myr

dt = 5.0*1e-2*ut  # in Myr ############################

rho_cut = 20

wdir_f = wdir.wdir22

start_glob = tm.time()

D = pp.pload(15, w_dir=wdir_f+'output/')

print("Date read complete....")

# [750:850,950:1050]  [700:1350,700:1350]

start_inp = tm.time()

inp_arr = pf.arr_arrange(np.array(np.copy((D.rho>rho_cut)*D.rho)).astype(float))

end_inp = tm.time()

print("Input array created: Time taken - ", end_inp-start_inp," s")

# plt.figure(figsize=(10,10))
# plt.imshow(inp_arr)
# plt.axis('off')

#%%

start_shrink = tm.time()

buffer = 100

# inp_arr = cr.array_reduce_seq(inp_arr,buffer)

inp_arr = cr.array_reduce_bin(inp_arr,buffer)

# plt.figure(figsize=(10,10))
# plt.imshow(inp_arr)
# plt.axis('off')

end_shrink = tm.time()

print("Time to shrink the array: ",end_shrink-start_shrink,' s')


# i1 = 125
# i2 = 150
# j1 = 300
# j2 = 325

# inp_arr = inp_arr[i1:i2,j1:j2]

#%%

start_loop = tm.time()

N,M = np.shape(inp_arr)

iter = 50
expon = 2

clump_arr = np.copy(inp_arr**expon)

for n in range(iter):

    start_inloop = tm.time()

    sum_arr = np.zeros_like(clump_arr)

    clump2 = np.copy(clump_arr)

    for i in range(1,N-1):
        for j in range(1,M-1):
        
            if (inp_arr[i,j]):
                clump2[i,j] = np.sum(clump_arr[i-1:i+2,j-1:j+2])

    clump_arr = np.copy(clump2-clump_arr)

    del(clump2)

    # sum_arr += 2*clump_arr
    # sum_arr += (np.roll(clump_arr,1,0) + np.roll(clump_arr,-1,0) )
    # sum_arr += (np.roll(clump_arr,1,1) + np.roll(clump_arr,-1,1) )
    # sum_arr += (np.roll(np.roll(clump_arr,1,0),1,1) )
    # sum_arr += (np.roll(np.roll(clump_arr,-1,0),-1,1) )
    # sum_arr += (np.roll(np.roll(clump_arr,1,0),-1,1) )
    # sum_arr += (np.roll(np.roll(clump_arr,-1,0),1,1) )

    # clump_arr = np.copy((sum_arr)*inp_arr.astype(bool))

    end_inloop = tm.time()


    print(str(n+1)+'th iteration: Time taken - ',end_inloop-start_inloop,' s')

end_loop = tm.time()

start_peak = tm.time()

print("Total loop time: ", end_loop-start_loop, ' s')

# plt.figure(figsize=(10,10))
# plt.imshow(clump_arr)
# plt.colorbar()
# plt.axis('off')
# plt.show()
# plt.close()



i1_list = []
j1_list = []
i2_list = []
j2_list = []

i3_list = []
j3_list = []

peak_arr = pr.peak_recog_arr(clump_arr,inp_arr)

peak_seq = pr.peak_recog_seq(clump_arr,inp_arr)

# plt.figure(figsize=(10,10))
# plt.imshow((peak_arr-peak_seq)[200:500,200:500])

peak_diff = peak_seq-peak_arr

for i in range(1,N-1):
    for j in range(1,M-1):

        if peak_arr[i,j] == 1:

            i1_list.append(i)
            j1_list.append(j)

        if peak_seq[i,j] == 1:

            i2_list.append(i)
            j2_list.append(j)

        if peak_diff[i,j] != 0:

            i3_list.append(i)
            j3_list.append(j)


# plt.figure()
# plt.imshow(peak_seq)

end_peak = tm.time()



print("Peak recognition time: ",end_peak-start_peak, ' s')
print("Number of peaks before cleaning: ",np.sum(peak_arr))

# plt.figure(figsize=(10,10))
# plt.imshow(peak_arr)
# # plt.colorbar()
# plt.axis('off')
# plt.show()
# plt.close()

print("Number of clumps: ",np.sum(peak_arr))
print("Number of clumps: ",np.sum(peak_seq))

end_glob = tm.time()

print("Total time taken: ",end_glob-start_glob, ' s')

# plt.figure(figsize=(10,10))
# plt.imshow(inp_arr)
# plt.axis('off')
# # plt.savefig("clump_count/density_dist_"+ str(np.round(end_glob-start_glob,2)) +"s.png")

i1 = 0
i2 = -1
j1 = 0
j2 = -1

# i1 = 125
# i2 = 150
# j1 = 300
# j2 = 325

plt.figure(figsize=(10,10))
plt.axis('off')
# plt.scatter(np.array(j_list)-200,np.array(i_list),marker='X',s=50,color='k')
plt.imshow(inp_arr[i1:i2,j1:j2])
# # plt.savefig("clump_count/clump_posn_"+ str(np.round(end_glob-start_glob,2)) +"s.png")

plt.figure(figsize=(10,10))
plt.axis('off')
# plt.scatter(np.array(j1_list)-j1,np.array(i1_list)-i1,marker='X',s=50,color='yellow')
plt.scatter(np.array(j2_list)-j1,np.array(i2_list)-i1,marker='o',s=50,color='tab:orange')
plt.imshow(inp_arr[i1:i2,j1:j2])

plt.figure(figsize=(10,10))
plt.axis('off')
plt.scatter(np.array(j3_list)-j1,np.array(i3_list)-i1,marker='X',s=50,color='k')
plt.imshow(inp_arr[i1:i2,j1:j2])

plt.figure(figsize=(10,10))
plt.axis('off')
plt.imshow(np.log10(clump_arr[i1:i2,j1:j2]))
# %%
