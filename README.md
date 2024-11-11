
# **Crypto Trading Tools**

This repository contains Python scripts for analyzing and simulating cryptocurrency trading strategies. The tools provided are:

1. **Exponentially Weighted Volatility Calculator**: Calculates the average exponentially weighted volatility of individual assets and a combined portfolio over a specified observation window and timestamp granularity.

2. **Portfolio Simulator**: Simulates portfolio trading strategies with multiple rebalancing periods, allowing you to backtest different rebalancing frequencies and compare performance metrics.

## **Table of Contents**

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Data Preparation](#data-preparation)
- [Sample CSV Structure](#sample-csv-structure)
- [Scripts](#scripts)
  - [Exponentially Weighted Volatility Calculator](#exponentially-weighted-volatility-calculator)
    - [Usage](#usage-volatility-calculator)
    - [Parameters](#parameters-volatility-calculator)
    - [Example](#example-volatility-calculator)
    - [Output](#output-volatility-calculator)
  - [Portfolio Simulator](#portfolio-simulator)
    - [Usage](#usage-portfolio-simulator)
    - [Command-Line Arguments](#command-line-arguments-portfolio-simulator)
    - [Example Command](#example-command-portfolio-simulator)
    - [Output Explanation](#output-explanation-portfolio-simulator)
- [Notes](#notes)
- [License](#license)

---

## **Features**

### **Exponentially Weighted Volatility Calculator**

- **User-Friendly Command-Line Interface**: Easily pass parameters such as data folder path, assets list, observation window, and timestamp granularity.
- **CSV File Handling**: Reads multiple CSV files from a specified data folder.
- **Volatility Calculations**: Computes each asset's average exponentially weighted volatility and compares it with the combined assets' average exponentially weighted volatility.
- **Timestamps Matching and Verification**: Ensures data covers the observation window and aligns timestamps when combining data.
- **Efficient Computations**: Utilizes NumPy and pandas for optimized data manipulation and calculations.
- **Python 3.6+ Compatibility**: Fully compatible with Python 3.6 and higher versions.

### **Portfolio Simulator**

- **Simulate Portfolio Strategies**: Backtest portfolio performance with different rebalancing periods (e.g., daily, weekly, monthly).
- **Multiple Assets Support**: Simulate trading across multiple assets with customizable initial capital and trading fees.
- **Performance Metrics**: Tracks and reports initial and final portfolio values, total return percentage, number of trades executed, and total fees paid.
- **Individual Asset Performance Comparison**: Provides performance metrics for individual assets for comparison.
- **Visualization**: Generates plots of portfolio and individual asset values over time.

---

## **Requirements**

- **Python**: Version 3.6 or higher.
- **Packages**:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `colorama`
  - `argparse`

Install the required packages using:

```bash
pip install pandas numpy matplotlib colorama argparse
```

---

## **Installation**

1. **Clone the Repository**

   ```bash
    git clone git@github.com:VVIMT/Exponentially_Weighted_Volatility_Calculator.git
    cd Exponentially_Weighted_Volatility_Calculator
   ```

2. **Ensure the Directory Structure**

   Your project directory should look like this:

   ```
   .
   ├── volatility_calculator.py
   ├── portfolio_simulator.py
   ├── data
   │   ├── Binance_BTCUSDT_2024_minute.csv
   │   ├── Binance_ETHUSDT_2024_minute.csv
   │   ├── Binance_SOLUSDT_2024_minute.csv
   │   ├── Binance_XRPUSDT_2024_minute.csv
   │   └── ... (other CSV data files)
   ```

3. **Prepare Data Files**

   - Place all your CSV data files in the `data` folder.
   - Ensure that the CSV files are named appropriately, e.g., `Binance_BTCUSDT_2024_minute.csv`.

---

## **Data Preparation**

Both the `volatility_calculator.py` and `portfolio_simulator.py` scripts use the same CSV files located in the `data` directory. There is no need for separate data preparation for each script.

Ensure that each asset's CSV file contains historical price data with the required columns.

---

## **Sample CSV Structure**

Below is a sample of the first few lines of a CSV file presented in ASCII table format:

| Unix          | Date                 | Symbol   | Open      | High      | Low       | Close     | Volume BTC | Volume USDT     | tradecount |
| ------------- | -------------------- | -------- | --------- | --------- | --------- | --------- | ---------- | --------------- | ---------- |
| 1730591940000 | 2024-11-02 23:59:00  | BTCUSDT  | 69327.99  | 69376.13  | 69316.00  | 69374.74  | 95.58074   | 6629738.5253384 | 1039       |
| 1730591880000 | 2024-11-02 23:58:00  | BTCUSDT  | 69296.00  | 69328.00  | 69286.92  | 69327.99  | 26.49626   | 1836430.7989713 | 1298       |
| 1730591820000 | 2024-11-02 23:57:00  | BTCUSDT  | 69300.01  | 69302.00  | 69296.00  | 69296.00  | 4.01482    | 278229.5453751  | 433        |
| 1730591760000 | 2024-11-02 23:56:00  | BTCUSDT  | 69306.01  | 69306.01  | 69300.00  | 69300.00  | 1.36238    | 94414.7744151   | 332        |
| ...           | ...                  | ...      | ...       | ...       | ...       | ...       | ...        | ...             | ...        |

**Explanation of the Columns**:

- **Unix**: Unix timestamp in milliseconds.
- **Date**: Corresponding human-readable date and time.
- **Symbol**: The trading pair symbol.
- **Open**: Opening price of the asset for the interval.
- **High**: Highest price of the asset during the interval.
- **Low**: Lowest price of the asset during the interval.
- **Close**: Closing price of the asset for the interval.
- **Volume BTC**: Volume traded in BTC during the interval.
- **Volume USDT**: Volume traded in USDT during the interval.
- **tradecount**: Number of trades executed during the interval.

---

## **Scripts**

### **Exponentially Weighted Volatility Calculator**

#### **Usage** <a name="usage-volatility-calculator"></a>

Run the script from the command line, passing the required parameters:

```bash
python volatility_calculator.py --data_folder path_to_data_folder --assets asset_list --observation_window_minutes window_size --span ewm_span --timestamp_granularity granularity
```

#### **Parameters** <a name="parameters-volatility-calculator"></a>

- `--data_folder`: (Optional) Path to the folder containing your CSV files. Default is `'data'`.
- `--assets`: (Required) Comma-separated list of asset symbols corresponding to the CSV filenames without the `.csv` extension (e.g., `Binance_BTCUSDT_2024_minute,Binance_ETHUSDT_2024_minute`).
- `--observation_window_minutes`: (Optional) Observation window in minutes (default: `525600` for 1 year).
- `--span`: (Optional) Span parameter for the Exponentially Weighted Moving (EWM) calculations (default: `20`).
- `--timestamp_granularity`: (Optional) Resampling frequency for timestamps (default: `'1min'`). Accepts any pandas offset alias (e.g., `'5min'`, `'1H'`).

#### **Example** <a name="example-volatility-calculator"></a>

Calculate the average exponentially weighted volatility for multiple assets over the past year with 1-minute granularity:

```bash
python volatility_calculator.py --data_folder data --assets Binance_BTCUSDT_2024_minute,Binance_ETHUSDT_2024_minute,Binance_SOLUSDT_2024_minute --observation_window_minutes 525600 --span 20 --timestamp_granularity 1min
```

#### **Output** <a name="output-volatility-calculator"></a>

The script outputs the average exponentially weighted volatility for each asset and the combined portfolio, sorted from lowest to highest volatility. The portfolio is equally weighted across all specified assets.

**Sample Output:**

```
Average Exponentially Weighted Volatility of SOLUSDT: 2.5600%
Average Exponentially Weighted Volatility of ETHUSDT: 3.1200%
Average Exponentially Weighted Volatility of BTCUSDT: 3.5400%
Average Exponentially Weighted Volatility of Portfolio: 3.0700%
```

*Note: The values above are illustrative.*

---

### **Portfolio Simulator**

#### **Usage** <a name="usage-portfolio-simulator"></a>

Run the script from the command line, passing the required parameters:

```bash
python portfolio_simulator.py \
    --data_folder data \
    --assets asset_list \
    --start_date YYYY-MM-DD \
    --end_date YYYY-MM-DD \
    --rebalance_periods period_list \
    --trading_fee fee_rate \
    --initial_capital amount \
    --timestamp_granularity granularity
```

#### **Command-Line Arguments** <a name="command-line-arguments-portfolio-simulator"></a>

- `--data_folder`: Folder containing CSV files with historical data (default: `data`).
- `--assets`: Comma-separated list of asset symbols corresponding to the CSV filenames without the `.csv` extension (e.g., `Binance_BTCUSDT_2024_minute,Binance_ETHUSDT_2024_minute`).
- `--start_date`: Start date for the simulation in `YYYY-MM-DD` format.
- `--end_date`: End date for the simulation in `YYYY-MM-DD` format.
- `--rebalance_periods`: Comma-separated list of rebalancing periods (e.g., `1D,1W,1M`).
- `--trading_fee`: Trading fee per transaction (e.g., `0.001` for 0.1%).
- `--initial_capital`: Initial capital for the simulation (default: `100000`).
- `--timestamp_granularity`: Timestamp granularity for resampling data (default: `1min`).

#### **Example Command** <a name="example-command-portfolio-simulator"></a>

```bash
python portfolio_simulator.py \
    --data_folder data \
    --assets Binance_BTCUSDT_2024_minute,Binance_ETHUSDT_2024_minute,Binance_SOLUSDT_2024_minute,Binance_XRPUSDT_2024_minute \
    --start_date 2024-01-01 \
    --end_date 2024-10-31 \
    --rebalance_periods 1D,1W,1M \
    --trading_fee 0.0002 \
    --initial_capital 100000 \
    --timestamp_granularity 1min
```

#### **Output Explanation** <a name="output-explanation-portfolio-simulator"></a>

After running the script, you will receive output similar to the following:

```plaintext
Loaded Binance_BTCUSDT_2024_minute data from 2024-01-01 to 2024-10-31.
...

Simulating Rebalancing Period: 1D
Initial Allocation on 2024-01-01:
Binance_BTCUSDT_2024_minute: 25.01%
...

Final Allocation on 2024-10-31:
Binance_BTCUSDT_2024_minute: 25.00%
...

Rebalance Period: 1D
Initial Portfolio Value: $99,980.00
Final Portfolio Value:   $137,333.92
Total Return:            37.36%
Total Trades Executed:   1220
Total Fees Paid:         $121.28

...
```

**Understanding the Output**

- **Initial and Final Allocations**: Shows the percentage of the portfolio allocated to each asset at the start and end of the simulation.
- **Rebalance Period**: Indicates the frequency of rebalancing in the simulation.
- **Portfolio Values**: Displays the initial and final portfolio values.
- **Total Return**: The percentage gain or loss over the simulation period.
- **Total Trades Executed**: The number of buy and sell trades executed during the simulation.
- **Total Fees Paid**: The cumulative trading fees paid during the simulation.
- **Individual Asset Performance**: Performance metrics if the entire initial capital was invested in a single asset.
- **Simulation Summary**: A comparative table of all simulations and individual asset performances.

---

## **Notes**

- **Data Coverage Verification**: Each script checks if each asset has data within the required period. Assets without sufficient data are skipped.
- **Timestamp Alignment**: Resamples each asset's data to ensure consistent timestamps across assets.
- **Error Handling**: Includes error handling for file reading and data processing, allowing the script to continue even if some assets encounter issues.
- **Equal Weighting**: Both scripts assume equal weighting of the specified assets unless otherwise adjusted.
- **Dependencies**: Ensure all required Python packages are installed.
- **Trading Fees**: Adjust the `--trading_fee` parameter in the portfolio simulator to match realistic trading conditions for your scenario.
- **Granularity**: The `--timestamp_granularity` should match the granularity of your data to avoid resampling issues.
- **Data Sources**: The sample CSV data provided is sourced from [CryptoDataDownload](https://www.cryptodatadownload.com). Ensure compliance with their terms of use when utilizing their data.
- **File Paths and Names**: Ensure that the asset symbols provided in the command-line arguments match the filenames in your `data` folder (without the `.csv` extension).

