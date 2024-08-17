import pandas as pd
from typing import List
from data.loader import DataLoader
from data.processor import DataProcessor
from analysis.calculator import MetricsCalculator
import os


class BacktestAnalyzer:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        self.all_data = pd.DataFrame()
        self.metrics_calculator = MetricsCalculator()

    def load_and_process_data(self):
        for file_path in self.file_paths:
            file_name = os.path.basename(file_path)
            strategy_type, stop_loss = DataLoader.extract_details(file_name)
            df = DataLoader.load_csv(file_path)
            df['Strategy Type'] = strategy_type
            df['Stop Loss %'] = stop_loss
            self.all_data = pd.concat([self.all_data, df], ignore_index=True)

    def get_optimal_stop_loss_by_day(self, df: pd.DataFrame) -> pd.DataFrame:
        grouped = df.groupby(['Day of Week', 'Stop Loss %'])

        metrics = []
        for (day, stop_loss), group in grouped:
            group_metrics = self.metrics_calculator.calculate_metrics(group)
            group_metrics.update({
                'Day of Week': day,
                'Stop Loss %': stop_loss,
                'Win %': (len(group[group['P/L'] > 0]) / len(group)) * 100 if len(group) > 0 else 0
            })
            metrics.append(group_metrics)

        metrics_df = pd.DataFrame(metrics)
        optimal_stop_loss = metrics_df.loc[metrics_df.groupby('Day of Week')['Avg Profit on Winning Trades'].idxmax()]
        return optimal_stop_loss

    def analyze(self, x: int, exclude_days: List[str] = None, exclude_stoploss: List[str] = None) -> pd.DataFrame:
        last_x_days_data = DataProcessor.filter_last_x_days(self.all_data, x)
        filtered_data = DataProcessor.exclude_days_or_stoploss(last_x_days_data, exclude_days, exclude_stoploss)
        return self.get_optimal_stop_loss_by_day(filtered_data)

    def generate_pivot_table(self) -> pd.DataFrame:
        grouped_data = self.all_data.groupby(['Strategy Type', 'Stop Loss %', 'Day of Week'])['P/L'].mean().reset_index()
        pivot_table = grouped_data.pivot_table(values='P/L', index='Day of Week', columns='Stop Loss %', aggfunc='mean')
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        pivot_table = pivot_table.reindex(days_order)
        pivot_table.fillna(0, inplace=True)
        pivot_table['Best Stop Loss %'] = pivot_table.idxmax(axis=1)
        return pivot_table
    