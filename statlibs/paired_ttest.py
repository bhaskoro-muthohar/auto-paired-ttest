"""
A module to auto calculate inferential statistic of paired t-test.
"""

# Original author (2022): Bhaskoro Muthohar

from typing import Union, Tuple, Optional, Dict, Any
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pylab
import matplotlib


class AutoPairedTest:
    """
    A class for automating paired sample t-tests with proper statistical checks.
    
    This class handles data visualization, normality testing, and appropriate
    statistical test selection (t-test or Wilcoxon) based on data characteristics.
    """
    
    def __init__(self, df: pd.DataFrame, col_dif: str, col_before: str, col_after: str):
        """
        Initialize the AutoPairedTest object.
        
        Args:
            df: DataFrame containing the paired data
            col_dif: Column name for the difference between before and after
            col_before: Column name for measurements before intervention
            col_after: Column name for measurements after intervention
        
        Raises:
            ValueError: If required columns are missing or contain non-numeric data
        """
        # Validate input data
        for col in [col_dif, col_before, col_after]:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in DataFrame")
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"Column '{col}' must contain numeric data")
        
        self.df = df
        self.col_dif = col_dif
        self.col_before = col_before
        self.col_after = col_after
        self.outlier_stats: Dict[str, Any] = {}

    def run_test(self, sig_lvl: int = 5) -> Any:
        """
        Run the appropriate statistical test for paired samples.
        
        The method will:
        1. Visualize the data distribution
        2. Check for normality using Anderson-Darling test
        3. Choose appropriate test (t-test or Wilcoxon)
        4. Remove outliers if needed and re-test
        
        Args:
            sig_lvl: Significance level for the Anderson-Darling test (default: 5%)
        
        Returns:
            Statistical test result (either TtestResult or WilcoxonResult)
        
        Raises:
            ValueError: If the significance level is invalid
        """
        if sig_lvl not in [1, 2, 5, 10, 15]:
            raise ValueError("Significance level must be one of: 1, 2, 5, 10, 15")
        
        n_pict = 2
        figsize = (18, 10)
        sns.set_theme("paper")
        sns.set(rc={"figure.figsize": (11.7, 8.27)})

        # Calculate quartiles for outlier detection
        Q1 = self.df[self.col_dif].quantile(0.25)
        Q3 = self.df[self.col_dif].quantile(0.75)
        IQR = Q3 - Q1
        
        # Store original sample size for outlier percentage calculation
        original_sample_size = len(self.df)

        # Create visualizations
        fig, axes = plt.subplots(n_pict, 1, figsize=figsize)
        for x in range(n_pict):
            if x == 0:
                sns.boxplot(ax=axes[x], data=self.df, x=self.col_dif)
            if x == 1:
                sns.kdeplot(ax=axes[x], data=self.df, x=self.col_dif)
        plt.show()

        stats.probplot(self.df[self.col_dif], dist="norm", plot=pylab)
        plt.show()

        # Normality test using Anderson-Darling
        anderson_test = stats.anderson(self.df[self.col_dif])
        print(f"Anderson Statistic: {anderson_test.statistic}")

        result = None  

        # Print normality test results for all significance levels
        for i in range(len(anderson_test.critical_values)):
            sig_lev, crit_val = (anderson_test.significance_level[i], anderson_test.critical_values[i])
            if anderson_test.statistic < crit_val:
                print(f"Probably gaussian : {crit_val} critical value at {sig_lev} level of significance")
            else:
                print(f"Probably not gaussian : {crit_val} critical value at {sig_lev} level of significance")

        # Run appropriate test based on normality at the specified significance level
        for i in range(len(anderson_test.critical_values)):
            sig_lev, crit_val = (anderson_test.significance_level[i], anderson_test.critical_values[i])
            if sig_lev == sig_lvl:
                if anderson_test.statistic < crit_val:
                    # Data is normally distributed - use t-test
                    result = stats.ttest_rel(self.df[self.col_before], self.df[self.col_after])
                    print(result)
                    self.outlier_stats = {
                        "outliers_removed": False,
                        "original_sample_size": original_sample_size,
                        "final_sample_size": original_sample_size,
                        "outlier_percentage": 0.0
                    }
                else:
                    # Data is not normally distributed - remove outliers and retest
                    df_clean = self.df.loc[
                        (self.df[self.col_dif] > (Q1 - 1.5 * IQR))
                        & (self.df[self.col_dif] < (Q3 + 1.5 * IQR))
                    ]
                    
                    # Calculate and store outlier statistics
                    outliers_count = original_sample_size - len(df_clean)
                    outlier_percentage = (outliers_count / original_sample_size) * 100 if original_sample_size > 0 else 0
                    
                    self.outlier_stats = {
                        "outliers_removed": True,
                        "original_sample_size": original_sample_size,
                        "final_sample_size": len(df_clean),
                        "outlier_count": outliers_count,
                        "outlier_percentage": outlier_percentage
                    }
                    
                    print(f"Removed {outliers_count} outliers ({outlier_percentage:.2f}%)")

                    # Normality re-test after outlier removal
                    anderson_retest = stats.anderson(df_clean[self.col_dif])

                    for j in range(len(anderson_retest.critical_values)):
                        sig_lev, crit_val = (
                            anderson_retest.significance_level[j],
                            anderson_retest.critical_values[j],
                        )
                        if sig_lev == sig_lvl:
                            if anderson_retest.statistic < crit_val:
                                # After outlier removal, data is normally distributed - use t-test
                                result = stats.ttest_rel(df_clean[self.col_before], df_clean[self.col_after])
                                print(result)
                            else:
                                # After outlier removal, data is still not normally distributed - use Wilcoxon
                                result = stats.wilcoxon(df_clean[self.col_before], df_clean[self.col_after])
                                print(result)

        if result is None:
            raise ValueError(f"No test result found for significance level {sig_lvl}")
            
        return result
        
    def get_outlier_stats(self) -> Dict[str, Any]:
        """
        Get statistics about outliers in the data.
        
        Returns:
            Dictionary containing outlier statistics:
            - outliers_removed: Whether outliers were removed
            - original_sample_size: Size of original dataset
            - final_sample_size: Size after outlier removal
            - outlier_count: Number of outliers removed
            - outlier_percentage: Percentage of outliers in original data
        """
        return self.outlier_stats
