import pandas as pd
from typing import List


class DataProcessor:
    @staticmethod
    def filter_last_x_days(data: pd.DataFrame, x: int) -> pd.DataFrame:
        latest_date = data['Entry Date'].max()
        return data[data['Entry Date'] >= (latest_date - pd.Timedelta(days=x))]

    @staticmethod
    def exclude_days_or_stoploss(df: pd.DataFrame, exclude_days: List[str] = None, exclude_stoploss: List[str] = None) -> pd.DataFrame:
        if exclude_days:
            df = df[~df['Day of Week'].isin(exclude_days)]
        if exclude_stoploss:
            df = df[~df['Stop Loss %'].isin(exclude_stoploss)]
        return df
    