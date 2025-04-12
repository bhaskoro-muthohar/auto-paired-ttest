API Reference
=============

The main components of Auto Paired Test:

.. toctree::
   :maxdepth: 2
   :caption: Python API:

   auto_paired_test

Usage Examples
=============

Basic Usage
-----------

.. code-block:: python

   import pandas as pd
   from statlibs import AutoPairedTest

   # Create sample data
   df = pd.DataFrame({
       'before': [10, 12, 15, 9, 11],
       'after': [15, 14, 18, 12, 13],
       'diff': [5, 2, 3, 3, 2]  # after - before
   })

   # Create and run the test
   test = AutoPairedTest(df, "diff", "before", "after")
   result = test.run_test()
   
   # Get outlier statistics
   outlier_stats = test.get_outlier_stats()

Working with Non-Normal Data
---------------------------

.. code-block:: python

   import pandas as pd
   import numpy as np
   from statlibs import AutoPairedTest

   # Create non-normal data with outliers
   np.random.seed(42)
   before = np.random.exponential(scale=10, size=30)
   after = before + np.random.exponential(scale=2, size=30)
   before[0] = 100  # Add outlier
   after[1] = 150   # Add outlier
   diff = after - before
   
   df = pd.DataFrame({
       'before': before,
       'after': after,
       'diff': diff
   })

   # The AutoPairedTest class will automatically:
   # 1. Detect the non-normal distribution
   # 2. Handle outliers appropriately
   # 3. Select the non-parametric test (Wilcoxon)
   test = AutoPairedTest(df, "diff", "before", "after")
   result = test.run_test()

   # Check which test was used
   print(f"Test used: {result['test_used']}")
   
   # Get outlier information
   outlier_stats = test.get_outlier_stats()
   print(f"Outliers removed: {outlier_stats['outliers_removed']}")
   if outlier_stats['outliers_removed']:
       print(f"Outlier count: {outlier_stats['outlier_count']}")
       print(f"Outlier percentage: {outlier_stats['outlier_percentage']:.2f}%")