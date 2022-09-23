import lamfn as lf

CONST_amu = 1.66053886e-24
UNIT_DENSITY = 1.66053886e-24
UNIT_VELOCITY = 1.e8
UNIT_LENGTH = 3.0856775807e18  * 1.e5
unit_q = UNIT_DENSITY*(UNIT_VELOCITY**3)
unit_q = unit_q / UNIT_LENGTH

CONST_kB = 1.3806505e-16
KELVIN = UNIT_VELOCITY*UNIT_VELOCITY*CONST_amu/CONST_kB

ul = 100 # in kpc
uv = 1.0E+8 # in cm/s
ut = ((ul * 3.086E+21)/uv)  # in s
ut = (ut / 3.154e+13)    # in Myr

uv = 1.022  # in kpc/Myr

# ut = 100 # in Myr
# t = 2.0 * ut  # in Myr
# dt = 1.0 # in Myr

gamma = 5./3.


Zsol = 0.6
Xsol = 1.01

mu = lf.MMWt_mu(Zsol, Xsol)