import argparse
import logging
import yt
import glob
import pandas
import os


def setup_argparse():
    parser = argparse.ArgumentParser(
        description="Compute....",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("out_prefix", help="The prefix to use for the output.")
    parser.add_argument(
        "vtk_filelst", help="List of vtk files (expands `*`)", nargs="+"
    )
    parser.add_argument(
        "-nstep", help="Only analyze every `nstep` files.", default=1, type=int
    )

    return parser.parse_args()


def main():
    args = setup_argparse()
    if "*" in args.vtk_filelst:
        fnlst = glob.glob(args.vtk_filelst)
        if yt.is_root():
            logging.info("Using path.")
    elif not os.path.isfile(args.vtk_filelst[0]):
        fnlst = glob.glob(os.path.abspath(args.vtk_filelst[0]) + "/*.vtk")
        if yt.is_root():
            logging.info("Using all files in folder.")
    else:
        fnlst = args.vtk_filelst
        if yt.is_root():
            logging.info("Using files given.")

    fnlst = sorted([i for i in fnlst if os.path.isfile(i)])[:: args.nstep]

    assert len(fnlst) > 0, "No vtk files found...?"

    storage = {}

    for sto, cfn in yt.parallel_objects(fnlst, storage=storage):
        logging.info(">>>> Computing quantities for %s", cfn)

        ds = yt.load(cfn)
        ad = ds.all_data()

        sto.result_id = cfn
        sto.result = {}

        ...  # compute stuff here

        # save like this:
        sto.result["time"] = float(ds.current_time.value)

    # now output the things to a file
    if yt.is_root():
        outpre = args.out_prefix
        logging.info("Gathering all data and save to %s*", outpre)

        df = pandas.DataFrame(storage).T
        # sort columns
        colnames = ["time"] + [i for i in df.keys() if i != "time"]
        logging.info("Columns: %s" % (str(colnames)))

        df = df[colnames]
        df.to_hdf(outpre + ".hdf5", "dat")
        hdr = ["# " + df.columns[0]] + [i for i in df.columns[1:]]
        df.to_csv(outpre + ".dat", sep="\t", index=False, header=hdr, na_rep="nan")

        logging.info(">>> Done with everything.")
