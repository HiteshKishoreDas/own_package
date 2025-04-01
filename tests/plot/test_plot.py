import sys
import os
import numpy as np

cwd = os.path.dirname(__file__)
for i in range(len(cwd.split("/"))):
    if cwd.split("/")[i] == "own_package":
        break

# Take the path of the package
package_abs_path = "/".join(cwd.split("/")[: i + 1]) + "/own_package/"

sys.path.insert(0, f"{package_abs_path}plot/")
import plot_histogram as ph


def test_1d_hist_calc():

    test_arr = np.ones(100)

    hst = ph.calc_histogram_1d(test_arr)

    assert np.sum(hst[0]) == 100
