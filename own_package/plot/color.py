"""
Created Date: 2022-10-26 14:49:55 
Author: Hitesh Kishore Das
"""

import numpy as np

# import cmasher as cr
import colorsys

import matplotlib as mt
import matplotlib.pyplot as plt
import matplotlib.colors as mc


def create_color(col_list, cmap="plasma", log=False):
    if log:
        cb_qnt = np.log10(np.array(col_list))
    else:
        cb_qnt = np.array(col_list)

    cmap_fn = mt.cm.get_cmap(cmap)
    line_col = cmap_fn((cb_qnt - cb_qnt.min()) / (cb_qnt.max() - cb_qnt.min()))

    return line_col


def adjust_lightness(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        if "C" in color:
            c = list(mt.rcParams["axes.prop_cycle"])[int(color[1:])]["color"]
        else:
            c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    c = colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

    return mc.to_hex(c)
