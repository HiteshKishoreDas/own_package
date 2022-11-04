'''
Created Date: 2022-10-26 14:49:55 
Author: Hitesh Kishore Das
'''

import numpy as np
import cmasher as cr
import sys
import os

import matplotlib as mt
import matplotlib.pyplot as plt



def create_color(col_list, cmap='plasma', log_flag=False):

    if log_flag:
        cb_qnt = np.log10(np.array(col_list))
    else:
        cb_qnt = np.array(col_list)

    cmap_fn = mt.cm.get_cmap(cmap)
    line_col = cmap_fn((cb_qnt-cb_qnt.min())/(cb_qnt.max()-cb_qnt.min()))

    return line_col
