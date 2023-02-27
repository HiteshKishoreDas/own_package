"""
@Author: Hitesh Kishore Das 
@Date: 2022-09-12 14:38:26 
@Last Modified by:   Hitesh Kishore Das 
@Last Modified time: 2022-09-12 14:38:26 
"""

import numpy as np
import PIL.Image as pim
import PIL.ImageOps as pio

pim.MAX_IMAGE_PIXELS = 2000000000


def image_arr(im_path):
    return np.array(pim.open(im_path))


def image_reverse(im_path):
    return pio.invert(pim.open(im_path))


def image_modify(im_path, fn):
    return fn(np.array((pim.open(im_path))))


def fn_outflow_modify(A):

    A_r = A[:, :, 0].astype(float) / 255
    A_g = A[:, :, 1].astype(float) / 255
    A_b = A[:, :, 2].astype(float) / 255

    A_mag = 0.2989 * A_r + 0.5870 * A_g + 0.1140 * A_b

    A_r = 1.0 - A_r
    A_g = 1.0 - A_g

    A_new = A_r - A_g
    A_new = 1 - A_new

    A_new -= A_new.min()
    A_new /= A_new.max()

    A_new[A_mag < 0.12] = 1.0
    A_new[A_mag > 0.95] = 1.0

    return A_new


def fn_dark(A):

    A_r = A[:, :, 0].astype(float) / 255
    A_g = A[:, :, 1].astype(float) / 255
    A_b = A[:, :, 2].astype(float) / 255

    A_mag = 0.2989 * A_r + 0.5870 * A_g + 0.1140 * A_b

    A_new = np.copy(A) / 255

    A_new[:, :, 0][A_mag < 0.25] = 1.0
    A_new[:, :, 1][A_mag < 0.25] = 1.0
    A_new[:, :, 2][A_mag < 0.25] = 1.0

    A_new[:, :, 0][A_mag > 0.75] = 0.0
    A_new[:, :, 1][A_mag > 0.75] = 0.0
    A_new[:, :, 2][A_mag > 0.75] = 0.0

    # A_mag[A_mag<0.25] = 1.0
    A_mag[A_mag > 0.75] = 0.0

    return A_new
    # return A_mag


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    # im  = pil.Image.open('test/solar_prominence2.png')
    # im_path = 'test/cgm.png'
    # im_path = 'test/GO_2021.png'
    im_path = "/home/mpaadmin/Downloads/stab3351fig8.jpeg"

    plt.figure()
    plt.imshow(image_arr(im_path))
    plt.axis("off")
    plt.show()

    # A_new = image_modify(im_path, fn_dark)
    A_new = image_reverse(im_path)

    plt.figure(figsize=(25, 25))
    plt.imshow(A_new, cmap="gray")
    plt.axis("off")
    # plt.colorbar()
    # plt.show()
    plt.savefig("test/GO_2021_dark.jpeg")
