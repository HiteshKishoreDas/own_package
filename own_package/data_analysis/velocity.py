"""
 # @ Author: Hitesh Kishore Das
 # @ Created: 2023-02-23 22:13:59
 # @ Description: Stolen from Max :). Velocity related analysis stuff.
 """

from . import helpers as h

import numpy as np
import os
import logging
from scipy.spatial.distance import pdist

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _get_pdist(k, ipick=None):
    if ipick is None:
        return pdist(k)
    else:
        return pdist(k[ipick])


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


def velocity_structure_function(
    ds,
    ad,
    outdir="velocity_structure_func/",
    cut_regions=[("all", None)],
    maxpoints=2e4,
    nbins=100,
    percentiles=[16, 50, 84],
    plot=True,
    new_fig=True,
    fig=None,
    ax=None,
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
    h.mkdir(outdir)
    if plot:
        plotoutdir = outdir + "plots/"
        h.mkdir(plotoutdir)
        plt.clf()

    plotted = False
    # cname -> Just name for the cut
    # cut_string -> cut condition
    for cname, cut_string in cut_regions:

        # output file name
        ofn = outdir + str(ds) + "_" + cname + ".npz"

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

        # Go to the next cut condition if no points found
        if npoints == 0:
            logging.warning("No points!")
            continue

        # if too many points
        if npoints > maxpoints:
            logging.info("Too many points (>%e), discarding some.", maxpoints)
            ipoints = np.random.permutation(npoints)[: int(maxpoints)]
        else:
            ipoints = None

        # Trying to be memory efficient
        ds.index.clear_all_data()

        # Computing distance in real space
        logging.info("Computing distance in real space.")
        dists = _get_pdist_pbc(pos, Lbox, ipoints)
        del pos

        # ipoints = None, means everything's good
        # else, it had crossed maxpoints, so select randomly
        if ipoints is None:
            vels = np.array([cad["velocity_" + ii].value for ii in ["x", "y", "z"]]).T
        else:
            vels = np.array(
                [cad["velocity_" + ii].value[ipoints] for ii in ["x", "y", "z"]]
            ).T
        del ipoints

        # Trying to be memory efficient
        ds.index.clear_all_data()

        # Computing distance in velocity space
        logging.info("Computing distance in velocity space.")
        veldiffs = _get_pdist_pbc(vels)
        del vels

        # Computing binned quantities
        logging.info("Computing binned quantities.")
        dist_bins = np.logspace(np.log10(dists.min()), np.log10(dists.max()), nbins)
        ibins = np.digitize(dists, dist_bins)

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

        if plot:
            if new_fig:
                fig, ax = plt.subplots()

            ax.plot(dist_bins, means, label=cname)
            ax.fill_between(dist_bins, qs[:, 0], qs[:, -1], alpha=0.2, label=cname)

            plotted = True

        logging.info("Done outputting to %s", ofn)

    # Saving the plot
    if plot and plotted:
        ax.legend(loc="best")
        ax.loglog()
        ax.set_xlabel(r"$d$", fontsize=20)
        ax.set_ylabel(r"$\langle | v | \langle$", fontsize=20)
        ofn_plot = plotoutdir + str(ds) + ".png"
        # logging.info("Saving plot to %s", ofn_plot)
        # plt.savefig(ofn_plot, bbox_inches="tight")
        return fig, ax
