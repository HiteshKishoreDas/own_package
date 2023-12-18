import numpy as np
import yt
import sys
import os

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]

sys.path.insert(0, f"{package_abs_path}utils/")
import units as un


def extraction_fn(all_data_level_0_hyd, fields, MHD_flag):
    implemented_field_list = []

    out_dict = {}

    if ("coord" in fields) or ("all" in fields):
        out_dict["coord"] = np.array(all_data_level_0_hyd[("PartType0", "Coordinates")])
    implemented_field_list += ["coord"]

    if (
        ("rho" in fields)
        or ("prs" in fields)
        or ("T" in fields)
        or ("logT" in fields)
        or ("all" in fields)
    ):
        out_dict["rho"] = np.array(all_data_level_0_hyd[("PartType0", "Density")])
    implemented_field_list += ["rho"]

    if (
        ("rho_mf" in fields)
        or ("T_mf" in fields)
        or ("logT_mf" in fields)
        or ("all" in fields)
    ):
        out_dict["rho_mf"] = np.array(all_data_level_0_hyd[("PartType0", "mfDensity")])
    implemented_field_list += ["rho_mf"]

    if ("prs" in fields) or ("T" in fields) or ("logT" in fields) or ("all" in fields):
        out_dict["IE"] = np.array(all_data_level_0_hyd[("PartType0", "InternalEnergy")])
        out_dict["prs"] = out_dict["IE"] * (un.g - 1) * out_dict["rho"]
    implemented_field_list += ["prs"]
    implemented_field_list += ["IE"]

    if (
        ("prs_mf" in fields)
        or ("T_mf" in fields)
        or ("logT_mf" in fields)
        or ("all" in fields)
    ):
        out_dict["IE_mf"] = np.array(
            all_data_level_0_hyd[("PartType0", "mfInternalEnergy")]
        )
        out_dict["prs_mf"] = out_dict["IE_mf"] * (un.g - 1) * out_dict["rho_mf"]
    implemented_field_list += ["prs_mf"]
    implemented_field_list += ["IE_mf"]

    if ("T" in fields) or ("logT" in fields) or ("all" in fields):
        T_arr = (out_dict["prs"] / out_dict["rho"]) * un.KELVIN * un.mu

        if "T" or "all" in fields:
            out_dict["T"] = T_arr
        if "logT" or "all" in fields:
            out_dict["logT"] = np.log10(T_arr)
    implemented_field_list += ["T"]
    implemented_field_list += ["logT"]

    if ("T_mf" in fields) or ("logT_mf" in fields) or ("all" in fields):
        T_arr = (out_dict["prs_mf"] / out_dict["rho_mf"]) * un.KELVIN * un.mu

        if "T_mf" or "all" in fields:
            out_dict["T_mf"] = T_arr
        if "logT_mf" or "all" in fields:
            out_dict["logT_mf"] = np.log10(T_arr)
    implemented_field_list += ["T_mf"]
    implemented_field_list += ["logT_mf"]

    if ("vel" in fields) or ("all" in fields):
        out_dict["vel"] = []

        vel1 = np.array(all_data_level_0_hyd[("PartType0", "velocity_x")])
        vel2 = np.array(all_data_level_0_hyd[("PartType0", "velocity_y")])
        vel3 = np.array(all_data_level_0_hyd[("PartType0", "velocity_z")])

        out_dict["vel"] = [vel1, vel2, vel3]
    implemented_field_list += ["vel"]

    if ("vel_mf" in fields) or ("all" in fields):
        vel1 = np.array(all_data_level_0_hyd[("PartType0", "mf_velocity_x")])
        vel2 = np.array(all_data_level_0_hyd[("PartType0", "mf_velocity_y")])
        vel3 = np.array(all_data_level_0_hyd[("PartType0", "mf_velocity_z")])

        out_dict["vel_mf"] = [vel1, vel2, vel3]
    implemented_field_list += ["vel_mf"]

    if ("alpha" in fields) or ("all" in fields):
        out_dict["alpha"] = np.array(
            all_data_level_0_hyd[("PartType0", "mfVolumeFraction")]
        )
    implemented_field_list += ["alpha"]

    # if MHD_flag and ("B" or "all" in fields):
    #     Bcc1 = np.array(all_data_level_0_hyd["Bcc1"])
    #     Bcc2 = np.array(all_data_level_0_hyd["Bcc2"])
    #     Bcc3 = np.array(all_data_level_0_hyd["Bcc3"])

    #     Bcc = [Bcc1, Bcc2, Bcc3]

    #     out_dict["B"] = Bcc

    # TODO: Add code for unimplemented fields
    # Check if any field in fields is missed
    # Try ("PartType0", field)
    # If that doesn't work, throw error

    return out_dict


def get_array_yt(fn, fields=["rho"], grid_resolution=[32, 32, 32], MHD_flag=False):
    ds = yt.load(fn)

    all_data_level_0_hyd = ds.r[
        :: complex(0, grid_resolution[0]),
        :: complex(0, grid_resolution[1]),
        :: complex(0, grid_resolution[2]),
    ]

    return extraction_fn(all_data_level_0_hyd, fields, MHD_flag)


def get_array_uservar_yt(fn, MHD_flag=False):
    ds = yt.load(fn)

    all_data_level_0_hyd = ds.covering_grid(
        level=0, left_edge=[0, 0.0, 0.0], dims=ds.domain_dimensions
    )

    out_dict = {}

    out_dict["user_out_var"] = np.array(all_data_level_0_hyd["user_out_var"])

    return out_dict


def get_particle_data(fn, fields=["rho"], MHD_flag=False):
    all_data_level_0_hyd = yt.load(fn).all_data()

    return extraction_fn(all_data_level_0_hyd, fields, MHD_flag)
