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
import pandas as pd
import logging
from class_project.data_proc import main, data_analysis


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)

CURRENT_DIR = os.path.dirname(__file__)
TEST_DIR = CURRENT_DIR
MAIN_DIR = os.path.join(CURRENT_DIR, '..')
PROJ_DIR = os.path.join(MAIN_DIR, 'class_project')
TEST_DATA_DIR = os.path.join(TEST_DIR, 'data_proc')
DATA_DIR = os.path.join(PROJ_DIR, 'data')
RES_DIR = os.path.join(PROJ_DIR, 'results')

SAMPLE_DATA_FILE_LOC = os.path.join(DATA_DIR, 'sample_data.csv')
SAMPLE_RES_FILENAME = ['sample_data_plot_A-', 'sample_data_plot_A+', 'sample_data_plot_S-', 'sample_data_plot_S+']
# SAMPLE_RES_FILENAME_1 = 'sample_data_plot_A-'
# SAMPLE_RES_FILENAME_2 = 'sample_data_plot_A+'
# SAMPLE_RES_FILENAME_3 = 'sample_data_plot_S-'
# SAMPLE_RES_FILENAME_4 = 'sample_data_plot_S+'


def silent_remove(filename, disable=False):  # ============================================================
    if not disable:
        try:
            os.remove(filename)
        except OSError as e:
            if e.error != errno.ENOENT:
                raise


class TestMain(unittest.TestCase):  # ====================================================================

    def test_SampleData(self):
        for i in range(4):
            silent_remove(os.path.join(RES_DIR, SAMPLE_RES_FILENAME[i] + '.png'), DISABLE_REMOVE)
            silent_remove(os.path.join(RES_DIR, SAMPLE_RES_FILENAME[i] + '.csv'), DISABLE_REMOVE)

        test_input = ["-c", SAMPLE_DATA_FILE_LOC]
        try:
            if logger.isEnabledFor(logging.DEBUG):
                main(test_input)
            with capture_stdout(main, test_input) as output:
                self.assertTrue(SAMPLE_RES_FILENAME[0] + '.csv' in output)

            for i in range(4):
                self.assertTrue(os.path.isfile(os.path.join(RES_DIR, SAMPLE_RES_FILENAME[i] + '.png')))
                self.assertTrue(os.path.isfile(os.path.join(RES_DIR, SAMPLE_RES_FILENAME[i] + '.csv')))

        finally:
            for i in range(4):
                silent_remove(os.path.join(RES_DIR, SAMPLE_RES_FILENAME[i] + '.png'), DISABLE_REMOVE)
                silent_remove(os.path.join(RES_DIR, SAMPLE_RES_FILENAME[i] + '.csv'), DISABLE_REMOVE)


class TestMainFailWell(unittest.TestCase):  # =============================================================
    def test_MissingFile(self):
        test_input = ["-c", "ghost.txt"]
        if logger.isEnabledFor(logging.DEBUG):
            main(test_input)
        with capture_stderr(main, test_input) as output:
            self.assertTrue("ghost.txt" in output)


class TestDataAnalysis(unittest.TestCase):  # =============================================================
    def test_SampleData1(self):
        csv_data = pd.read_csv(SAMPLE_DATA_FILE_LOC)
        analysis_results = data_analysis(csv_data, 'A', '-', True)
        expected_results = np.loadtxt(fname=os.path.join(TEST_DATA_DIR, SAMPLE_RES_FILENAME[0] +
                                                         '_norm.csv'), delimiter=',')
        self.assertTrue(np.allclose(expected_results, analysis_results))

    def test_SampleData2(self):
        csv_data = pd.read_csv(SAMPLE_DATA_FILE_LOC)
        analysis_results = data_analysis(csv_data, 'A', '+', True)
        expected_results = np.loadtxt(fname=os.path.join(TEST_DATA_DIR, SAMPLE_RES_FILENAME[1] +
                                                         '_norm.csv'), delimiter=',')
        self.assertTrue(np.allclose(expected_results, analysis_results))

    def test_SampleData3(self):
        csv_data = pd.read_csv(SAMPLE_DATA_FILE_LOC)
        analysis_results = data_analysis(csv_data, 'S', '-', True)
        expected_results = np.loadtxt(fname=os.path.join(TEST_DATA_DIR, SAMPLE_RES_FILENAME[2] +
                                                         '_norm.csv'), delimiter=',')
        self.assertTrue(np.allclose(expected_results, analysis_results))

    def test_SampleData4(self):
        csv_data = pd.read_csv(SAMPLE_DATA_FILE_LOC)
        analysis_results = data_analysis(csv_data, 'S', '+', True)
        expected_results = np.loadtxt(fname=os.path.join(TEST_DATA_DIR, SAMPLE_RES_FILENAME[3] +
                                                         '_norm.csv'), delimiter=',')
        self.assertTrue(np.allclose(expected_results, analysis_results))

    def test_SampleData11(self):
        csv_data = pd.read_csv(SAMPLE_DATA_FILE_LOC)
        analysis_results = data_analysis(csv_data, 'A', '-', False)
        expected_results = np.loadtxt(fname=os.path.join(TEST_DATA_DIR, SAMPLE_RES_FILENAME[0] +
                                                         '_real.csv'), delimiter=',')
        self.assertTrue(np.allclose(expected_results, analysis_results))

# Utility functions =======================================================================================
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


@contextmanager
def capture_stderr(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    err, sys.stderr = sys.stderr, StringIO()
    command(*args, **kwargs)
    sys.stderr.seek(0)
    yield sys.stderr.read()
    sys.stderr = err
