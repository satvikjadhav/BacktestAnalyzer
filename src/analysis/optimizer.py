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

        best_setup = {
            'total_profit': float('-inf'),
            'setup': {}
        }

        # Try all combinations of stop loss for each day
        for setup in self._generate_setups(days_of_week, stop_loss_options):
            profit = self._calculate_profit(last_x_days_data, setup)
            if profit > best_setup['total_profit']:
                best_setup['total_profit'] = profit
                best_setup['setup'] = setup

        # Check if excluding any day improves the result
        for day in days_of_week:
            setup_without_day = best_setup['setup'].copy()
            setup_without_day[day] = 'Exclude'
            profit_without_day = self._calculate_profit(last_x_days_data, setup_without_day)
            if profit_without_day > best_setup['total_profit']:
                best_setup['total_profit'] = profit_without_day
                best_setup['setup'] = setup_without_day

        return best_setup

    def _generate_setups(self, days: List[str], stop_loss_options: List[str]) -> List[Dict[str, str]]:
        if not days:
            return [{}]
        
        setups = []
        for option in stop_loss_options:
            sub_setups = self._generate_setups(days[1:], stop_loss_options)
            for setup in sub_setups:
                setup[days[0]] = option
                setups.append(setup)
        return setups

    def _calculate_profit(self, data: pd.DataFrame, setup: Dict[str, str]) -> float:
        profit = 0
        for day, stop_loss in setup.items():
            if stop_loss == 'Exclude':
                continue
            day_data = data[(data['Day of Week'] == day) & (data['Stop Loss %'] == stop_loss)]
            profit += day_data['P/L'].sum()
        return profit

    def get_optimal_setup_summary(self, x: int) -> pd.DataFrame:
        optimal_setup = self.find_optimal_setup(x)
        summary = pd.DataFrame(list(optimal_setup['setup'].items()), columns=['Day', 'Optimal Stop Loss'])
        summary['Total Profit'] = optimal_setup['total_profit']
        return summary
    