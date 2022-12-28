from src import AutoPairedTtest
import pandas as pd
import numpy as np

array_rand = np.random.randint(100, size=(5, 2))
array_rand_diff = np.subtract.reduce(array_rand, axis=1).reshape(-1, 1)
array = np.hstack((array_rand, array_rand_diff))
column = ["before", "after", "diff"]

df = pd.DataFrame(data=array, columns=column)


AutoPairedTtest(df, "diff", "before", "after").run_test()
