import sys
import os

cwd = os.path.dirname(__file__)
for i in range(len(cwd.split("/"))):
    if cwd.split("/")[i] == "own_package":
        break

# Take the path of the package
package_abs_path = "/".join(cwd.split("/")[: i + 1]) + "/own_package/"

sys.path.insert(0, f"{package_abs_path}data_analysis/")

import array_operations as ao


def test_dot_product():

    A = [0, 0, 1]
    B = [0, 1, 0]

    output = ao.dot_product(A, B)

    assert output[0] == 0
    assert output[1] == 0
