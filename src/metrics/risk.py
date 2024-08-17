from base import Metric
import pandas as pd


class RewardToRiskRatio(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        total_profit = df[df['P/L'] > 0]['P/L'].sum()
        total_loss = abs(df[df['P/L'] < 0]['P/L'].sum())
        return total_profit / total_loss if total_loss != 0 else float('inf')

class MaxDrawdown(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        cumulative = df['P/L'].cumsum()
        running_max = cumulative.cummax()
        drawdown = running_max - cumulative
        return drawdown.max()
    