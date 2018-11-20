#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
data_proc.py
ChE696 class project
Minh Hoang Nguyen
"""

from __future__ import print_function
import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = 'data'
DEFAULT_DATA_FN = DATA_DIR+'\experimentalData.csv'


def warning(*objs):  # =====================================================================================
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def canvas(with_attribution=True):  # ======================================================================
    """
    Placeholder function to show example docstring (NumPy format)

    Replace this function and doc string for your own project

    Parameters
    ----------
    with_attribution : bool, Optional, default: True
        Set whether or not to display who the quote is from

    Returns
    -------
    quote : str
        Compiled string including quote and optional attribution
    """

    quote = "The code is but a canvas to our imagination."
    if with_attribution:
        quote += "\n\t- Adapted from Henry David Thoreau"
    return quote


def parse_cmdline(argv):  # ==================================================================================
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser(description='Read in a csv (no header) of'
                                                 ' experimental data and plots results.')
    parser.add_argument("-c", "--csv_data_file", help="Directory and name of the csv file with data to analyzed.",
                        default=DEFAULT_DATA_FN)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--real_values", help="Plotting real values", action="store_true")
    group.add_argument("-n", "--normalized_values", help="Plotting normalized values", action="store_true")

    args = None
    try:
        args = parser.parse_args(argv)
        args.csv_data = np.loadtxt(fname=args.csv_data_file)
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, 1
    except ValueError as e:
        warning("Read invalid data:", e)
        parser.print_help()
        return args, 2

    return args, 0


def main(argv=None):  # =====================================================================================
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret
    # print(args)
    # print(canvas(args.no_attribution))

    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
