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
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = 'class_project'
DATA_DIR = 'data'
DEFAULT_DATA_FN = DATA_DIR + '\experimentalData.csv'

MODULUS_0_AVG = 7539.0
MODULUS_0_STDDEV = 2.2


def warning(*objs):  # =====================================================================================
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def data_analysis(df, alignment, archi, value_type):  # =================================================================
    """
        - Filtering
        - Convert to Numpy Array
        - Convert std. dev. from % to real values
    """

    # FILTERING -----------
    a = df.loc[df['Defect_alignment'] == alignment]
    b = a.loc[a['Defect_architecture'] == archi]
    b = b.drop(columns=["Defect_alignment", "Defect_architecture"])
    print(b)

    # CONVERTING ----------
    c = b.values
    print(c)
    baseline = [0, MODULUS_0_AVG, MODULUS_0_STDDEV]
    c = np.vstack([baseline, c])
    c[:, 2] = np.multiply(c[:, 1], c[:, 2])/100

    if value_type:
        ylimit = 1.3
        ylabel_text = value_type + ' modulus (-)'
        # Normalize
        c[:, 1] = c[:, 1] / MODULUS_0_AVG
        c[:, 2] = c[:, 2] / MODULUS_0_AVG
    else:
        ylimit = 8500
        ylabel_text = ' modulus (ksi)'

    print(c)

    # PLOTTING ------------
    # plt.plot(b[:, 0], b[:, 1], 'bs') # cannot plot data frame ...
    plt.plot([0, 5.5], [c[0, 1], c[0, 1]], 'b--')
    plt.plot(c[:, 0], c[:, 1], 'r.')
    plt.errorbar(c[:, 0], c[:, 1], yerr=c[:, 2], fmt='o', capsize=5)
    plt.title('Modulus of Defect Specimens (' + alignment + archi + ')')
    plt.xlabel('defect size (in)')
    plt.ylabel(ylabel_text)
    plt.axis([0, 0.55, 0, ylimit])
    plt.grid(True)
    # plt.show()
    plt.savefig("resultPlot_" + alignment + archi + ".png")
    plt.clf()


def parse_cmdline(argv):  # ================================================================================
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
    group.add_argument("-r", "--real_values", help="Plotting real values", action="store_true", default=True)
    group.add_argument("-n", "--normalized_values", help="Plotting normalized values", action="store_true", default=False)

    args = None
    try:
        args = parser.parse_args(argv)
        # args.csv_data = np.loadtxt(fname=args.csv_data_file, delimiter=',')
        args.csv_data = pd.read_csv(args.csv_data_file)
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, 1
    except ValueError as e:
        warning("Read invalid data:", e)
        parser.print_help()
        return args, 2

    return args, 0


def plot_data(data_array):  # =========================================================================================
    """
        Plotting error bars
        https://matplotlib.org/1.2.1/examples/pylab_examples/errorbar_demo.html
    """
    pass


def main(argv=None):  # =====================================================================================
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret

    value_type = ''
    if args.normalized_values:
        value_type = 'Normalized'
    print(value_type)

    # print(args.csv_data)
    # data = args.csv_data
    # print(data.index)
    # print(data.columns)

    # print(data.ix[:, 'Defect_alignment'])
    data_analysis(args.csv_data, 'A', '-', value_type)
    data_analysis(args.csv_data, 'A', '+', value_type)
    data_analysis(args.csv_data, 'S', '-', value_type)
    data_analysis(args.csv_data, 'S', '+', value_type)

    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
