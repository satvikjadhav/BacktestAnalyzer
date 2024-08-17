from metrics.base import Metric
import pandas as pd



class AverageProfitOnWinningTrades(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        return df[df['P/L'] > 0]['P/L'].mean()

class AverageLossOnLosingTrades(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        return df[df['P/L'] < 0]['P/L'].mean()

class MaxProfitInSingleTrade(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        return df['P/L'].max()

class MaxLossInSingleTrade(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        return df['P/L'].min()
    