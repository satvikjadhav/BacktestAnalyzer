import pandas as pd
from typing import List, Optional


class DataProcessor:
    @staticmethod
    def filter_last_x_days(data: pd.DataFrame, x: int) -> pd.DataFrame:
        latest_date = data['Entry Date'].max()
        return data[data['Entry Date'] >= (latest_date - pd.Timedelta(days=x))]
    
    @staticmethod
    def filter_days_and_stoploss(df: pd.DataFrame, days: Optional[List[str]] = None, stoploss: Optional[List[str]] = None, include_days: bool = True, include_stoploss: bool = True) -> pd.DataFrame:
        if days is not None:
            if include_days:
                df = df[df['Day of Week'].isin(days)]
            else:
                df = df[~df['Day of Week'].isin(days)]
        
        if stoploss is not None:
            if include_stoploss:
                df = df[df['Stop Loss %'].isin(stoploss)]
            else:
                df = df[~df['Stop Loss %'].isin(stoploss)]
        
        return df
