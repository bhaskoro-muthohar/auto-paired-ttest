# Auto Paired Test

This module automates the inferential statistical testing of paired samples. It handles data validation, visualization, normality testing, and automatic test selection based on data characteristics.

## Installation

```bash
pip install auto-paired-test
```

## Usage

### Basic Usage

```python
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
```

### Advanced Features

The package automatically:
- Validates input data (checks for missing columns and non-numeric data)
- Performs normality testing using Anderson-Darling test
- Removes outliers when needed for better statistical validity
- Selects the appropriate test (paired t-test or Wilcoxon signed-rank test)
- Provides detailed outlier statistics

```python
# Specify significance level for normality test (1, 2, 5, 10, or 15)
result = test.run_test(sig_lvl=5)  # 5% significance level

# Get statistics about outliers
outlier_stats = test.get_outlier_stats()
print(f"Outliers removed: {outlier_stats['outliers_removed']}")
print(f"Original sample size: {outlier_stats['original_sample_size']}")
print(f"Final sample size: {outlier_stats['final_sample_size']}")

if outlier_stats['outliers_removed']:
    print(f"Outlier count: {outlier_stats['outlier_count']}")
    print(f"Outlier percentage: {outlier_stats['outlier_percentage']:.2f}%")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)