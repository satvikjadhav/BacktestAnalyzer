from metrics.base import Metric
import pandas as pd



class TotalProfit(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        return df['P/L'].sum()

    def is_higher_better(self) -> bool:
        return True

class WinPercentage(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        if df.empty:
            return 0.0
        winning_trades = df[df['P/L'] > 0]
        return (len(winning_trades) / len(df)) * 100

    def is_higher_better(self) -> bool:
        return True

class AverageProfitOnWinningTrades(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        winning_trades = df[df['P/L'] > 0]
        if winning_trades.empty:
            return 0.0
        return winning_trades['P/L'].mean()

    def is_higher_better(self) -> bool:
        return True

class AverageLossOnLosingTrades(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        losing_trades = df[df['P/L'] < 0]
        if losing_trades.empty:
            return 0.0
        return losing_trades['P/L'].mean()

    def is_higher_better(self) -> bool:
        return False  # For losses, a higher (less negative) number is better

class MaxProfitInSingleTrade(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        return df['P/L'].max()

    def is_higher_better(self) -> bool:
        return True
    
class MaxLossInSingleTrade(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        return df['P/L'].min()

    def is_higher_better(self) -> bool:
        return False
    