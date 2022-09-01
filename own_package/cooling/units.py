from yt import derived_field

CONST_pc  = 3.086e18
CONST_yr  = 3.154e7
CONST_amu = 1.66053886e-24
CONST_kB  = 1.3806505e-16
unit_length = CONST_pc*1e3  # 1 kpc
unit_time   = CONST_yr*1e6  # 1 Myr
unit_density = CONST_amu    # 1 mp/cm-3
unit_velocity = unit_length/unit_time
KELVIN = unit_velocity*unit_velocity*CONST_amu/CONST_kB
unit_q = (unit_density * (unit_velocity**3))/unit_length

g = 5/3
T_floor = 10000.0
T_ceil = 1e8

X = 1.0
Y = 0.0
Z = 0.0

mu = 1.0/(2.*X+ 3.*(1.-X-Z)/4.+ Z/2.)
mue = 2.0/(1.0+X)
muH = 1.0/X
mH = 1.0


@derived_field(name="temp", units="code_length**3*code_pressure/code_mass", \
    sampling_type="cell",force_override=True)
def _temp(field, data):
    return (data["gas", "pressure"] / data["gas", "density"]) * KELVIN * mu