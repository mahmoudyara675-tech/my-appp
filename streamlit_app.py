import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# Page configuration
st.set_page_config(
    page_title="Marah's BMW M-Power Terminal", 
    page_icon="🏎️", 
    layout="wide"
)

# Supreme Red & Black M-Power Styling with Real BMW Background Vibe
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    .main {
        background-color: #030305;
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Real BMW M-Power Aesthetic Header with Background Image */
    .bmw-supreme-banner {
        background: linear-gradient(90deg, rgba(0,0,0,0.85) 0%, rgba(20,5,8,0.7) 100%), 
                    url('https://images.unsplash.com/photo-1555215695-3004980ad54e?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border: 2px solid #dc2626;
        padding: 45px 40px;
        border-radius: 24px;
        box-shadow: 0 0 35px rgba(220, 38, 38, 0.3);
        margin-bottom: 30px;
        position: relative;
    }

    .bmw-supreme-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 36px;
        font-weight: 900;
        letter-spacing: 1px;
        margin: 0;
        text-shadow: 0 0 15px rgba(220, 38, 38, 0.7);
    }

    .bmw-supreme-sub {
        color: #cbd5e1;
        font-size: 15px;
        font-weight: 600;
        margin: 10px 0 0 0;
        letter-spacing: 0.5px;
    }

    .m-power-badge {
        display: inline-block;
        background: #dc2626;
        color: white;
        padding: 6px 16px;
        border-radius: 6px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 2px;
        margin-bottom: 12px;
        box-shadow: 0 0 10px #dc2626;
    }

    /* Modern Metric Cards */
    .stMetric {
        background: #0b0b0f;
        border: 1px solid #1f1f2e;
        border-left: 4px solid #dc2626;
        padding: 20px;
        border-radius: 12px;
    }

    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #060609;
        border-right: 1px solid #14070a;
    }

    /* Red Action Buttons */
    .stButton button {
        background: #dc2626;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 0 15px rgba(220, 38, 38, 0.4);
    }
    .stButton button:hover {
        background: #ef4444;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.7);
    }
    </style>
""", unsafe_allow_html=True)

# Header Section with BMW Vibe and Marah's Name
st.markdown("""
    <div class="bmw-supreme-banner">
        <div class="m-power-badge">M-POWER EDITION</div>
        <h1 class="bmw-supreme-title">MARAH'S BMW TERMINAL</h1>
        <p class="bmw-supreme-sub">High-Performance Trading & Precision Backtesting Suite</p>
    </div>
""", unsafe_allow_html=True)

# Permanent Storage File
DATA_FILE = "trades_data.json"

if 'trades' not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.trades = json.load(f)
    else:
        st.session_state.trades = []

def save_trades():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.trades, f)

# Sidebar Form (Completely Cleaned: No Risk Amount, No PnL)
st.sidebar.markdown("### 🏎️ Add New Trade")
st.sidebar.markdown("---")

with st.sidebar.form("trade_form"):
    trade_date = st.date_input("Trade Date", value=date.today())
    direction = st.selectbox("Direction", ["Long (Buy)", "Short (Sell)"])
    session = st.selectbox("Session", ["NYC", "London", "Asia"])
    pair = st.text_input("Pair / Instrument", "XAUUSD")
    result = st.selectbox("Result", ["Win", "Loss"])
    lot_size = st.number_input("Lot Size", min_value=0.01, value=1.00, step=0.1)
    rr = st.number_input("Risk : Reward (R:R Ratio)", min_value=0.1, value=2.0, step=0.5)
    notes = st.text_input("Notes / Confluence", "FVG / Session Setup")
    submitted = st.form_submit_button("🚀 Record Trade")

if submitted:
    trade_num = len(st.session_state.trades) + 1
    
    st.session_state.trades.append({
        "Trade #": trade_num,
        "Date": str(trade_date),
        "Direction": direction,
        "Session": session,
        "Pair": pair.upper(),
        "Result": result,
        "Lot Size": lot_size,
        "R:R": f"1:{rr}",
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

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    with col2:
        st.metric("Total Trades", f"{total_trades}")
    with col3:
        st.metric("Total Profit (R)", f"{total_profit_r:+.1f} R")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🏁 Trade Ledger & Management")
    
    m_col1, m_col2 = st.columns([1.5, 1])
    
    with m_col1:
        trade_to_delete = st.selectbox("Select Trade # to Delete", options=[None] + list(df['Trade #']))
        if st.button("🗑️ Delete Selected Trade") and trade_to_delete is not None:
            st.session_state.trades = [t for t in st.session_state.trades if t['Trade #'] != trade_to_delete]
            for idx, t in enumerate(st.session_state.trades):
                t['Trade #'] = idx + 1
            save_trades()
            st.warning(f"Trade #{trade_to_delete} removed.")
            st.rerun()
            
    with m_col2:
        st.markdown("##### ⚠️ Danger Zone")
        confirm_all = st.checkbox("Confirm Delete All Records")
        if st.button("🗑️ Delete All Trades", type="primary") and confirm_all:
            st.session_state.trades = []
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            st.success("All data cleared successfully.")
            st.rerun()

    st.markdown("---")
    st.dataframe(df.drop(columns=['R_Value']), use_container_width=True)
else:
    st.info("No trades recorded yet. Start adding your trades using the sidebar form!")
