from typing import Dict
import pandas as pd
from metrics.base import Metric
from metrics.profit_loss import AverageProfitOnWinningTrades, AverageLossOnLosingTrades, MaxProfitInSingleTrade, MaxLossInSingleTrade
from metrics.risk import RewardToRiskRatio, MaxDrawdown


class MetricsCalculator:
    def __init__(self):
        self.metrics: Dict[str, Metric] = {
            'Avg Profit on Winning Trades': AverageProfitOnWinningTrades(),
            'Avg Loss on Losing Trades': AverageLossOnLosingTrades(),
            'Max Profit in Single Trade': MaxProfitInSingleTrade(),
            'Max Loss in Single Trade': MaxLossInSingleTrade(),
            'Reward to Risk Ratio': RewardToRiskRatio(),
            'Max Drawdown': MaxDrawdown()
        }

    def calculate_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        return {name: metric.calculate(df) for name, metric in self.metrics.items()}

    def add_metric(self, name: str, metric: Metric):
        self.metrics[name] = metric
