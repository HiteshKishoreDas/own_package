"""
 # @ Author: Hitesh Kishore Das
 # @ Created: 2023-02-23 22:13:59
 # @ Description: Stolen from Max :). Velocity related analysis stuff.
 """

from . import helpers as h

import numpy as np
import os
import logging
import gc
from scipy.spatial.distance import pdist, cdist

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# def _get_pdist(k, ipick=None):
#     if ipick is None:
#         return pdist(k)
#     else:
#         return pdist(k[ipick])


# def _get_cdist(m, n, ipick=None, jpick=None):
#     if ipick is None:
#         return cdist(m, n)
#     else:
#         return pdist(m[ipick], n[jpick])


def _get_pdist_pbc(k, Lbox=None, ipick=None):
    """pdist with periodic bounday conditions.
    Uses still scipy pdist to be fast.

    L_box is float
    """
    if ipick is not None:
        return _get_pdist_pbc(k[ipick], Lbox)

    if Lbox is None:
        dist_1d = pdist(k)  # shape (N * (N - 1) // 2, )
        return dist_1d

    else:
        N, dim = k.shape
        dist_nd_sq = np.zeros(N * (N - 1) // 2)  # to match the result of pdist

        for d in range(dim):
            pos_1d = k[:, d][:, np.newaxis]  # shape (N, 1)
            dist_1d = pdist(pos_1d)  # shape (N * (N - 1) // 2, )
            dist_1d[dist_1d > 0.5 * Lbox[d]] -= Lbox[d]
            dist_nd_sq += dist_1d**2

        return np.sqrt(dist_nd_sq)


def _get_cdist_pbc(m, n, Lbox=None, ipick=None, jpick=None):
    """pdist with periodic bounday conditions.
    Uses still scipy pdist to be fast.

    L_box is float
    """
    if ipick is not None:
        return _get_cdist_pbc(m[ipick], n, Lbox, jpick=jpick)
    if jpick is not None:
        return _get_cdist_pbc(m, n[jpick], Lbox)

    if Lbox is None:
        dist_1d = cdist(m, n)  # shape (N * (N - 1) // 2, )
        return dist_1d
    else:
        N_m, dim_m = m.shape
        N_n, dim_n = n.shape
        # dist_nd_sq = np.zeros(N * (N - 1) // 2)  # to match the result of pdist
        dist_nd_sq = np.zeros((N_m, N_n))  # to match the result of pdist

        print(f"{N_m = }")
        print(f"{N_n = }")
        print(f"{np.shape(dist_nd_sq) = }")
        print(f"{np.shape(dist_nd_sq) = }")

        for d in range(dim_m):
            pos_1d_m = m[:, d][:, np.newaxis]  # shape (N, 1)
            pos_1d_n = n[:, d][:, np.newaxis]  # shape (N, 1)

            print(f"{np.shape(pos_1d_m) = }")
            print(f"{np.shape(pos_1d_n) = }")

            dist_1d = cdist(pos_1d_m, pos_1d_n)  # shape (N * (N - 1) // 2, )

            print(f"{np.shape(dist_1d) = }")

            dist_1d[dist_1d > 0.5 * Lbox[d]] -= Lbox[d]

            print(f" After condition: {np.shape(dist_1d) = }")

            dist_nd_sq += dist_1d**2

        return np.sqrt(dist_nd_sq)


def velocity_structure_function(
    ds,
    ad,
    outdir="velocity_structure_func/",
    cut_regions=[("all", None)],
    maxpoints=2e4,
    nbins=100,
    percentiles=[16, 50, 84],
    # plot=True,
    # new_fig=False,
    # fig=None,
    # ax=None,
    sim_name="",
):
    """
    Keyword Arguments:
    ds        dataset from yt
    ad        all_data? output of ds.covering_grid()?
    cut_regions  -- `cut_regions` is list of `(name, cut_string)` combinations.
           Example:
           ('hot', "obj['temperature'] > 1e6)
           or
           ('fast', 'obj["velocity_magnitude"].in_units("km/s") > 1')
           or
           ('all', None)
    """
    assert len(cut_regions) > 0

    Lbox = np.array(ad.get_bbox()[1] - ad.get_bbox()[0])

    # Create directory for plots
    # h.mkdir(outdir)
    # if plot:
    #     plotoutdir = outdir + "plots/"
    #     h.mkdir(plotoutdir)
    #     # plt.clf()

    # cname -> Just name for the cut
    # cut_string -> cut condition

    return_dict = {}
    return_dict["means"] = []
    return_dict["dist_bins"] = []
    return_dict["qs"] = []
    return_dict["cname"] = []

    for cname, cut_string in cut_regions:
        # output file name
        ofn = outdir + str(ds) + "_" + cname + f"_{sim_name}.npz"

        # # Check if file already exists
        # if os.path.isfile(ofn):
        #     logging.info("%s exists already. Skipping VSF computation." % (ofn))
        #     continue
        logging.info(
            "Computing velocity structure function for %s [%s] --> %s",
            str(ds),
            cname,
            ofn,
        )

        # Check if cut_string is empty
        # cad -> ad after applying the cut condition
        if cut_string is None or cut_string == "":
            cad = ad
        else:
            cad = ad.cut_region(cut_string)

        # position array for cad as [pos_x, pos_y, pos_z]
        pos = np.array([cad[ii].value for ii in ["x", "y", "z"]]).T

        # Checking for number of points after cut
        logging.info("Computing VSF for %s", str(pos.shape))
        npoints = pos.shape[0]

        print("_________________________________________")
        print(f"{npoints = }")
        print(f"{maxpoints = }")
        print("_________________________________________")

        # Go to the next cut condition if no points found
        if npoints == 0:
            logging.warning("No points!")
            continue

        # if too many points
        if npoints > maxpoints:
            logging.info("Too many points (>%e), discarding some.", maxpoints)
            print("_________________________________________")
            print("Too many points (>%e), discarding some.", maxpoints)
            ipoints = np.random.permutation(npoints)[: int(maxpoints)]
            print("Points selected successfully!!")
            print("_________________________________________")
        else:
            ipoints = None

        # Trying to be memory efficient
        ds.index.clear_all_data()

        print("_________________________________________")
        print("Cleared memory!...")
        print("_________________________________________")

        # Computing distance in real space
        logging.info("Computing distance in real space.")
        dists = _get_pdist_pbc(pos, Lbox, ipoints)
        del pos
        gc.collect()

        print("_________________________________________")
        print("Distance calculated!...")
        print("_________________________________________")

        # ipoints = None, means everything's good
        # else, it had crossed maxpoints, so select randomly
        if ipoints is None:
            vels = np.array([cad["velocity_" + ii].value for ii in ["x", "y", "z"]]).T
        else:
            vels = np.array(
                [cad["velocity_" + ii].value[ipoints] for ii in ["x", "y", "z"]]
            ).T
        del ipoints
        gc.collect()

        print("_________________________________________")
        print("Getting velocity in velocity space!...")
        print("_________________________________________")

        # Trying to be memory efficient
        ds.index.clear_all_data()

        # Computing distance in velocity space
        logging.info("Computing distance in velocity space.")
        veldiffs = _get_pdist_pbc(vels)
        del vels
        gc.collect()

        # Computing binned quantities
        logging.info("Computing binned quantities.")
        dist_bins = np.logspace(np.log10(dists.min()), np.log10(dists.max()), nbins)
        ibins = np.digitize(dists, dist_bins)

        del dists
        gc.collect()

        # Main velocity structure function calculation?
        nums = []
        qs = []
        means = []
        for i in range(nbins):
            m = ibins == i
            nums.append(np.sum(m))
            means.append(np.mean(veldiffs[m]))

            if np.sum(m) == 0:
                qs.append(np.repeat(np.nan, len(percentiles)))
            else:
                qs.append(np.percentile(veldiffs[m], percentiles))

        means = np.array(means)
        qs = np.array(qs)
        nums = np.array(nums)

        # Saving the output
        logging.info("Outputting to %s.", ofn)
        np.savez(
            ofn,
            distance_bins=dist_bins,
            velocity_means=means,
            velocity_percentiles=qs,
            number=nums,
        )
        logging.info("Done outputting to %s", ofn)

        return_dict["means"].append(means)
        return_dict["dist_bins"].append(dist_bins)
        return_dict["qs"].append(qs)
        return_dict["cname"].append(cname)

        # if plot:
        #     if new_fig:
        #         fig, ax = plt.subplots()

        #     # print(means)

        #     ax.plot(dist_bins, means, label=cname)
        #     ax.fill_between(dist_bins, qs[:, 0], qs[:, -1], alpha=0.2, label=cname)

        #     ax.legend(loc="best")
        #     ax.loglog()
        #     ax.set_xlabel(r"$d$ (kpc$^{-1}$)", fontsize=20)
        #     # ax.set_ylabel(r"$\langle | v | \rangle$", fontsize=20)

        del means, qs, nums
        del dist_bins, ibins
        del veldiffs
        gc.collect()

    return return_dict

    # Saving the plot
    # if plot and plotted:
    #     ax.legend(loc="best")
    #     ax.loglog()
    #     ax.set_xlabel(r"$d$", fontsize=20)
    #     ax.set_ylabel(r"$\langle | v | \langle$", fontsize=20)
    #     ofn_plot = plotoutdir + str(ds) + ".png"
    #     # logging.info("Saving plot to %s", ofn_plot)
    #     # plt.savefig(ofn_plot, bbox_inches="tight")
    #     return fig, ax


def cross_velocity_structure_function(
    ds,
    ad,
    outdir="velocity_structure_func/",
    cut_regions=[("all", None)],
    maxpoints=2e4,
    nbins=100,
    percentiles=[16, 50, 84],
    sim_name="",
):
    """
    Keyword Arguments:
    ds        dataset from yt
    ad        all_data? output of ds.covering_grid()?
    cut_regions  -- `cut_regions` is list of `(name, cut_string)` combinations.
           Example:
           ('hot', "obj['temperature'] > 1e6)
           or
           ('fast', 'obj["velocity_magnitude"].in_units("km/s") > 1')
           or
           ('all', None)
    """
    assert len(cut_regions) > 0

    Lbox = np.array(ad.get_bbox()[1] - ad.get_bbox()[0])

    return_dict = {}
    return_dict["means"] = []
    return_dict["dist_bins"] = []
    return_dict["qs"] = []
    return_dict["cname"] = []

    cname_list = []
    cut_list = []

    for cname, cut_string in cut_regions:
        cname_list.append(cname)
        cut_list.append(cut_string)

    # output file name
    ofn = outdir + str(ds) + "_" + "cross" + f"_{sim_name}.npz"

    logging.info(
        "Computing cross velocity structure function for %s [%s] --> %s",
        f"between {cname[0]} and {cname[1]}",
        str(ds),
        ofn,
    )

    # Check if cut_string is empty
    # cad -> ad after applying the cut condition
    # if cut_string is None or cut_string == "":
    #     cad = ad
    # else:
    cad_0 = ad.cut_region(cut_list[0])
    cad_1 = ad.cut_region(cut_list[1])

    # position array for cad as [pos_x, pos_y, pos_z]
    pos0 = np.array([cad_0[ii].value for ii in ["x", "y", "z"]]).T
    pos1 = np.array([cad_1[ii].value for ii in ["x", "y", "z"]]).T

    # Checking for number of points after cut
    logging.info("Computing VSF for %s %s", str(pos0.shape), str(pos1.shape))
    npoints0 = pos0.shape[0]
    npoints1 = pos1.shape[0]

    print("_________________________________________")
    print(f"{npoints0 = }")
    print(f"{npoints1 = }")
    print(f"{maxpoints = }")
    print("_________________________________________")

    # Go to the next cut condition if no points found
    if npoints0 == 0 or npoints1 == 0:
        logging.warning("No points!")
        exit()

    # if too many points
    if npoints0 > maxpoints:
        logging.info("Too many points in first set (>%e), discarding some.", maxpoints)
        print("_________________________________________")
        print("Too many points in first set (>%e), discarding some.", maxpoints)
        ipoints = np.random.permutation(npoints0)[: int(maxpoints)]
        print("Points selected successfully!!")
        print("_________________________________________")
    else:
        ipoints = None

    if npoints1 > maxpoints:
        logging.info("Too many points in second set (>%e), discarding some.", maxpoints)
        print("_________________________________________")
        print("Too many points in second set (>%e), discarding some.", maxpoints)
        jpoints = np.random.permutation(npoints1)[: int(maxpoints)]
        print("Points selected successfully!!")
        print("_________________________________________")
    else:
        jpoints = None

    # Trying to be memory efficient
    ds.index.clear_all_data()

    print("_________________________________________")
    print("Cleared memory!...")
    print("_________________________________________")

    # Computing distance in real space
    logging.info("Computing distance in real space.")
    dists = _get_cdist_pbc(pos0, pos1, Lbox, ipoints, jpoints)
    del pos0, pos1
    gc.collect()

    print("_________________________________________")
    print("Distance calculated!...")
    print("_________________________________________")

    # ipoints = None, means everything's good
    # else, it had crossed maxpoints, so select randomly
    if ipoints is None:
        vels0 = np.array([cad_0["velocity_" + ii].value for ii in ["x", "y", "z"]]).T
    else:
        vels0 = np.array(
            [cad_0["velocity_" + ii].value[ipoints] for ii in ["x", "y", "z"]]
        ).T

    if jpoints is None:
        vels1 = np.array([cad_1["velocity_" + jj].value for jj in ["x", "y", "z"]]).T
    else:
        vels1 = np.array(
            [cad_1["velocity_" + jj].value[jpoints] for jj in ["x", "y", "z"]]
        ).T

    del ipoints, jpoints
    gc.collect()

    print("_________________________________________")
    print("Getting velocity in velocity space!...")
    print("_________________________________________")

    # Trying to be memory efficient
    ds.index.clear_all_data()

    # Computing distance in velocity space
    logging.info("Computing distance in velocity space.")
    veldiffs = _get_cdist_pbc(vels0, vels1)
    del vels0, vels1
    gc.collect()

    # Computing binned quantities
    logging.info("Computing binned quantities.")
    dist_bins = np.logspace(np.log10(dists.min()), np.log10(dists.max()), nbins)
    ibins = np.digitize(dists, dist_bins)

    del dists
    gc.collect()

    # Main velocity structure function calculation?
    nums = []
    qs = []
    means = []
    for i in range(nbins):
        m = ibins == i
        nums.append(np.sum(m))
        means.append(np.mean(veldiffs[m]))

        if np.sum(m) == 0:
            qs.append(np.repeat(np.nan, len(percentiles)))
        else:
            qs.append(np.percentile(veldiffs[m], percentiles))

    means = np.array(means)
    qs = np.array(qs)
    nums = np.array(nums)

    # Saving the output
    logging.info("Outputting to %s.", ofn)
    np.savez(
        ofn,
        distance_bins=dist_bins,
        velocity_means=means,
        velocity_percentiles=qs,
        number=nums,
    )
    logging.info("Done outputting to %s", ofn)

    return_dict["means"].append(means)
    return_dict["dist_bins"].append(dist_bins)
    return_dict["qs"].append(qs)
    return_dict["cname"].append(cname)

    del means, qs, nums
    del dist_bins, ibins
    del veldiffs
    gc.collect()

    return return_dict
