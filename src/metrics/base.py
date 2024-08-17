from abc import ABC, abstractmethod
import pandas as pd

class Metric(ABC):
    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> float:
        pass
    