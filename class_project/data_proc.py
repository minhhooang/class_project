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
RES_DIR = 'results'
DEFAULT_DATA_FN = DATA_DIR + '\sample_data.csv'

MODULUS_0_AVG = 7539.0
MODULUS_0_STDDEV = 2.2
BASELINE = [0, MODULUS_0_AVG, MODULUS_0_STDDEV]


def warning(*objs):  # =====================================================================================
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def data_analysis(df, alignment, archi, value_type):  # ====================================================
    """
        - Filtering
        - Convert to Numpy Array
        - Convert std. dev. from % to real values
    """

    # FILTERING -----------
    df = df.loc[df['Defect_alignment'] == alignment]
    df = df.loc[df['Defect_architecture'] == archi]
    df = df.drop(columns=["Defect_alignment", "Defect_architecture"])

    # CONVERTING ----------
    a = df.values
    a = np.vstack([BASELINE, a])
    a[:, 2] = np.multiply(a[:, 1], a[:, 2])/100

    if value_type:
        a[:, 1] = a[:, 1] / MODULUS_0_AVG
        a[:, 2] = a[:, 2] / MODULUS_0_AVG

    return a


def plot_data(a, alignment, archi, value_type, base_out_fname):  # =============================================
    """
        Plotting error bars
        https://matplotlib.org/1.2.1/examples/pylab_examples/errorbar_demo.html
    """

    if value_type:
        ylimit = 1.3
        ylabel_text = value_type + ' modulus (-)'
    else:
        ylimit = 8500
        ylabel_text = ' modulus (ksi)'

    plt.plot([0, 5.5], [a[0, 1], a[0, 1]], 'b--')
    plt.plot(a[:, 0], a[:, 1], 'r.')
    plt.errorbar(a[:, 0], a[:, 1], yerr=a[:, 2], fmt='o', capsize=5)
    plt.title('Modulus of Defect Specimens (' + alignment + archi + ')')
    plt.xlabel('defect size (in)')
    plt.ylabel(ylabel_text)
    plt.axis([0, 0.55, 0, ylimit])
    plt.grid(True)
    # plt.show()
    plt.savefig(RES_DIR + '\\' + base_out_fname + '_plot_' + alignment + archi + ".png")
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


def main(argv=None):  # =====================================================================================
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret

    value_type = ''
    if args.normalized_values:
        value_type = 'Normalized'
    print(value_type)

    configs = np.array([['A', '-'], ['A', '+'], ['S', '-'], ['S', '+']])
    for i in range(4):
        a = data_analysis(args.csv_data, configs[i, 0], configs[i, 1], value_type)
        base_out_fname = os.path.basename(args.csv_data_file)
        base_out_fname = os.path.splitext(base_out_fname)[0]
        plot_data(a, configs[i, 0], configs[i, 1], value_type, base_out_fname)

    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
