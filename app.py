import streamlit as st
import pandas as pd
from utils.capital_tracker import get_current_capital, calculate_lot_size
from utils.risk_manager import check_risk_warnings
from datetime import datetime
import os

# Load trade data
TRADE_FILE = "data/trades.csv"
if os.path.exists(TRADE_FILE):
    trades = pd.read_csv(TRADE_FILE)
else:
    trades = pd.DataFrame(columns=["date", "time", "setup", "entry_price", "exit_price", "qty", "sl", "target", "planned_risk", "actual_profit", "followed_plan", "emotion_score", "notes"])

# Header
st.title("📈 Trader Console")

# Capital & Lot Display
capital = get_current_capital(trades)
lots = calculate_lot_size(capital)
risk_per_trade = lots * 10  # ₹10 per quantity x 75 (per lot)

st.sidebar.header("Capital Status")
st.sidebar.metric("Current Capital", f"₹{capital:,.0f}")
st.sidebar.metric("Lot Size", f"{lots} lot(s)")
st.sidebar.metric("Max Risk/Trade", f"₹{risk_per_trade * 75}")

# Risk Alerts
alerts = check_risk_warnings(trades, risk_per_trade * 75)
if alerts:
    st.warning("\n".join(alerts))

# --- Trade Entry Form ---
st.subheader("📋 Log a New Trade")
with st.form("log_trade"):
    col1, col2 = st.columns(2)
    setup = col1.text_input("Setup Name")
    qty = col2.number_input("Quantity", min_value=75, step=75, value=lots * 75)
    
    entry = col1.number_input("Entry Price")
    exit = col2.number_input("Exit Price")
    
    sl = col1.number_input("Stop Loss")
    target = col2.number_input("Target")

    planned_risk = col1.number_input("Planned Risk", value=1500)
    actual_profit = col2.number_input("Actual Profit (+/-)", value=0)

    followed_plan = st.selectbox("Followed Plan?", ["Yes", "No"])
    emotion_score = st.slider("Emotion Level (1 = calm, 5 = anxious)", 1, 5, 3)
    notes = st.text_area("Notes (Why exit? What felt off?)")

    submitted = st.form_submit_button("Add Trade")

    if submitted:
        now = datetime.now()
        new_trade = pd.DataFrame([{
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "setup": setup,
            "entry_price": entry,
            "exit_price": exit,
            "qty": qty,
            "sl": sl,
            "target": target,
            "planned_risk": planned_risk,
            "actual_profit": actual_profit,
            "followed_plan": followed_plan,
            "emotion_score": emotion_score,
            "notes": notes
        }])
        trades = pd.concat([trades, new_trade], ignore_index=True)
        trades.to_csv(TRADE_FILE, index=False)
        st.success("Trade logged!")

# --- Trade History ---
st.subheader("📊 Trade History")
st.dataframe(trades.sort_values("date", ascending=False).reset_index(drop=True))

# --- Performance Metrics ---
st.subheader("📈 Performance Summary")
total_profit = trades["actual_profit"].sum()
win_rate = (trades["actual_profit"] > 0).mean() * 100 if not trades.empty else 0
avg_r = trades["actual_profit"].mean() if not trades.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total P&L", f"₹{total_profit:,.0f}")
col2.metric("Win Rate", f"{win_rate:.1f}%")
col3.metric("Avg Profit/Loss", f"₹{avg_r:.0f}")
