# Exponentially Weighted Volatility Calculator

This repository contains a Python script that calculates the average exponentially weighted volatility of individual assets and a combined portfolio over a specified observation window and timestamp granularity. The script is user-friendly, allowing you to pass parameters from the command line.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Data Preparation](#data-preparation)
- [Usage](#usage)
- [Parameters](#parameters)
- [Example](#example)
- [Output](#output)
- [Notes](#notes)
- [License](#license)

## Features

- **User-Friendly Command-Line Interface**: Easily pass parameters such as data folder path, assets list, observation window, and timestamp granularity.
- **CSV File Handling**: Reads multiple CSV files from a specified data folder, supporting files with headers and initial non-data lines.
- **Volatility Calculations**: Computes each asset's average exponentially weighted volatility and compares it with the combined assets' average exponentially weighted volatility.
- **Timestamps Matching and Verification**: Ensures data covers the observation window and aligns timestamps when combining data.
- **Efficient Computations**: Utilizes NumPy and pandas for optimized data manipulation and calculations.
- **Python 3.12 Compatibility**: Fully compatible with Python 3.12.

## Requirements

- Python 3.12
- pandas
- numpy
- colorama

Install the required Python packages using:

```bash
pip install pandas numpy colorama
```

## Installation

1. **Clone the Repository**

   ```bash
   git clone git@github.com:VVIMT/Exponentially_Weighted_Volatility_Calculator.git
   cd volatility-calculator
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *Note: Ensure you have Python 3.12 installed.*

## Data Preparation

Ensure you have historical data CSV files for the assets you want to analyze. The CSV files should be placed in a folder (default is `data/`) and named with the asset symbol (e.g., `BTCUSDT.csv`).

### CSV File Format

Your CSV files should have the following structure:

- The **first line** can be a URL or any non-data text (the script skips this line).
- The **second line** contains headers:

  ```
  unix,date,symbol,open,high,low,close,Volume BTC,Volume USDT,tradecount
  ```

- **Data columns**:

  - `unix`: Unix timestamp in milliseconds.
  - `date`: Human-readable date and time.
  - `symbol`: Asset symbol (e.g., `BTC/USDT`).
  - `open`, `high`, `low`, `close`: OHLC data.
  - `Volume BTC`, `Volume USDT`: Trading volume.
  - `tradecount`: Number of trades.

### Sample CSV Entry

```
1609459140000,2020-12-31 23:59:00,BTC/USDT,28923.66000000,28952.28000000,28903.86000000,28923.63000000,51.89534300,1501320.57892362,860
```

## Usage

Run the script from the command line, passing the required parameters:

```bash
python volatility_calculator.py --data_folder path_to_data_folder --assets asset_list --observation_window_minutes window_size --span ewm_span --timestamp_granularity granularity
```

### Minimal Example

```bash
python volatility_calculator.py --assets BTCUSDT,ETHUSDT,SOLUSDT
```

## Parameters

- `--data_folder`: (Optional) Path to the folder containing your CSV files. Default is `'data'`.
- `--assets`: (Required) Comma-separated list of asset symbols corresponding to the CSV filenames without the `.csv` extension (e.g., `BTCUSDT,ETHUSDT,SOLUSDT`).
- `--observation_window_minutes`: (Optional) Observation window in minutes. Default is `525600` minutes (1 year).
- `--span`: (Optional) Span parameter for the Exponentially Weighted Moving (EWM) calculations. Default is `20`.
- `--timestamp_granularity`: (Optional) Resampling frequency for timestamps. Default is `'1min'`. Accepts any pandas offset alias (e.g., `'5min'`, `'1H'`).

## Example

Calculate the average exponentially weighted volatility for BTCUSDT, ETHUSDT, and SOLUSDT over the past year with 1-minute granularity:

```bash
python volatility_calculator.py --data_folder data --assets BTCUSDT,ETHUSDT,SOLUSDT --observation_window_minutes 525600 --span 20 --timestamp_granularity 1min
```

## Output

The script outputs the average exponentially weighted volatility for each asset and the combined portfolio, sorted from lowest to highest volatility. The portfolio is equally weighted across all specified assets.

**Sample Output:**

```
Average Exponentially Weighted Volatility of SOLUSDT: 0.0256
Average Exponentially Weighted Volatility of ETHUSDT: 0.0312
Average Exponentially Weighted Volatility of BTCUSDT: 0.0354
Average Exponentially Weighted Volatility of Portfolio: 0.0307
```

*Note: The values above are illustrative.*

## Notes

- **Data Coverage Verification**: The script checks if each asset has data within the observation window. Assets without sufficient data are skipped.
- **Timestamp Alignment**: Resamples each asset's data to ensure consistent timestamps across assets.
- **Error Handling**: Includes error handling for file reading and data processing, allowing the script to continue even if some assets encounter issues.
- **Equal Weighting**: The combined portfolio assumes equal weighting of the specified assets.
- **Dependencies**: Ensure all required Python packages are installed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Disclaimer**: This script is intended for educational and informational purposes only. It should not be used as financial advice. Always conduct your own research or consult a professional when making investment decisions.
