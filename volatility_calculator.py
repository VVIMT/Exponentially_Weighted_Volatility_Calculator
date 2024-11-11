import pandas as pd
import numpy as np
import os
import sys
import argparse
from colorama import init, Fore, Style
from utils.data_reader import read_historical_data

# Initialize colorama
init(autoreset=True)

def calculate_returns(data):
    data['returns'] = np.log(data['close'] / data['close'].shift(1))
    return data

def calculate_exponentially_weighted_volatility(returns, span):
    ewm_volatility = returns.ewm(span=span, adjust=False).std()
    return ewm_volatility

def get_symbols_from_args(assets_arg):
    symbols = [asset.strip() for asset in assets_arg.split(',')]
    return symbols

def parse_arguments():
    parser = argparse.ArgumentParser(description='Compute Exponentially Weighted Volatility of Assets')
    parser.add_argument('--data_folder', type=str, default='data', help='Folder containing CSV files')
    parser.add_argument('--assets', type=str, required=True, help='Comma-separated list of assets (e.g., BTCUSDT,ETHUSDT)')
    parser.add_argument('--observation_window_minutes', type=int, default=525600, help='Observation window in minutes (default: 525600 for 1 year)')
    parser.add_argument('--span', type=int, default=20, help='Span parameter for EWM (default: 20)')
    parser.add_argument('--timestamp_granularity', type=str, default='1min', help='Timestamp granularity (default: 1min)')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    data_folder = args.data_folder
    symbols = get_symbols_from_args(args.assets)
    observation_window_minutes = args.observation_window_minutes
    observation_window = pd.Timedelta(minutes=observation_window_minutes)
    span = args.span
    timestamp_granularity = args.timestamp_granularity

    all_returns = []
    individual_volatilities = {}
    latest_timestamp = None

    # Determine the latest timestamp across all assets
    for symbol in symbols:
        try:
            data = read_historical_data(symbol, data_folder)
            if data is None or data.empty:
                print(f"No data for {symbol}.")
                continue
            symbol_latest_timestamp = data.index.max()
            if latest_timestamp is None or symbol_latest_timestamp < latest_timestamp:
                latest_timestamp = symbol_latest_timestamp
        except Exception as e:
            print(f"Error processing data for {symbol}: {e}")
            continue

    if latest_timestamp is None:
        print("No data available.")
        exit()

    # Define observation period
    end_time = latest_timestamp
    start_time = end_time - observation_window

    for symbol in symbols:
        try:
            data = read_historical_data(symbol, data_folder)
            if data is None or data.empty:
                print(f"No data for {symbol}.")
                continue
            # Filter data within the observation period
            data = data[(data.index >= start_time) & (data.index <= end_time)]
            if data.empty:
                print(f"No data for {symbol} within the observation window.")
                continue
            # Resample data to the desired timestamp granularity
            data = data.resample(timestamp_granularity).last()
            # Compute returns
            data = calculate_returns(data)
            returns = data['returns']
            # Compute exponentially weighted volatility
            ewm_volatility = calculate_exponentially_weighted_volatility(returns, span)
            # Compute average exponentially weighted volatility
            avg_ewm_volatility = ewm_volatility.mean()
            individual_volatilities[symbol] = avg_ewm_volatility
            # Keep returns for portfolio calculation
            all_returns.append(returns)
        except Exception as e:
            print(f"Error processing data for {symbol}: {e}")
            continue

    if not all_returns:
        print("No returns data available.")
        exit()

    # Combine returns into a DataFrame
    returns_df = pd.concat(all_returns, axis=1)
    returns_df.columns = [symbol for symbol in individual_volatilities.keys()]
    returns_df.dropna(inplace=True)

    # Ensure timestamps match
    if returns_df.empty:
        print("No overlapping timestamps across assets.")
        exit()

    # Compute portfolio returns (equal weighting)
    portfolio_returns = returns_df.mean(axis=1)
    # Compute exponentially weighted volatility of portfolio returns
    portfolio_ewm_volatility = calculate_exponentially_weighted_volatility(portfolio_returns, span)
    # Compute average exponentially weighted volatility of the portfolio
    portfolio_avg_volatility = portfolio_ewm_volatility.mean()
    # Add portfolio volatility to the dictionary
    individual_volatilities['Portfolio'] = portfolio_avg_volatility
    # Sort volatilities from lowest to highest
    sorted_volatilities = sorted(individual_volatilities.items(), key=lambda x: x[1])
    # Display the sorted volatilities in percentage
    for asset, vol in sorted_volatilities:
        vol_percentage = vol * 100  # Convert to percentage
        if asset == 'Portfolio':
            print(Fore.GREEN + f'Average Exponentially Weighted Volatility of {asset}: {vol_percentage:.4f}%')
        else:
            print(f'Average Exponentially Weighted Volatility of {asset}: {vol_percentage:.4f}%')

if __name__ == "__main__":
    main()
