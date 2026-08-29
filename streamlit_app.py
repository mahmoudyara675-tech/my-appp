import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# Page configuration & Styling
st.set_page_config(page_title="Prop Firm Backtest Tracker", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        color: #f8fafc;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Auto Backtest Tracker (Prop Firms)")

# Permanent Storage File
DATA_FILE = "trades_data.json"

# Load trades permanently
if 'trades' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.trades = json.load(f)
    else:
        st.session_state.trades = []

def save_trades():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.trades, f)

# Sidebar for Adding Trades
st.sidebar.header("➕ Add New Trade")

with st.sidebar.form("trade_form"):
    trade_date = st.date_input("Trade Date", value=date.today())
    direction = st.selectbox("Direction", ["Long (Buy)", "Short (Sell)"])
    session = st.selectbox("Session", ["NYC", "London", "Asia"])
    pair = st.text_input("Pair / Instrument", "EURUSD")
    result = st.selectbox("Result", ["Win", "Loss"])
    lot_size = st.number_input("Lot Size", min_value=0.01, value=1.00, step=0.1)
    risk_amount = st.number_input("Risk Amount ($)", min_value=0.0, value=100.0, step=10.0)
    rr = st.number_input("Risk : Reward (R:R Ratio)", min_value=0.1, value=2.0, step=0.5)
    notes = st.text_input("Notes / Confluence", "Silver Bullet 10AM FVG")
    submitted = st.form_submit_button("🚀 Add Trade")

if submitted:
    trade_num = len(st.session_state.trades) + 1
    pnl_dollar = (risk_amount * rr) if result == "Win" else (-risk_amount)
    
    st.session_state.trades.append({
        "Trade #": trade_num,
        "Date": str(trade_date),
        "Direction": direction,
        "Session": session,
        "Pair": pair.upper(),
        "Result": result,
        "Lot Size": lot_size,
        "Risk ($)": risk_amount,
        "R:R": f"1:{rr}",
        "P&L ($)": pnl_dollar,
        "R_Value": rr if result == "Win" else -1.0,
        "Notes": notes
    })
    save_trades()
    st.success("Trade added successfully!")
    st.rerun()

# Main Dashboard View
if st.session_state.trades:
    df = pd.DataFrame(st.session_state.trades)
    
    total_trades = len(df)
    wins = len(df[df['Result'] == 'Win'])
    win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
    total_profit_r = df['R_Value'].sum()
    total_pnl_dollar = df['P&L ($)'].sum() if 'P&L ($)' in df.columns else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Win Rate", f"{win_rate:.1f}%")
    col2.metric("Total Trades", f"{total_trades}")
    col3.metric("Total Profit (R)", f"{total_profit_r:+.1f} R")
    col4.metric("Net P&L ($)", f"${total_pnl_dollar:+,.2f}")

    st.markdown("---")
    st.subheader("📋 Trade History & Management")
    
    trade_to_delete = st.selectbox("Select Trade # to Delete (Optional)", options=[None] + list(df['Trade #']))
    if st.button("🗑️ Delete Selected Trade") and trade_to_delete is not None:
        st.session_state.trades = [t for t in st.session_state.trades if t['Trade #'] != trade_to_delete]
        for idx, t in enumerate(st.session_state.trades):
            t['Trade #'] = idx + 1
        save_trades()
        st.warning(f"Trade #{trade_to_delete} deleted!")
        st.rerun()

    st.dataframe(df.drop(columns=['R_Value']), use_container_width=True)
    
    if st.sidebar.button("⚠️ Reset All Data"):
        st.session_state.trades = []
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.rerun()
else:
    st.info("No trades recorded yet. Add your first trade using the sidebar form!")
