import sys
import os 

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')

import array_operations as ao
import clump_analysis   as ca

def test_dot_product ():

    A = [0,0,1]
    B = [0,1,0]

    output = ao.dot_product(A,B)

    assert output[0] == 0
    assert output[1] == 0