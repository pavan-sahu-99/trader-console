import pandas as pd

def check_risk_warnings(trade_data, current_risk):
    warnings = []

    if current_risk > 1500:
        warnings.append("⚠️ Risk per trade exceeds ₹1500!")

    daily_loss = trade_data.groupby("date")["actual_profit"].sum()
    if not daily_loss.empty and daily_loss.iloc[-1] < -3000:
        warnings.append("🛑 Daily loss > ₹3000! Stop trading for the day.")

    return warnings

