#!/usr/bin/env python3
"""
Unit and regression test for the class_project package.
"""

# Import package, test suite, and other packages as needed
import errno
import os
import sys
import unittest
from contextlib import contextmanager
from io import StringIO
import numpy as np
import logging
from class_project import main, data_analysis


logging.basicConfig(level=logging.DEBUG)
logger =logging.getLogger(__name__)
DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)

CURRENT_DIR = os.path.dirname(__file__)
MAIN_DIR = os.path.join(CURRENT_DIR, '..')
TEST_DATA_DIR = os.path.join(CURRENT_DIR, 'data_proc')
PROJ_DIR = os.path.join(MAIN_DIR, 'class_project')
DATA_DIR = os.path.join(PROJ_DIR, 'data')
RES_DIR = os.path.join(PROJ_DIR, 'results')
SAMPLE_DATA_FILE_LOC = os.path.join(DATA_DIR, 'sample_data.csv')
SAMPLE_EXP_RES_FILENAME_1 = os.path.join(RES_DIR, 'sample_data_plot_A-.png')
SAMPLE_EXP_RES_FILENAME_2 = os.path.join(RES_DIR, 'sample_data_plot_A+.png')
SAMPLE_EXP_RES_FILENAME_3 = os.path.join(RES_DIR, 'sample_data_plot_S-.png')
SAMPLE_EXP_RES_FILENAME_4 = os.path.join(RES_DIR, 'sample_data_plot_S+.png')


def silent_remove(filename, disable=False):  # ============================================================
    if not disable:
        try:
            os.remove(filename)
        except OSError as e:
            if e.error != errno.ENOENT:
                raise


class TestMain(unittest.TestCase):  # ====================================================================

    def testSampleData(self):
        silent_remove(SAMPLE_EXP_RES_FILENAME_1, DISABLE_REMOVE)
        silent_remove(SAMPLE_EXP_RES_FILENAME_2, DISABLE_REMOVE)
        silent_remove(SAMPLE_EXP_RES_FILENAME_3, DISABLE_REMOVE)
        silent_remove(SAMPLE_EXP_RES_FILENAME_4, DISABLE_REMOVE)
        print("removed")

        test_input = ["-c", SAMPLE_DATA_FILE_LOC]
        try:
            if logger.isEnabledFor(logging.DEBUG):
                main(test_input)
            with capture_stdout(main, test_input) as output:
                self.assertTrue("..." in output)
            self.assertTrue(os.path.isfile(SAMPLE_EXP_RES_FILENAME_1))
            self.assertTrue(os.path.isfile(SAMPLE_EXP_RES_FILENAME_2))
            self.assertTrue(os.path.isfile(SAMPLE_EXP_RES_FILENAME_3))
            self.assertTrue(os.path.isfile(SAMPLE_EXP_RES_FILENAME_4))
            print("checked")
        finally:
            silent_remove(SAMPLE_EXP_RES_FILENAME_1, DISABLE_REMOVE)
            silent_remove(SAMPLE_EXP_RES_FILENAME_2, DISABLE_REMOVE)
            silent_remove(SAMPLE_EXP_RES_FILENAME_3, DISABLE_REMOVE)
            silent_remove(SAMPLE_EXP_RES_FILENAME_4, DISABLE_REMOVE)
            print("removed")


# Utility functions

# From http://schinckel.net/2013/04/15/capture-and-test-sys.stdout-sys.stderr-in-unittest.testcase/
@contextmanager
def capture_stdout(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    out, sys.stdout = sys.stdout, StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out
