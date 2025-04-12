import unittest
import pandas as pd
import numpy as np
from statlibs import AutoPairedTest

class AutoPairedTestTests(unittest.TestCase):

    def setUp(self):
        # Create normal (Gaussian) test data
        np.random.seed(42)  # Set seed for reproducibility
        before = np.random.normal(loc=50, scale=10, size=30)
        after = before + np.random.normal(loc=5, scale=2, size=30)  # Simulating improvement
        diff = after - before
        
        self.df_normal = pd.DataFrame({
            'before': before,
            'after': after,
            'diff': diff
        })
        
        # Create non-normal test data with outliers
        np.random.seed(43)
        before = np.random.exponential(scale=10, size=30)
        after = before + np.random.exponential(scale=2, size=30)
        
        # Add outliers
        before[0] = 100  # Add outlier
        after[1] = 150   # Add outlier
        diff = after - before
        
        self.df_non_normal = pd.DataFrame({
            'before': before,
            'after': after,
            'diff': diff
        })
        
        # Small dataset for basic testing
        array_rand = np.random.randint(100, size=(5, 2))
        array_rand_diff = np.subtract.reduce(array_rand, axis=1).reshape(-1, 1)
        array = np.hstack((array_rand, array_rand_diff))
        column = ['before', 'after', 'diff']
        self.df_small = pd.DataFrame(data=array, columns=column)
        
        # Invalid data for testing error handling
        self.df_invalid = pd.DataFrame({
            'before': np.random.normal(loc=50, scale=10, size=5),
            'after': np.random.normal(loc=55, scale=10, size=5),
            'missing_diff': np.random.normal(loc=5, scale=2, size=5)
        })
        
        self.df_non_numeric = pd.DataFrame({
            'before': np.random.normal(loc=50, scale=10, size=5),
            'after': np.random.normal(loc=55, scale=10, size=5),
            'diff': ['a', 'b', 'c', 'd', 'e']  # Non-numeric data
        })

    def test_basic_run_test(self):
        """Test basic functionality with small dataset."""
        auto_paired_test = AutoPairedTest(self.df_small, "diff", "before", "after")
        result = auto_paired_test.run_test()
        self.assertIsNotNone(result)
    
    def test_normal_data(self):
        """Test with normally distributed data."""
        auto_paired_test = AutoPairedTest(self.df_normal, "diff", "before", "after")
        result = auto_paired_test.run_test()
        self.assertIsNotNone(result)
        
        # Check outlier stats when no outliers are removed
        outlier_stats = auto_paired_test.get_outlier_stats()
        self.assertFalse(outlier_stats["outliers_removed"])
        self.assertEqual(outlier_stats["original_sample_size"], len(self.df_normal))
        self.assertEqual(outlier_stats["final_sample_size"], len(self.df_normal))
        self.assertEqual(outlier_stats["outlier_percentage"], 0.0)
    
    def test_non_normal_data_with_outliers(self):
        """Test with non-normal data containing outliers."""
        auto_paired_test = AutoPairedTest(self.df_non_normal, "diff", "before", "after")
        result = auto_paired_test.run_test()
        self.assertIsNotNone(result)
        
        # Check outlier stats when outliers are removed
        outlier_stats = auto_paired_test.get_outlier_stats()
        if outlier_stats["outliers_removed"]:
            self.assertTrue(outlier_stats["outlier_count"] > 0)
            self.assertTrue(outlier_stats["outlier_percentage"] > 0)
            self.assertTrue(outlier_stats["final_sample_size"] < outlier_stats["original_sample_size"])
    
    def test_invalid_significance_level(self):
        """Test that invalid significance levels raise errors."""
        auto_paired_test = AutoPairedTest(self.df_small, "diff", "before", "after")
        with self.assertRaises(ValueError):
            auto_paired_test.run_test(sig_lvl=3)  # 3 is not a valid significance level
    
    def test_column_validation(self):
        """Test that missing columns raise errors."""
        with self.assertRaises(ValueError):
            AutoPairedTest(self.df_invalid, "diff", "before", "after")
    
    def test_non_numeric_validation(self):
        """Test that non-numeric data raises errors."""
        with self.assertRaises(ValueError):
            AutoPairedTest(self.df_non_numeric, "diff", "before", "after")
    
    def test_outlier_stats_method(self):
        """Test that get_outlier_stats returns the expected structure."""
        auto_paired_test = AutoPairedTest(self.df_small, "diff", "before", "after")
        
        # Before running the test, outlier_stats should be empty
        self.assertEqual(auto_paired_test.get_outlier_stats(), {})
        
        # After running the test, outlier_stats should be populated
        auto_paired_test.run_test()
        stats = auto_paired_test.get_outlier_stats()
        
        self.assertIn("outliers_removed", stats)
        self.assertIn("original_sample_size", stats)
        self.assertIn("final_sample_size", stats)
        self.assertIsNotNone(stats["outliers_removed"])
        self.assertIsInstance(stats["original_sample_size"], int)
        self.assertIsInstance(stats["final_sample_size"], int)

if __name__ == '__main__':
    unittest.main()