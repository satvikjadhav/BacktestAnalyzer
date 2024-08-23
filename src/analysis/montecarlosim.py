import numpy as np
from analysis.analyzer import BacktestAnalyzer
import pandas as pd
from typing import Tuple


class MonteCarloSimulator:
    def __init__(self, backtest_analyzer: BacktestAnalyzer, num_simulations: int = 1000):
        self.backtest_analyzer = backtest_analyzer
        self.num_simulations = num_simulations

    def run_simulation(self, days: int, confidence_interval: float = 0.95) -> Tuple[pd.DataFrame, dict]:
        results = []
        original_data = self.backtest_analyzer.all_data['P/L']
        
        for _ in range(self.num_simulations):
            simulated_returns = np.random.choice(original_data, size=days, replace=True)
            cumulative_returns = np.cumsum(simulated_returns)
            max_drawdown = self._calculate_max_drawdown(cumulative_returns)
            total_profit = cumulative_returns[-1]
            
            results.append({
                'Total Profit': total_profit,
                'Max Drawdown': max_drawdown,
                'Final Equity': cumulative_returns[-1]
            })
        
        results_df = pd.DataFrame(results)
        
        summary_stats = self._calculate_summary_stats(results_df, confidence_interval)
        
        return results_df, summary_stats

    def _calculate_max_drawdown(self, cumulative_returns: np.array) -> float:
        peak = np.maximum.accumulate(cumulative_returns)
        drawdown = peak - cumulative_returns
        return np.max(drawdown)

    def _calculate_summary_stats(self, results_df: pd.DataFrame, confidence_interval: float) -> dict:
        lower_percentile = (1 - confidence_interval) / 2
        upper_percentile = 1 - lower_percentile
        
        return {
            'Mean Total Profit': results_df['Total Profit'].mean(),
            'Std Dev Total Profit': results_df['Total Profit'].std(),
            f'{confidence_interval*100}% CI Lower': results_df['Total Profit'].quantile(lower_percentile),
            f'{confidence_interval*100}% CI Upper': results_df['Total Profit'].quantile(upper_percentile),
            'Mean Max Drawdown': results_df['Max Drawdown'].mean(),
            'Mean Final Equity': results_df['Final Equity'].mean(),
        }

    def plot_results(self, results_df: pd.DataFrame, summary_stats: dict):
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 6))
        plt.hist(results_df['Total Profit'], bins=50, edgecolor='black')
        plt.title('Distribution of Total Profit in Monte Carlo Simulations')
        plt.xlabel('Total Profit')
        plt.ylabel('Frequency')
        
        stats_text = "\n".join([f"{k}: {v:.2f}" for k, v in summary_stats.items()])
        plt.text(0.05, 0.95, stats_text, transform=plt.gca().transAxes, verticalalignment='top', 
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
        
        plt.show()