import os
import pandas as pd

def read_historical_data(symbol, data_folder):
    file_path = os.path.join(data_folder, f"{symbol}.csv")
    try:
        # Read the CSV file, skipping the first line if it contains the URL
        with open(file_path, 'r') as f:
            first_line = f.readline()
            if 'CryptoDataDownload' in first_line:
                data = pd.read_csv(file_path, skiprows=1)
            else:
                data = pd.read_csv(file_path)
        # Standardize column names to lowercase
        data.columns = data.columns.str.lower()
        # Map the columns to standard names
        column_mapping = {
            'unix': 'unix',
            'date': 'date',
            'symbol': 'symbol',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'volume btc': 'volume',
            'volume usdt': 'volume_from',
            'volume_from': 'volume_from',
            'tradecount': 'tradecount'
        }
        data = data.rename(columns=column_mapping)
        # Check if 'unix' column exists
        if 'unix' not in data.columns:
            raise KeyError("'unix' column is missing after renaming.")
        # Convert 'unix' column to datetime
        data['timestamp'] = pd.to_datetime(data['unix'], unit='ms')
        # Set 'timestamp' as the index
        data.set_index('timestamp', inplace=True)
        # Sort the data by index
        data = data.sort_index()
        return data
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
