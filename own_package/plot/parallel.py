'''
Created Date: Thursday, January 1st 1970, 1:00:00 am
Author: Hitesh Kishore Das
'''

import numpy as np
import cmasher as cr
import sys
import os

from multiprocessing import Pool

import matplotlib as mt
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]


def parallelise (fn, iter_list=None, processes=2):
    """
    Function to distribute a repeated function call over multiple processors

    Args:
        fn (function): Function to be run parallely
        iter_list (list, optional): List with elements to iterate over. Defaults to None.
        processes (int, optional): Number of cores to send the jobs. Defaults to 2.
    """

    if iter_list==None:
        iter_list = [i for i in range(processes)]
    
    with Pool(processes) as pool:
        processed = pool.map(fn, iter_list)