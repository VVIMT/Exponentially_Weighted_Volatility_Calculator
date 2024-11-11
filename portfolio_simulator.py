import pandas as pd
import numpy as np
import os
import argparse
from colorama import init, Fore, Style
from utils.data_reader import read_historical_data

# Initialize colorama
init(autoreset=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Backtest Portfolio Trading with Multiple Rebalancing Periods')
    parser.add_argument('--data_folder', type=str, default='data', help='Folder containing CSV files')
    parser.add_argument('--assets', type=str, required=True, help='Comma-separated list of assets (e.g., BTCUSDT,ETHUSDT)')
    parser.add_argument('--start_date', type=str, required=True, help='Start date for the simulation in YYYY-MM-DD format')
    parser.add_argument('--end_date', type=str, required=True, help='End date for the simulation in YYYY-MM-DD format')
    parser.add_argument('--rebalance_periods', type=str, required=True, help='Comma-separated list of rebalancing periods (e.g., 1D,1H,15min)')
    parser.add_argument('--trading_fee', type=float, default=0.001, help='Trading fee per transaction (e.g., 0.001 for 0.1%)')
    parser.add_argument('--initial_capital', type=float, default=100000, help='Initial capital for the simulation')
    parser.add_argument('--timestamp_granularity', type=str, default='1min', help='Timestamp granularity (default: 1min)')
    args = parser.parse_args()
    return args

def simulate_trading(price_df, symbols, rebalance_period, trading_fee, initial_capital, rebalance=False, verbose=True):
    if rebalance:
        # Generate rebalancing dates
        rebalancing_dates = pd.date_range(
            start=price_df.index.min(), end=price_df.index.max(), freq=rebalance_period
        )
        rebalancing_dates = rebalancing_dates.intersection(price_df.index)
    else:
        rebalancing_dates = []

    # Include initial date for initial allocation
    initial_date = price_df.index[0]
    rebalancing_dates = [initial_date] + list(rebalancing_dates)

    # Initialize portfolio
    holdings = {symbol: 0 for symbol in symbols}
    cash = initial_capital
    portfolio_history = []
    # Initialize trade counters and total fees
    trade_counts = {symbol: {'buy': 0, 'sell': 0} for symbol in symbols}
    total_fees_paid = 0.0

    for current_date in price_df.index:
        current_prices = price_df.loc[current_date]

        # Rebalance on specified dates
        if current_date in rebalancing_dates:
            # Calculate total portfolio value
            total_portfolio_value = cash + sum(
                holdings[symbol] * current_prices[symbol] for symbol in symbols
            )
            # Desired allocation per asset
            desired_value_per_asset = total_portfolio_value / len(symbols)

            # Rebalance holdings
            for symbol in symbols:
                current_price = current_prices[symbol]
                if pd.isna(current_price) or current_price == 0:
                    if verbose:
                        print(Fore.YELLOW + f"Invalid price for {symbol} on {current_date}, skipping.")
                    continue

                current_value = holdings[symbol] * current_price
                delta_value = desired_value_per_asset - current_value
                delta_shares = delta_value / current_price

                if abs(delta_value) < 0.01:
                    # Ignore trivial adjustments
                    continue

                transaction_amount = delta_shares * current_price
                fee = abs(transaction_amount) * trading_fee

                if delta_shares > 0:
                    # Buy asset
                    total_cost = transaction_amount + fee
                    cash -= total_cost
                    holdings[symbol] += delta_shares
                    trade_counts[symbol]['buy'] += 1
                    total_fees_paid += fee
                else:
                    # Sell asset
                    total_revenue = -transaction_amount - fee
                    cash += total_revenue
                    holdings[symbol] += delta_shares
                    trade_counts[symbol]['sell'] += 1
                    total_fees_paid += fee

            # Record initial allocation
            if current_date == initial_date and verbose:
                total_value = cash + sum(holdings[symbol] * current_prices[symbol] for symbol in symbols)
                initial_alloc_percent = {
                    symbol: (holdings[symbol] * current_prices[symbol] / total_value) * 100 for symbol in symbols
                }
                print(Fore.BLUE + f"Initial Allocation on {current_date.date()}:")
                for symbol, percent in initial_alloc_percent.items():
                    print(f"{symbol}: {percent:.2f}%")

        # Update portfolio history
        total_value = cash + sum(holdings[symbol] * current_prices[symbol] for symbol in symbols)
        portfolio_history.append({'date': current_date, 'total_value': total_value})

    # Record final allocation
    final_prices = price_df.iloc[-1]
    total_value = cash + sum(holdings[symbol] * final_prices[symbol] for symbol in symbols)
    final_alloc_percent = {
        symbol: (holdings[symbol] * final_prices[symbol] / total_value) * 100 for symbol in symbols
    }
    if verbose:
        print(Fore.BLUE + f"Final Allocation on {price_df.index[-1].date()}:")
        for symbol, percent in final_alloc_percent.items():
            print(f"{symbol}: {percent:.2f}%")

    # Create DataFrame from portfolio history
    portfolio_df = pd.DataFrame(portfolio_history)
    portfolio_df.set_index('date', inplace=True)

    # Calculate performance metrics
    initial_total_value = portfolio_df['total_value'].iloc[0]
    final_total_value = portfolio_df['total_value'].iloc[-1]
    total_return = (final_total_value / initial_total_value - 1) * 100

    return portfolio_df, initial_total_value, final_total_value, total_return, trade_counts, total_fees_paid

def calculate_individual_asset_performance(price_df, initial_capital, trading_fee):
    performance_results = []
    initial_prices = price_df.iloc[0]
    final_prices = price_df.iloc[-1]

    for symbol in price_df.columns:
        initial_price = initial_prices[symbol]
        final_price = final_prices[symbol]

        # Calculate total return for buy and hold strategy
        total_return = (final_price / initial_price - 1) * 100

        # Calculate the final value if initial capital was invested entirely in this asset
        final_value = initial_capital * (final_price / initial_price)
        # Subtract trading fees (assumed to be incurred on both buy and sell)
        total_fees = initial_capital * trading_fee + final_value * trading_fee
        final_value -= total_fees

        performance_results.append({
            'Asset': symbol,
            'Initial Price': initial_price,
            'Final Price': final_price,
            'Total Return (%)': total_return,
            'Final Value': final_value
        })

    # Convert to DataFrame
    performance_df = pd.DataFrame(performance_results)
    return performance_df

def main():
    args = parse_arguments()
    data_folder = args.data_folder
    symbols = [asset.strip() for asset in args.assets.split(',')]
    start_date = pd.to_datetime(args.start_date)
    end_date = pd.to_datetime(args.end_date)
    rebalance_periods = [period.strip() for period in args.rebalance_periods.split(',')]
    trading_fee = args.trading_fee
    initial_capital = args.initial_capital
    timestamp_granularity = args.timestamp_granularity

    price_data = {}
    # Load data for each asset
    for symbol in symbols:
        data = read_historical_data(symbol, data_folder)
        if data is None or data.empty:
            print(Fore.RED + f"No data for {symbol}. Exiting simulation.")
            return
        # Filter data within the simulation period
        data = data[(data.index >= start_date) & (data.index <= end_date)]
        if data.empty:
            print(Fore.RED + f"No data for {symbol} within the simulation period ({start_date.date()} to {end_date.date()}). Exiting simulation.")
            return
        # Check if data covers the entire simulation period
        data_start = data.index.min()
        data_end = data.index.max()
        if data_start > start_date or data_end < end_date:
            print(Fore.RED + f"Data for {symbol} does not fully cover the simulation period.")
            print(Fore.YELLOW + f"Data starts on {data_start.date()} and ends on {data_end.date()}.")
            return
        # Resample data to the desired timestamp granularity
        data = data.resample(timestamp_granularity).last().ffill()
        price_data[symbol] = data['close']
        print(Fore.GREEN + f"Loaded {symbol} data from {data_start.date()} to {data_end.date()}.")

    # Align all dataframes on the same timestamps
    price_df = pd.DataFrame(price_data)
    price_df.dropna(inplace=True)
    if price_df.empty:
        print(Fore.RED + "No overlapping timestamps across assets. Exiting simulation.")
        return

    # Prepare to store results for each rebalancing period
    results = []

    # Simulations with rebalancing
    for rebalance_period in rebalance_periods:
        print(Fore.CYAN + f"\nSimulating Rebalancing Period: {rebalance_period}")
        portfolio_df, initial_val, final_val, total_ret, trade_counts, total_fees = simulate_trading(
            price_df=price_df,
            symbols=symbols,
            rebalance_period=rebalance_period,
            trading_fee=trading_fee,
            initial_capital=initial_capital,
            rebalance=True
        )
        total_trades = sum([sum(tc.values()) for tc in trade_counts.values()])
        results.append({
            'Simulation Type': f"Rebalance {rebalance_period}",
            'Initial Value': initial_val,
            'Final Value': final_val,
            'Total Return (%)': total_ret,
            'Total Trades': total_trades,
            'Total Fees Paid': total_fees
        })
        print(Fore.GREEN + f"Rebalance Period: {rebalance_period}")
        print(f"Initial Portfolio Value: ${initial_val:,.2f}")
        print(f"Final Portfolio Value:   ${final_val:,.2f}")
        print(f"Total Return:            {total_ret:.2f}%")
        print(f"Total Trades Executed:   {total_trades}")
        print(f"Total Fees Paid:         ${total_fees:,.2f}\n")

    # Simulation with no rebalancing
    print(Fore.CYAN + "\nSimulating No Rebalancing Scenario")
    portfolio_df_no_rebalance, initial_val_nr, final_val_nr, total_ret_nr, trade_counts_nr, total_fees_nr = simulate_trading(
        price_df=price_df,
        symbols=symbols,
        rebalance_period=None,  # Not used in simulate_trading when rebalance=False
        trading_fee=trading_fee,
        initial_capital=initial_capital,
        rebalance=False
    )
    total_trades_nr = sum([sum(tc.values()) for tc in trade_counts_nr.values()])
    results.append({
        'Simulation Type': "No Rebalancing",
        'Initial Value': initial_val_nr,
        'Final Value': final_val_nr,
        'Total Return (%)': total_ret_nr,
        'Total Trades': total_trades_nr,
        'Total Fees Paid': total_fees_nr
    })
    print(Fore.GREEN + "No Rebalancing Simulation")
    print(f"Initial Portfolio Value: ${initial_val_nr:,.2f}")
    print(f"Final Portfolio Value:   ${final_val_nr:,.2f}")
    print(f"Total Return:            {total_ret_nr:.2f}%")
    print(f"Total Trades Executed:   {total_trades_nr}")
    print(f"Total Fees Paid:         ${total_fees_nr:,.2f}\n")

    # Calculate individual asset performance
    print(Fore.MAGENTA + "\n=== Individual Asset Performance ===")
    # Pass trading_fee to the function
    individual_performance_df = calculate_individual_asset_performance(price_df, initial_capital, trading_fee)
    # Merge individual asset performance into results
    for index, row in individual_performance_df.iterrows():
        total_fees_asset = initial_capital * trading_fee + row['Final Value'] * trading_fee
        results.append({
            'Simulation Type': f"Asset {row['Asset']}",
            'Initial Value': initial_capital,
            'Final Value': row['Final Value'],
            'Total Return (%)': row['Total Return (%)'],
            'Total Trades': 2,  # One buy and one sell
            'Total Fees Paid': total_fees_asset
        })
    # Display individual performance
    print(individual_performance_df[['Asset', 'Initial Price', 'Final Price', 'Total Return (%)', 'Final Value']].to_string(index=False))

    # Create a summary DataFrame
    summary_df = pd.DataFrame(results)
    summary_df = summary_df.sort_values(by='Total Return (%)', ascending=False)
    print(Fore.MAGENTA + "\n=== Simulation Summary ===")
    print(summary_df[['Simulation Type', 'Initial Value', 'Final Value', 'Total Return (%)', 'Total Trades', 'Total Fees Paid']].to_string(index=False))

    # Optionally, plot the portfolio values for each simulation
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(14, 7))
        # Plot portfolio simulations
        for result in results:
            simulation_type = result['Simulation Type']
            if simulation_type.startswith("Rebalance") or simulation_type == "No Rebalancing":
                # Re-simulate to get portfolio history for plotting
                if simulation_type.startswith("Rebalance"):
                    rebalance_period = simulation_type.split("Rebalance ")[1]
                    portfolio_df_plot, _, _, _, _, _ = simulate_trading(
                        price_df=price_df,
                        symbols=symbols,
                        rebalance_period=rebalance_period,
                        trading_fee=trading_fee,
                        initial_capital=initial_capital,
                        rebalance=True,
                        verbose=False  # Suppress output during plotting
                    )
                elif simulation_type == "No Rebalancing":
                    portfolio_df_plot, _, _, _, _, _ = simulate_trading(
                        price_df=price_df,
                        symbols=symbols,
                        rebalance_period=None,
                        trading_fee=trading_fee,
                        initial_capital=initial_capital,
                        rebalance=False,
                        verbose=False  # Suppress output during plotting
                    )
                plt.plot(portfolio_df_plot.index, portfolio_df_plot['total_value'], label=simulation_type)
        # Plot individual asset performances
        for symbol in symbols:
            asset_values = (price_df[symbol] / price_df[symbol].iloc[0]) * initial_capital
            # Subtract trading fees (assumed on buy and sell)
            total_fees = initial_capital * trading_fee + asset_values * trading_fee
            asset_values -= total_fees
            plt.plot(price_df.index, asset_values, label=f"Asset {symbol}")
        plt.title('Portfolio and Individual Asset Values Over Time')
        plt.xlabel('Date')
        plt.ylabel('Value ($)')
        plt.legend(title='Simulation Type', loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except ImportError:
        print(Fore.YELLOW + "Matplotlib not installed. Install it to see the portfolio value plots.")

if __name__ == "__main__":
    main()
