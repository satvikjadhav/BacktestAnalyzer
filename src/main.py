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

    # Example usage
    x = 365
    exclude_days = []
    exclude_stoploss = []

    optimal_stop_loss_df = analyzer.analyze(x, exclude_days, exclude_stoploss)
    print("Optimal Stop Loss by Day:")
    print(optimal_stop_loss_df)

    pivot_table = analyzer.generate_pivot_table()
    print("\nPivot Table:")
    print(pivot_table)

if __name__ == "__main__":
    main()
    