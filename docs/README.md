# Backtest Analyzer

## Overview

This project is created as a basktesting tool for the csv outoput from [AlgoTest](https://algotest.in/). It's designed to analyze financial backtesting data, calculate various metrics, and provide insights into trading strategies.

## Features

- Modular design with separate classes for specific responsibilities
- Adherence to SOLID principles (Single Responsibility, Open/Closed, Dependency Inversion)
- Use of Abstract Base Classes for defining interfaces
- Type hinting for improved code readability and error catching
- Easily extensible for adding new metrics or analysis functions

## Project Structure

```
backtesting_analysis_tool/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   └── processor.py
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── profit_loss.py
│   │   └── risk.py
│   └── analysis/
│       ├── __init__.py
│       ├── analyzer.py
│       └── calculator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_data_processor.py
│   ├── test_metrics.py
│   └── test_analyzer.py
│
├── data/
│   └── report/
│       ├── banknifty_atm_920_320_10p.csv
│       ├── banknifty_atm_920_320_20p.csv
│       ├── banknifty_atm_920_320_30p.csv
│       ├── banknifty_atm_920_320_40p.csv
│       └── banknifty_atm_920_320_50p.csv
│
├── docs/
│   ├── README.md
│   └── CONTRIBUTING.md
│
├── requirements.txt
├── setup.py
└── .gitignore
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/satvikjadhav/BacktestAnalyzer.git
   cd backtest-analyzer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Prepare your input CSV file(s) according to the following format:

   The CSV file should contain the following columns:
   - Index: A unique identifier for each trade
   - Entry Date: The date of trade entry (format: DD-MM-YY)
   - Entry Time: The time of trade entry (format: H:MM:SS AM/PM)
   - Exit Date: The date of trade exit (format: DD-MM-YY)
   - Exit Time: The time of trade exit (format: H:MM:SS AM/PM)
   - Type: The option type (CE for Call, PE for Put)
   - Strike: The strike price of the option
   - B/S: Buy or Sell indicator
   - Qty: The quantity of contracts traded
   - Entry Price: The price at which the trade was entered
   - Exit Price: The price at which the trade was exited
   - Vix: The VIX index value (optional)
   - P/L: The profit/loss for the trade

   Example:
   ```
   Index,Entry Date,Entry Time,Exit Date,Exit Time,Type,Strike,B/S,Qty,Entry Price,Exit Price,Vix,P/L
   1,01-01-20, 9:20:00 AM,01-01-20, 3:20:00 PM,,,,,,,11.59,433.5
   1.1,01-01-20, 9:20:00 AM,01-01-20, 3:20:00 PM,CE,32500,Sell,15,62.45,11.4,,765.75
   1.2,01-01-20, 9:20:00 AM,01-01-20, 9:42:00 AM,PE,32500,Sell,15,221.4,243.55,,-332.25
   ```

   Note: Ensure that your CSV file is properly formatted and contains all the required columns.

2. Modify the `file_paths` in the `main()` function of `src/main.py` to point to your CSV file(s):
   ```python
   file_paths = ['path/to/your/input.csv']
   ```

3. Run the script:
   ```
   python src/main.py
   ```

4. The script will process the input data, calculate metrics, and output the results.

## Extending the Project

To add new functionality or analysis functions:

1. Create a new class that inherits from `Metric` for any new metric you want to add.
2. Add the new metric to the `MetricsCalculator` in its `__init__` method or use the `add_metric` method.
3. For entirely new types of analysis, add methods to the `BacktestAnalyzer` class or create new classes that use the `BacktestAnalyzer`.

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
