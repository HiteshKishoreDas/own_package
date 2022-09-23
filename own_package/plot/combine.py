'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-12 14:38:26 
@Last Modified by:   Hitesh Kishore Das 
@Last Modified time: 2022-09-12 14:38:26 
'''

import os
import sys
import PIL.Image as img
img.MAX_IMAGE_PIXELS = 2000000000

import gc

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 


im_HD_size  = [3000,3000]
im_MHD_size = [3000,3000]
# im_HD_size  = [20000,20000]
# im_MHD_size = [20000,20000]
im_tot_size = [im_HD_size[0]+im_MHD_size[0], im_HD_size[1]]
# im_mpa_size = [1500 ,775]


im_full = img.new('RGBA', tuple(im_tot_size))

im_HD  = img.open('../athena/rho_smooth_HD_gist_rainbow_black_bcg.png')

im_full.paste(im_HD, (0,0))

del im_HD
gc.collect()

im_MHD = img.open('../athena/rho_smooth_MHD_gist_rainbow_black_bcg.png')
im_full.paste(im_MHD, (im_HD_size[0],0))

del im_MHD
gc.collect()

# im_mpa = img.open('../athena/MPA_hoch_E_green.png')
# print(im_mpa.size)

# del im_mpa
# gc.collect()

im_full.save('../athena/rho_full_combined_black_bcg.png')

del(im_full)
gc.collect()


# im_HD.show()