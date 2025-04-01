import sys
import os

cwd = os.path.dirname(__file__)
for i in range(len(cwd.split("/"))):
    if cwd.split("/")[i] == "own_package":
        break

# Take the path of the package
package_abs_path = "/".join(cwd.split("/")[: i + 1]) + "/own_package/"

sys.path.insert(0, f"{package_abs_path}pluto/")


def test_true():
    assert True == True
