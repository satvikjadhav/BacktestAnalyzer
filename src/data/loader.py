import pandas as pd


class DataLoader:
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path)
        df["Entry Date"] = pd.to_datetime(df["Entry Date"], format='%Y-%m-%d')
        df["Day of Week"] = df["Entry Date"].dt.day_name()
        # filtering on Type = Null so that we don't consider individual strike data
        df = df[pd.isna(df['Type'])]
        return df

    @staticmethod
    def extract_details(file_name: str) -> tuple:
        parts = file_name.split("_")
        strategy_type = parts[1]
        stop_loss = parts[-1].replace(".csv", "")
        entry_time = parts[2]
        exit_time = parts[3]
        return strategy_type, stop_loss
