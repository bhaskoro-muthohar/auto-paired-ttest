"""
A module to auto calculate inferential statistic of paired t-test.

"""

# Original author (2022): Bhaskoro Muthohar

from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pylab
import matplotlib


class AutoPairedTest:
    def __init__(self, df, col_dif, col_before, col_after):
        self.df = df
        self.col_dif = col_dif
        self.col_before = col_before
        self.col_after = col_after

    def run_test(self, sig_lvl=5):
        n_pict = 2
        figsize = (18, 10)
        sns.set_theme("paper")
        sns.set(rc={"figure.figsize": (11.7, 8.27)})

        Q1 = self.df[self.col_dif].quantile(0.25)
        Q3 = self.df[self.col_dif].quantile(0.75)
        IQR = Q3 - Q1

        fig, axes = plt.subplots(n_pict, 1, figsize=figsize)
        for x in range(n_pict):
            if x == 0:
                sns.boxplot(ax=axes[x], data=self.df, x=self.col_dif)
            if x == 1:
                sns.kdeplot(ax=axes[x], data=self.df, x=self.col_dif)
        plt.show()

        stats.probplot(self.df[self.col_dif], dist="norm", plot=pylab)
        plt.show()

        # normality test
        ## 1. Anderson
        anderson_test = stats.anderson(self.df[self.col_dif])
        print(f"Anderson Statistic: {anderson_test.statistic}")
        for i in range(len(anderson_test.critical_values)):
            sig_lev, crit_val = (
                anderson_test.significance_level[i],
                anderson_test.critical_values[i],
            )
            if anderson_test.statistic < crit_val:
                print(
                    f"Probably gaussian : {crit_val} critical value at {sig_lev} level of significance"
                )
            else:
                print(
                    f"Probably not gaussian : {crit_val} critical value at {sig_lev} level of significance"
                )
        for i in range(len(anderson_test.critical_values)):
            sig_lev, crit_val = (
                anderson_test.significance_level[i],
                anderson_test.critical_values[i],
            )
            if sig_lev == sig_lvl:
                if anderson_test.statistic < crit_val:
                    print(
                        stats.ttest_rel(
                            self.df[self.col_before], self.df[self.col_after]
                        )
                    )
                else:
                    # outlier removal
                    df = self.df.loc[
                        (self.df[self.col_dif] > (Q1 - 1.5 * IQR))
                        & (self.df[self.col_dif] < (Q3 + 1.5 * IQR))
                    ]

                    ## normality re-test
                    anderson_retest = stats.anderson(df[self.col_dif])
                    # print(anderson_retest)

                    for i in range(len(anderson_retest.critical_values)):
                        sig_lev, crit_val = (
                            anderson_test.significance_level[i],
                            anderson_test.critical_values[i],
                        )
                        if sig_lev == sig_lvl:
                            if anderson_test.statistic < crit_val:
                                print(
                                    stats.ttest_rel(
                                        df[self.col_before], df[self.col_after]
                                    )
                                )
                            else:
                                print(
                                    stats.wilcoxon(
                                        df[self.col_before], df[self.col_after]
                                    )
                                )


## to do:
### liat persentase outliers
### tambahin fields untuk digunakan orang lain
