from metrics.base import Metric
import pandas as pd


class RewardToRiskRatio(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        total_profit = df[df['P/L'] > 0]['P/L'].sum()
        total_loss = abs(df[df['P/L'] < 0]['P/L'].sum())
        return total_profit / total_loss if total_loss != 0 else float('inf')
    
    def is_higher_better(self) -> bool:
        return True

class MaxDrawdown(Metric):
    def calculate(self, df: pd.DataFrame) -> float:
        cumulative = df['P/L'].cumsum()
        running_max = cumulative.cummax()
        drawdown = running_max - cumulative
        return drawdown.max()
    
    def is_higher_better(self) -> bool:
        return False  # For losses, a higher (less negative) number is better
    
class SharpeRatio(Metric):
    """
    The Sharpe Ratio measures the return per unit of risk. 
    It’s calculated as the average return (or profit) minus the risk-free rate, 
    divided by the standard deviation of the returns."""

    def __init__(self, risk_free_rate: float = 0.074):
        self.risk_free_rate = risk_free_rate

    def calculate(self, df: pd.DataFrame) -> float:
        # Calculate daily returns
        daily_returns = df['P/L'].pct_change().dropna()

        # Calculate the Sharpe Ratio
        excess_returns = daily_returns - self.risk_free_rate / 252  # Convert annual rate to daily
        return excess_returns.mean() / excess_returns.std() if excess_returns.std() != 0 else float('inf')

    def is_higher_better(self) -> bool:
        return True

class SortinoRatio(Metric):
    """
    Metric used to assess the risk-adjusted return of an investment or portfolio. 
    Unlike the Sharpe Ratio, which considers all volatility as risk, the Sortino Ratio focuses specifically on downside risk.
    """
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate

    def calculate(self, df: pd.DataFrame) -> float:
        # Calculate daily returns
        daily_returns = df['P/L'].pct_change().dropna()

        # Calculate the downside deviation (only negative returns)
        downside_deviation = daily_returns[daily_returns < 0].std()

        # Calculate excess returns
        excess_returns = daily_returns - self.risk_free_rate / 252  # Convert annual rate to daily

        return excess_returns.mean() / downside_deviation if downside_deviation != 0 else float('inf')

    def is_higher_better(self) -> bool:
        return True

class CalmarRatio(Metric):
    """
    Metric used to assess the performance of an investment relative to its risk, specifically focusing on drawdowns. 
    It is designed to evaluate the return of an investment in relation to the risk of significant declines in value.
    """
    
    def calculate(self, df: pd.DataFrame) -> float:
        # Calculate the annualized return
        cumulative_return = (1 + df['P/L'].sum()) ** (252 / len(df)) - 1

        # Get the max drawdown
        max_drawdown = MaxDrawdown().calculate(df)

        return cumulative_return / abs(max_drawdown) if max_drawdown != 0 else float('inf')

    def is_higher_better(self) -> bool:
        return True
