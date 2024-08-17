import pandas as pd


class DataLoader:
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path)
        df["Entry Date"] = pd.to_datetime(df["Entry Date"], format="%d-%m-%y")
        df["Day of Week"] = df["Entry Date"].dt.day_name()
        return df

    @staticmethod
    def extract_details(file_name: str) -> tuple:
        parts = file_name.split("_")
        strategy_type = parts[1]
        stop_loss = parts[-1].replace(".csv", "")
        return strategy_type, stop_loss
