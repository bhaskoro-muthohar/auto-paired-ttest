""" [WIP] Test functions for auto paired t-test module
    WRITTEN BY Bhaskoro Muthohar <bhaskoro.jr@gmail.com> 
"""

import unittest
from src import AutoPairedTtest

class AutoPairedTtest_tests:

    def setUp(self):
        array_rand = np.random.randint(100, size=(5, 2))
        array_rand_diff = np.subtract.reduce(array_rand, axis=1).reshape(-1, 1)
        array = np.hstack((array_rand, array_rand_diff))
        column = ['before', 'after', 'diff']
        df = pd.DataFrame(data = array, columns = column)

        self.auto_paired_ttest = AutoPairedTtest_tests(df)

if __name__ == '__main__':
    unittest.main()