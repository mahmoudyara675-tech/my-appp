import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# Page configuration
st.set_page_config(
    page_title="Marah's Elite Trading Terminal", 
    page_icon="⚡", 
    layout="wide"
)

# Ultra-Professional Custom Styling (Glassmorphism & Institutional Dark Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main {
        background-color: #07090e;
        color: #f1f5f9;
    }

    /* Hide standard elements for clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Super Professional Header */
    .terminal-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 30px 40px;
        border-radius: 20px;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 35px;
        position: relative;
        overflow: hidden;
    }

    .terminal-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #38bdf8, #6366f1);
    }

    .terminal-title {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .terminal-subtitle {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 500;
        margin: 6px 0 0 0;
        letter-spacing: 0.2px;
    }

    .status-badge {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        padding: 8px 16px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.1);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #34d399;
        border-radius: 50%;
        box-shadow: 0 0 10px #34d399;
    }

    /* Modern Metric Cards */
    .metric-container {
        background: linear-gradient(145deg, #0f172a 0%, #111827 100%);
        border: 1px solid #1e293b;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    .metric-container:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }

    /* Custom Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid #1e293b;
    }

    /* Custom Buttons */
    .stButton button {
        background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transition: all 0.2s ease;
    }

    .stButton button:hover {
        opacity: 0.9;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="terminal-header">
        <div>
            <h1 class="terminal-title">
                <span>⚡</span> MARAH'S INSTITUTIONAL TERMINAL
            </h1>
            <p class="terminal-subtitle">Advanced Quantitative Backtesting & Prop Firm Risk Engine</p>
        </div>
        <div>
            <div class="status-badge">
                <div class="status-dot"></div>
                SYSTEM LIVE & SECURE
            </div>
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
st.sidebar.markdown("### 📊 Trade Execution Panel")
st.sidebar.markdown("---")

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
    submitted = st.form_submit_button("🚀 Execute & Record Trade")

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
    st.success("Trade recorded successfully!")
    st.rerun()

# Main Dashboard View
if st.session_state.trades:
    df = pd.DataFrame(st.session_state.trades)
    
    total_trades = len(df)
    wins = len(df[df['Result'] == 'Win'])
    win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
    total_profit_r = df['R_Value'].sum()
    total_pnl_dollar = df['P&L ($)'].sum() if 'P&L ($)' in df.columns else 0.0

    # Professional Metrics Layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    with col2:
        st.metric("Total Trades", f"{total_trades}")
    with col3:
        st.metric("Total Profit (R)", f"{total_profit_r:+.1f} R")
    with col4:
        st.metric("Net P&L ($)", f"${total_pnl_dollar:+,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Institutional Ledger & Controls")
    
    # Management Section
    m_col1, m_col2 = st.columns([1.5, 1])
    
    with m_col1:
        trade_to_delete = st.selectbox("Select Trade # to Expunge", options=[None] + list(df['Trade #']))
        if st.button("🗑️ Remove Selected Trade") and trade_to_delete is not None:
            st.session_state.trades = [t for t in st.session_state.trades if t['Trade #'] != trade_to_delete]
            for idx, t in enumerate(st.session_state.trades):
                t['Trade #'] = idx + 1
            save_trades()
            st.warning(f"Trade #{trade_to_delete} removed.")
            st.rerun()
            
    with m_col2:
        st.markdown("##### ⚠️ Risk Zone")
        confirm_all = st.checkbox("Authorize Database Wipe")
        if st.button("🗑️ Purge All Data", type="primary") and confirm_all:
            st.session_state.trades = []
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            st.success("Database purged successfully.")
            st.rerun()

    st.markdown("---")
    st.dataframe(df.drop(columns=['R_Value']), use_container_width=True)
else:
    st.info("No trading telemetry recorded yet. Initialize your first record using the sidebar execution panel.")
