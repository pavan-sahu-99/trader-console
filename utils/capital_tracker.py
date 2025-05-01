import pandas as pd

def get_current_capital(trade_data, base_capital=35500):
    if trade_data.empty:
        return base_capital
    return base_capital + trade_data["actual_profit"].sum()

def calculate_lot_size(capital):
    step = 15000
    lots = 2 + max(0, (capital - 35500) // step)
    return int(lots)

