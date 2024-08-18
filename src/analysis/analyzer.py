import pandas as pd
from typing import List
from data.loader import DataLoader
from data.processor import DataProcessor
from analysis.calculator import MetricsCalculator
from analysis.optimizer import Optimizer
import os


class BacktestAnalyzer:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        self.all_data = pd.DataFrame()
        self.metrics_calculator = MetricsCalculator()
        self.optimizer = None
        self.total_days = None

    def load_and_process_data(self):
        for file_path in self.file_paths:
            file_name = os.path.basename(file_path)
            strategy_type, stop_loss = DataLoader.extract_details(file_name)
            df = DataLoader.load_csv(file_path)
            df['Strategy Type'] = strategy_type
            df['Stop Loss %'] = stop_loss
            self.all_data = pd.concat([self.all_data, df], ignore_index=True)

        self.optimizer = Optimizer(self.all_data)
        self.total_days = len(self.all_data["Entry Date"].unique())

    def get_optimal_stop_loss_by_metric(self, df: pd.DataFrame, metric_name: str = 'Total Profit') -> pd.DataFrame:
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
        # Get the optimal stop loss based on a user provided metric
        optimal_stop_loss = metrics_df.loc[metrics_df.groupby('Day of Week')[metric_name].idxmax()]
        return optimal_stop_loss

    def analyze(self, x: int, exclude_days: List[str] = None, exclude_stoploss: List[str] = None) -> pd.DataFrame:
        last_x_days_data = DataProcessor.filter_last_x_days(self.all_data, x)
        filtered_data = DataProcessor.exclude_days_or_stoploss(last_x_days_data, exclude_days, exclude_stoploss)
        return self.get_optimal_stop_loss_by_metric(filtered_data)

    def generate_pivot_table(self) -> pd.DataFrame:
        grouped_data = self.all_data.groupby(['Strategy Type', 'Stop Loss %', 'Day of Week'])['P/L'].mean().reset_index()
        pivot_table = grouped_data.pivot_table(values='P/L', index='Day of Week', columns='Stop Loss %', aggfunc='mean')
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        pivot_table = pivot_table.reindex(days_order)
        pivot_table.fillna(0, inplace=True)
        pivot_table['Best Stop Loss %'] = pivot_table.idxmax(axis=1)
        return pivot_table
    
    def optimize(self, x: int) -> pd.DataFrame:
        if self.optimizer is None:
            raise ValueError("Data has not been loaded. Call load_and_process_data() first.")
        return self.optimizer.get_optimal_setup_summary(x)
    
    def generate_summary(self, x: int = None, sl: str = None) -> pd.DataFrame:
        data = self.all_data if x is None else DataProcessor.filter_last_x_days(self.all_data, x)
        grouped = data.groupby(['Day of Week', 'Stop Loss %'])
        
        summary = []
        for (day, stop_loss), group in grouped:
            metrics = self.metrics_calculator.calculate_metrics(group)
            metrics['Day of Week'] = day
            metrics['Stop Loss %'] = stop_loss
            summary.append(metrics)
        
        summary = summary if sl is None else [entry for entry in summary if entry['Stop Loss %'] == sl]
        
        return pd.DataFrame(summary)
    