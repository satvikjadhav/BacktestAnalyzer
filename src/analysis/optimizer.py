import pandas as pd
from typing import List, Dict, Tuple, Any
from data.processor import DataProcessor

class Optimizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def find_optimal_setup(self, x: int) -> Dict[str, Any]:
        # Filter for the last x days
        last_x_days_data = DataProcessor.filter_last_x_days(self.data, x)

        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        stop_loss_options = last_x_days_data['Stop Loss %'].unique()
        strategy_types = last_x_days_data['Strategy Type'].unique()

        best_setup = {
            'total_profit': float('-inf'),
            'setup': {}
        }

        # Try all combinations of stop loss and strategy type for each day
        for setup in self._generate_setups(days_of_week, stop_loss_options, strategy_types):
            profit = self._calculate_profit(last_x_days_data, setup)
            if profit > best_setup['total_profit']:
                best_setup['total_profit'] = profit
                best_setup['setup'] = setup

        # Check if excluding any day improves the result
        for day in days_of_week:
            setup_without_day = best_setup['setup'].copy()
            setup_without_day[day] = ('Exclude', 'Exclude')  # Exclude both stop loss and strategy type
            profit_without_day = self._calculate_profit(last_x_days_data, setup_without_day)
            if profit_without_day > best_setup['total_profit']:
                best_setup['total_profit'] = profit_without_day
                best_setup['setup'] = setup_without_day

        return best_setup

    def _generate_setups(self, days: List[str], stop_loss_options: List[str], strategy_types: List[str]) -> List[Dict[str, Tuple[str, str]]]:
        if not days:
            return [{}]
        
        setups = []
        for stop_loss in stop_loss_options:
            for strategy_type in strategy_types:
                sub_setups = self._generate_setups(days[1:], stop_loss_options, strategy_types)
                for setup in sub_setups:
                    setup[days[0]] = (stop_loss, strategy_type)
                    setups.append(setup)
        return setups

    def _calculate_profit(self, data: pd.DataFrame, setup: Dict[str, Tuple[str, str]]) -> float:
        profit = 0
        for day, (stop_loss, strategy_type) in setup.items():
            if stop_loss == 'Exclude' or strategy_type == 'Exclude':
                continue
            day_data = data[(data['Day of Week'] == day) &
                            (data['Stop Loss %'] == stop_loss) &
                            (data['Strategy Type'] == strategy_type)]
            profit += day_data['P/L'].sum()
        return profit

    def get_optimal_setup_summary(self, x: int) -> pd.DataFrame:
        optimal_setup = self.find_optimal_setup(x)
        summary = pd.DataFrame(list(optimal_setup['setup'].items()), columns=['Day', 'Optimal Setup'])
        summary[['Optimal Stop Loss', 'Optimal Strategy Type']] = pd.DataFrame(summary['Optimal Setup'].tolist(), index=summary.index)
        summary = summary.drop(columns=['Optimal Setup'])
        summary['Total Profit'] = optimal_setup['total_profit']
        return summary
