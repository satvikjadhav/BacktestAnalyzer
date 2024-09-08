import pandas as pd
from typing import List, Optional, Dict, Any
from data.loader import DataLoader
from data.processor import DataProcessor
from analysis.calculator import MetricsCalculator
from analysis.optimizer import Optimizer
import os


class BacktestAnalyzer:
    def __init__(self, file_paths: List[str], metrics: Optional[List[str]] = None):
        """Initialize the BacktestAnalyzer with file paths and essential components."""
        self.file_paths = file_paths
        self.all_data = pd.DataFrame()
        self.metrics_calculator = MetricsCalculator(metrics)
        self.optimizer = None
        self.total_days = None

    def load_and_process_data(self):
        """Load and process data from the specified file paths, then store it in the analyzer."""
        data_frames = []
        for file_path in self.file_paths:
            # Extract strategy details (e.g., type and stop loss percentage) from the file name
            strategy_type, stop_loss = self._extract_strategy_details(file_path)
            
            # Load the CSV and add strategy-related columns
            df = self._load_and_prepare_dataframe(file_path, strategy_type, stop_loss)
            data_frames.append(df)

        # Combine all loaded data into a single DataFrame
        self.all_data = pd.concat(data_frames, ignore_index=True)
        
        # Initialize the optimizer with the loaded data
        self.optimizer = Optimizer(self.all_data)
        
        # Calculate the total number of unique days in the data
        self.total_days = len(self.all_data["Entry Date"].unique())

    def analyze(self, days: int, exclude_include_days: Optional[List[str]] = None, stoploss: Optional[List[str]] = None, include_days: bool = True, include_stoploss: bool = True, metric_name: str = 'Total Profit') -> pd.DataFrame:
        """Analyze and determine the optimal stop loss based on the given metric."""
        # Filter data for the last X days and apply exclusions (e.g., certain days or stop losses)
        filtered_data = self._filter_data_for_analysis(days, exclude_include_days, stoploss, include_days, include_stoploss)
        
        # Return the optimal stop loss for the given metric
        return self._get_optimal_stop_loss_by_metric(filtered_data, metric_name)

    def generate_pivot_table(self, days: Optional[int] = None, exclude_include_days: Optional[List[str]] = None, stoploss: Optional[List[str]] = None, include_days: bool = True, include_stoploss: bool = True) -> pd.DataFrame:
        """Generate a pivot table summarizing by the provided metric (P/L) by strategy type and day of the week."""
        # Create a pivot table grouped by day of the week and stop loss percentage
        # Filter data for the last X days if specified
        data = self._filter_data_for_analysis(days, exclude_include_days, stoploss, include_days, include_stoploss)
        pivot_table = self._create_pivot_table(data)
        
        # Add a column indicating the best stop loss for each day
        pivot_table['Best Stop Loss %'] = pivot_table.idxmax(axis=1)
        return pivot_table

    def optimize(self, days: int) -> pd.DataFrame:
        """Optimize and summarize the strategy setup."""
        if not self.optimizer:
            raise ValueError("Data has not been loaded. Call load_and_process_data() first.")
        return self.optimizer.get_optimal_setup_summary(days)

    def generate_summary(self, days: Optional[int] = None, exclude_include_days: Optional[List[str]] = None, stoploss: Optional[List[str]] = None, include_days: bool = True, include_stoploss: bool = True) -> pd.DataFrame:
        """Generate a summary of metrics grouped by day of the week and stop loss percentage."""
        # Filter data for the last X days if specified
        data = self._filter_data_for_analysis(days, exclude_include_days, stoploss, include_days, include_stoploss)
        
        # Calculate metrics grouped by day of the week and stop loss percentage
        summary = self._calculate_grouped_metrics(data, stoploss)

        return pd.DataFrame(summary)
    
    def time_based_performance_breakdown(self, days: int, period: str, exclude_include_days: Optional[List[str]] = None, stoploss: Optional[List[str]] = None, include_days: bool = True, include_stoploss: bool = True, plot: bool = False) -> pd.DataFrame:
        """Analyze performance by time period. 
        
        Valid Time Periods: Use 'M' for monthly, 'Q' for quarterly, or 'Y' for yearly."""
        self.period = period
        # Filter data for the last X days and apply exclusions (e.g., certain days or stop losses)
        filtered_data = self._filter_data_for_analysis(days, exclude_include_days, stoploss, include_days, include_stoploss)

        metrics_calculated = self._calculate_grouped_metrics(filtered_data, columns=['Period'])
        
        if plot:
            self._plot_time_based_performance(metrics_calculated)

        return metrics_calculated
    
    def _plot_time_based_performance(self, df: pd.DataFrame):
        import matplotlib.pyplot as plt
        import plotly.graph_objects as go
        
        df = df.groupby(['Period', 'Strategy Type', 'Stop Loss %'])['Total Profit'].sum().reset_index()
        pivot_table = df.pivot_table(values='Total Profit', index='Period', columns=['Strategy Type', 'Stop Loss %'], aggfunc='sum')
        
        # Convert Period index to strings
        pivot_table.index = pivot_table.index.astype(str)

        fig = go.Figure()

        for column in pivot_table.columns:
            strategy_type, stop_loss = column
            fig.add_trace(go.Scatter(
                x=pivot_table.index,
                y=pivot_table[column],
                mode='lines+markers',
                name=f'{strategy_type} - {stop_loss}',
                hovertemplate='Period: %{x}<br>Total Profit: %{y:.2f}'
            ))

        fig.update_layout(
            title='Profit/Loss Trends Over Time by Strategy Type',
            xaxis_title='Period',
            yaxis_title='Total Profit/Loss',
            legend_title='Strategy Type - Stop Loss %',
            hovermode='x unified'
        )

        fig.show()



    def _group_by(self, df: pd.DataFrame, columns: Optional[list[str]]) -> pd.DataFrame:
        """
        Groups the DataFrame by a specified list of columns.
        """
        default_col_list = ['Day of Week', 'Stop Loss %', 'Strategy Type']

        if columns:
            default_col_list += columns
        
        if 'Period' in default_col_list:
            df['Period'] = df['Entry Date'].dt.to_period(self.period)

        return df.groupby(default_col_list)

    def _extract_strategy_details(self, file_path: str):
        """Extract strategy type and stop loss from the file name."""
        file_name = os.path.basename(file_path)
        return DataLoader.extract_details(file_name)

    def _load_and_prepare_dataframe(self, file_path: str, strategy_type: str, stop_loss: float) -> pd.DataFrame:
        """Load the CSV file and add strategy-related columns."""
        df = DataLoader.load_csv(file_path)
        df['Strategy Type'] = strategy_type
        df['Stop Loss %'] = stop_loss
        return df

    def _filter_data_for_analysis(self, days: int, exclude_include_days: Optional[List[str]], stoploss: Optional[List[str]], include_days: bool = True, include_stoploss: bool = True) -> pd.DataFrame:
        """Filter the data for analysis based on the last X days and exclude criteria."""
        # Filter the data to include only the last X days
        last_x_days_data = DataProcessor.filter_last_x_days(self.all_data, days)

        # Apply exclusions or inclusion for specific days or stop losses
        filtered_data = DataProcessor.filter_days_and_stoploss(last_x_days_data, exclude_include_days, stoploss, include_days, include_stoploss)
        
        return filtered_data

    def _get_optimal_stop_loss_by_metric(self, df: pd.DataFrame, metric_name: str) -> pd.DataFrame:
        """Determine the optimal stop loss based on the specified metric."""
        # Calculate metrics for each group and store them in a DataFrame
        metrics_df = self._calculate_grouped_metrics(df)
        
        # Determine whether higher values of the metric are better or not
        is_higher_better = self.metrics_calculator.is_higher_better(metric_name)

        # Get the index of the row with the best metric value for each day
        idx = metrics_df.groupby('Day of Week')[metric_name].idxmax() if is_higher_better else metrics_df.groupby('Day of Week')[metric_name].idxmin()
        
        # Retrieve the rows corresponding to the optimal stop loss for each day
        return metrics_df.loc[idx]

    def _calculate_grouped_metrics(self, df: pd.DataFrame, columns: Optional[list[str]] = None, stop_loss: Optional[List[str]] = None) -> pd.DataFrame:
        """Calculate metrics grouped by day of the week, stop loss, and strategy type (and additional columns if given)"""
        grouped = self._group_by(df, columns)
        
        # Calculate metrics for each group and store the results in a list
        # Extract group keys dynamically
        metrics = [
            self._generate_group_metrics(group, dict(zip(grouped.grouper.names, keys)))
            for keys, group in grouped
        ]

        # Optionally filter the summary for a specific stop loss percentage
        if stop_loss:
            metrics = [entry for entry in metrics if entry.get('Stop Loss %') in stop_loss]
        
        return pd.DataFrame(self._filter_metrics_by_stop_loss(metrics, stop_loss))

    def _generate_group_metrics(self, group: pd.DataFrame, group_keys: dict) -> dict:
        """Generate metrics for a specific group of data."""
        metrics = self.metrics_calculator.calculate_metrics(group)
        metrics.update(group_keys)

        return metrics
    
    def _filter_metrics_by_stop_loss(self, metrics: List[Dict[str, Any]], stop_loss: Optional[str]) -> List[Dict[str, Any]]:
        """Filter metrics by stop loss if specified."""
        if stop_loss is not None:
            return [entry for entry in metrics if entry.get('Stop Loss %') == stop_loss]
        return metrics

    def _create_pivot_table(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create a pivot table for average P/L grouped by strategy, stop loss, and day."""
        # Group by Strategy Type, Stop Loss %, and Day of Week, and calculate mean P/L
        grouped_data = data.groupby(['Strategy Type', 'Stop Loss %', 'Day of Week'])['P/L'].mean().reset_index()
        # print(grouped_data.apply(print))
        # exit()
        # Define the order of days
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # Create a pivot table with multi-level columns: Strategy Type and Stop Loss %
        pivot_table = grouped_data.pivot_table(
            values='P/L',
            index='Day of Week',
            columns=['Strategy Type', 'Stop Loss %']
        )

        # Reindex the days to ensure they are in the desired order and fill missing values with 0
        pivot_table = pivot_table.reindex(days_order).fillna(0)

        return pivot_table
