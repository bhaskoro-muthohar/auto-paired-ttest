import unittest
import pandas as pd
import numpy as np
from statlibs import AutoPairedTest

class AutoPairedTestTests(unittest.TestCase):

    def setUp(self):
        array_rand = np.random.randint(100, size=(5, 2))
        array_rand_diff = np.subtract.reduce(array_rand, axis=1).reshape(-1, 1)
        array = np.hstack((array_rand, array_rand_diff))
        column = ['before', 'after', 'diff']
        self.df = pd.DataFrame(data=array, columns=column)

    def test_run_test(self):
        auto_paired_test = AutoPairedTest(self.df, "diff", "before", "after")
        result = auto_paired_test.run_test()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()