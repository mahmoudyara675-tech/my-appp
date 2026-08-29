import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# Page configuration
st.set_page_config(page_title="Marah's Prop Firm Tracker", layout="wide")

# Stunning Professional Custom CSS Styling
st.markdown("""
    <style>
    .main {
        background-color: #080c14;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    /* Marah's Custom Header Banner */
    .marah-hero {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 50%, #020617 100%);
        padding: 30px 35px;
        border-radius: 20px;
        border: 1px solid #312e81;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .marah-title {
        color: #f8fafc;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: -0.5px;
        margin: 0;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .marah-subtitle {
        color: #94a3b8;
        font-size: 15px;
        margin: 6px 0 0 0;
        font-weight: 500;
    }
    .badge-marah {
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 14px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.1);
    }
    /* Metric Cards Customization */
    .stMetric {
        background: linear-gradient(145deg, #111827 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        border: 1px solid #1f2937;
    }
    </style>
""", unsafe_allow_html=True)

# Stunning Header with Marah's Name
st.markdown("""
    <div class="marah-hero">
        <div>
            <h1 class="marah-title">✨ Marah's Elite Trading Dashboard</h1>
            <p class="marah-subtitle">Prop Firm Advanced Backtesting & Risk Management Suite</p>
        </div>
        <div>
            <span class="badge-marah">👑 Master Trader</span>
        </div>
    </div>
""", unsafe_allow_html=True)

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
st.sidebar.markdown("### ➕ Add New Trade")

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
    submitted = st.form_submit_button("🚀 Save Trade")

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
    st.subheader("📋 Trade History & Management Control")
    
    # Management Section: Delete Specific Trade or Delete All
    m_col1, m_col2 = st.columns([1.5, 1])
    
    with m_col1:
        st.markdown("##### 🗑️ Delete Specific Trade")
        trade_to_delete = st.selectbox("Select Trade # to Delete", options=[None] + list(df['Trade #']))
        if st.button("Delete Selected Trade") and trade_to_delete is not None:
            st.session_state.trades = [t for t in st.session_state.trades if t['Trade #'] != trade_to_delete]
            for idx, t in enumerate(st.session_state.trades):
                t['Trade #'] = idx + 1
            save_trades()
            st.warning(f"Trade #{trade_to_delete} has been deleted!")
            st.rerun()
            
    with m_col2:
        st.markdown("##### ⚠️ Danger Zone (Delete All)")
        confirm_all = st.checkbox("I confirm to delete all records")
        if st.button("Delete All Trades", type="primary") and confirm_all:
            st.session_state.trades = []
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            st.success("All trade data wiped successfully!")
            st.rerun()

    st.markdown("---")
    st.dataframe(df.drop(columns=['R_Value']), use_container_width=True)
else:
    st.info("No trades recorded yet. Start adding your trades using the sidebar form!")
