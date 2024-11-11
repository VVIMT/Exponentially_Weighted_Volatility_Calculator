#!/usr/bin/env python3

import pandas as pd
import argparse
import sys
import os
from utils.data_reader import read_historical_data
import mplfinance as mpf

def find_red_candles(data):
    # Filter red candles (close < open)
    red_candles = data[data['close'] < data['open']].copy()
    return red_candles

def calculate_differences(red_candles):
    # Calculate difference between close and low (price difference)
    red_candles['close_low_diff'] = red_candles['close'] - red_candles['low']
    # Calculate percentage difference between close and low
    red_candles['close_low_pct'] = (red_candles['close_low_diff'] / red_candles['close']) * 100

    # Calculate difference between high and low (price difference)
    red_candles['high_low_diff'] = red_candles['high'] - red_candles['low']
    # Calculate percentage difference between high and low
    red_candles['high_low_pct'] = (red_candles['high_low_diff'] / red_candles['low']) * 100

    return red_candles

def get_top_candles(red_candles, top_n):
    # Get top N red candles with largest close-low difference
    top_close_low_diff = red_candles.nlargest(top_n, 'close_low_diff')
    # Get top N red candles with largest high-low difference
    top_high_low_diff = red_candles.nlargest(top_n, 'high_low_diff')
    return top_close_low_diff, top_high_low_diff

def plot_candles(top_candles, diff_type, symbol):
    # Prepare data for mplfinance
    top_candles = top_candles.copy()
    top_candles = top_candles[['open', 'high', 'low', 'close']]
    # Ensure the index is datetime
    top_candles.index = pd.to_datetime(top_candles.index)
    
    title = ""
    if diff_type == 'close_low_diff':
        title = f"Top Candles with Largest (Close - Low) Difference for {symbol}"
    elif diff_type == 'high_low_diff':
        title = f"Top Candles with Largest (High - Low) Difference for {symbol}"

    # Plot using mplfinance without the mav parameter
    mpf.plot(top_candles, type='candle', style='charles', title=title, volume=False)

def main():
    parser = argparse.ArgumentParser(description='Find and plot candlesticks with largest differences among red candles.')
    parser.add_argument('--data_folder', type=str, default='data', help='Path to the data folder containing CSV files.')
    parser.add_argument('--symbol', type=str, required=True, help='Symbol to analyze (e.g., BTCUSDT).')
    parser.add_argument('--top_n', type=int, default=100, help='Number of top candles to find (default: 100).')
    args = parser.parse_args()

    data_folder = args.data_folder
    symbol = args.symbol
    top_n = args.top_n

    # Read the data
    data = read_historical_data(symbol, data_folder)
    if data is None or data.empty:
        print(f"No data available for symbol '{symbol}'.")
        sys.exit(1)

    # Ensure necessary columns are present
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in data.columns:
            print(f"Column '{col}' not found in data for symbol '{symbol}'.")
            sys.exit(1)

    # Convert columns to numeric
    data[required_columns] = data[required_columns].apply(pd.to_numeric, errors='coerce')
    data = data.dropna(subset=required_columns)
    if data.empty:
        print(f"No valid OHLC data available for symbol '{symbol}'.")
        sys.exit(1)

    # Find red candles
    red_candles = find_red_candles(data)
    if red_candles.empty:
        print("No red candles found in data.")
        sys.exit(1)

    # Calculate differences
    red_candles = calculate_differences(red_candles)

    # Get top candles
    top_close_low_diff, top_high_low_diff = get_top_candles(red_candles, top_n)

    # Print the results
    pd.set_option('display.float_format', '{:.2f}'.format)  # Format float numbers
    print(f"Top {top_n} red candles with largest (Close - Low) difference:")
    print(top_close_low_diff[['open', 'high', 'low', 'close', 'close_low_diff', 'close_low_pct']])

    print(f"\nTop {top_n} red candles with largest (High - Low) difference:")
    print(top_high_low_diff[['open', 'high', 'low', 'close', 'high_low_diff', 'high_low_pct']])

    # Plotting
    plot_candles(top_close_low_diff, 'close_low_diff', symbol)
    plot_candles(top_high_low_diff, 'high_low_diff', symbol)

if __name__ == "__main__":
    main()
