
'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-12 14:38:26 
@Last Modified by:   Hitesh Kishore Das 
@Last Modified time: 2022-09-12 14:38:26 
'''

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


if __name__=='__main__':

    import matplotlib.pyplot as plt

    # im  = pil.Image.open('test/solar_prominence2.png')
    # im_path = 'test/cgm.png'
    im_path = 'test/magnetic_fields.png'

    plt.figure()
    plt.imshow(image_arr(im_path))
    plt.axis('off')
    plt.show()

    def fn_im (A):

        # A_return = np.zeros(np.shape(A), dtype=float)

        A_r = A[:,:,0].astype(float)/255
        A_g = A[:,:,1].astype(float)/255
        A_b = A[:,:,2].astype(float)/255

        A_mag = 0.2989*A_r + 0.5870*A_g + 0.1140*A_b 

        # A_r /= 2.0
        # A_g /= 2.0
        # A_b /= 2.0

        # A_return[:,:,0] = A_r
        # A_return[:,:,1] = A_g
        # A_return[:,:,2] = A_b

        A_r = 1.0 - A_r
        A_g = 1.0 - A_g

        A_new = A_r - A_g
        A_new = 1-A_new

        A_new -= A_new.min()
        A_new /= A_new.max()

        A_new[A_mag<0.12] = 1.0

        A_new[A_mag>0.95] = 1.0

        # return A_new/A_new.max()

        # return A_g
        return A_new


    # A_new = image_modify(im_path, fn_im)
    A_new = image_reverse(im_path)

    plt.figure(figsize=(15,15))
    plt.imshow(A_new)
    plt.axis('off')
    # plt.colorbar()
    plt.show()


