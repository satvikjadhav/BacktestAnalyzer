from analysis.analyzer import BacktestAnalyzer

def main():
    file_paths = [
        'data/report/banknifty_atm_920_320_10p.csv',
        'data/report/banknifty_atm_920_320_20p.csv',
        'data/report/banknifty_atm_920_320_30p.csv',
        'data/report/banknifty_atm_920_320_40p.csv',
        'data/report/banknifty_atm_920_320_50p.csv',
    ]

    analyzer = BacktestAnalyzer(file_paths)
    analyzer.load_and_process_data()

    # # Example usage
    # x = 365
    # exclude_days = []
    # exclude_stoploss = []

    # optimal_stop_loss_df = analyzer.analyze(x, exclude_days, exclude_stoploss)
    # print("Optimal Stop Loss by Day:")
    # print(optimal_stop_loss_df)

    # pivot_table = analyzer.generate_pivot_table()
    # print("\nPivot Table:")
    # print(pivot_table)

    # Generate summary for last 365 days
    # summary_365 = analyzer.generate_summary(365, '10p')
    # print("\nSummary of last 365 days:")
    # print(summary_365)

    # Optimize for profit in last 365 days
    # optimization_result_win = analyzer.optimize(365)
    # print("\nOptimized Setup for Profit in Last 365 Days:")
    # print(optimization_result_win)

if __name__ == "__main__":
    main()
    