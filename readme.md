# Auto Paired Test

This module automates the inference statistic test of a paired sample.

## Installation

```bash
pip install auto-paired-test
```

## Usage

```python
from statlibs import AutoPairedTest
# ... (prepare your DataFrame)
AutoPairedTest(df, "diff", "before", "after").run_test()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)