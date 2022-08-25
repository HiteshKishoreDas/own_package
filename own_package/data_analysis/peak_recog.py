#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created Date: Monday, June 14th 2021, 2:49:26 am
Author: Hitesh
'''

import numpy as np
from matplotlib import pyplot as plt


def peak_recog_arr (clump_arr,inp_arr):

    peak_arr = np.zeros_like(clump_arr)

    peak_arr += np.less_equal (clump_arr, np.roll(clump_arr,1,0))

    # plt.figure(figsize=(5,5))
    # plt.imshow(peak_arr)

    peak_arr += np.less_equal (clump_arr, np.roll(clump_arr,-1,0))
    
    # plt.figure(figsize=(5,5))
    # plt.imshow(peak_arr)
    
    peak_arr += np.less_equal (clump_arr, np.roll(clump_arr,1,1))

    # plt.figure(figsize=(5,5))
    # plt.imshow(peak_arr)
    
    peak_arr += np.less_equal (clump_arr, np.roll(clump_arr,-1,1))

    # plt.figure(figsize=(5,5))
    # plt.imshow(peak_arr)
    

    peak_arr += np.less_equal (clump_arr, np.roll(np.roll(clump_arr,1,0),1,1) )
    peak_arr += np.less_equal (clump_arr, np.roll(np.roll(clump_arr,-1,0),-1,1) )
    peak_arr += np.less_equal (clump_arr, np.roll(np.roll(clump_arr,1,0),-1,1) )
    peak_arr += np.less_equal (clump_arr, np.roll(np.roll(clump_arr,-1,0),1,1) )

    # peak_arr = np.logical_and(np.logical_not(peak_arr),inp_arr)

    peak_arr = np.logical_not(peak_arr)

    return peak_arr



def peak_recog_seq (clump_arr,inp_arr):

    N,M = np.shape(clump_arr)

    peak_arr = np.zeros_like(clump_arr)

    for i in range(1,N-1):
        for j in range(1,M-1):

            if (inp_arr[i,j]):

                if (np.max(clump_arr[i-1:i+2,j-1:j+2]) == clump_arr[i,j]):

                    if np.sum(peak_arr[i-1:i+2,j-1:j+2]) == 0:

                        peak_arr[i,j] = 1.0
                        # i_list.append(i)
                        # j_list.append(j)

    return peak_arr

        
