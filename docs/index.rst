.. Auto Paired Test documentation master file, created by
   sphinx-quickstart on Thu Dec 29 15:40:57 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Auto Paired Test's documentation!
============================================

Auto Paired Test is a Python library that automates the process of testing paired samples for statistical significance. It handles data validation, visualization, normality testing, and automatic test selection based on data characteristics.

Features
--------

* Automatic selection between parametric (t-test) and non-parametric (Wilcoxon) tests
* Integrated outlier detection and handling
* Visualization of data distributions and results
* Built-in Google BigQuery integration for data retrieval
* Comprehensive validation of input data

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/api/index


Installation
===========

You can install Auto Paired Test via pip:

.. code-block:: bash

   pip install auto-paired-test


Quick Start
==========

.. code-block:: python

   import pandas as pd
   from statlibs import AutoPairedTest

   # Prepare your DataFrame with before, after, and difference columns
   df = pd.DataFrame({
       'before': [10, 12, 15, 9, 11],
       'after': [15, 14, 18, 12, 13],
       'diff': [5, 2, 3, 3, 2]  # after - before
   })

   # Create the test object and run the analysis
   test = AutoPairedTest(df, "diff", "before", "after")
   result = test.run_test()

   # Print the statistical test result
   print(result)



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
