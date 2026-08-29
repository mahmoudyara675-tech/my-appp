import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# Page configuration
st.set_page_config(
    page_title="Marah's BMW Elite Terminal", 
    page_icon="🏎️", 
    layout="wide"
)

# Ultra-Professional Red & Black Styling + BMW Vibe + Maximum Usability
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main {
        background-color: #050507;
        color: #f1f5f9;
    }

    /* Hide standard Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Supreme BMW & Red Crimson Header */
    .bmw-header {
        background: linear-gradient(135deg, #090a0f 0%, #18080c 50%, #29050b 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 35px 40px;
        border-radius: 24px;
        box-shadow: 0 25px 50px -12px rgba(220, 38, 38, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }

    .bmw-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #ef4444, #dc2626);
    }

    .header-title-box h1 {
        color: #ffffff;
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .header-title-box p {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 500;
        margin: 8px 0 0 0;
    }

    /* BMW M-Power Vibe Badge */
    .bmw-badge {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(0, 0, 0, 0.6));
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #f87171;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
        letter-spacing: 0.5px;
    }

    .bmw-dot {
        width: 10px;
        height: 10px;
        background-color: #ef4444;
        border-radius: 50%;
        box-shadow: 0 0 10px #ef4444;
    }

    /* Metric Cards Red Accent */
    .stMetric {
        background: linear-gradient(145deg, #0f0f13 0%, #160a0d 100%);
        border: 1px solid #2a1215;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }

    /* Custom Sidebar Red Theme */
    [data-testid="stSidebar"] {
        background-color: #07070a;
        border-right: 1px solid #1a0b0e;
    }

    /* Crimson Buttons */
    .stButton button {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
        transition: all 0.2s ease;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# Supreme Header with Marah's Name & BMW Vibe
st.markdown("""
    <div class="bmw-header">
        <div class="header-title-box">
            <h1>
                <span>🏎️</span> MARAH'S BMW ELITE TERMINAL
            </h1>
            <p>High-Performance Prop Firm Backtesting & Precision Analytics</p>
        </div>
        <div>
            <div class="bmw-badge">
                <div class="bmw-dot"></div>
                M-POWER TRADING SYSTEM
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
st.sidebar.markdown("### 📊 Add New Trade")
st.sidebar.markdown("---")

with st.sidebar.form("trade_form"):
    trade_date = st.date_input("Trade Date", value=date.today())
    direction = st.selectbox("Direction", ["Long (Buy)", "Short (Sell)"])
    session = st.selectbox("Session", ["NYC", "London", "Asia"])
    pair = st.text_input("Pair / Instrument", "EURUSD")
    result = st.selectbox("Result", ["Win", "Loss"])
    lot_size = st.number_input("Lot Size", min_value=0.01, value=1.00, step=0.1)
    rr = st.number_input("Risk : Reward (R:R Ratio)", min_value=0.1, value=2.0, step=0.5)
    notes = st.text_input("Notes / Confluence", "Silver Bullet 10AM FVG")
    submitted = st.form_submit_button("🚀 Save Trade")

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

    # Clean Metrics Layout (Without Dollar Risk/PnL)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    with col2:
        st.metric("Total Trades", f"{total_trades}")
    with col3:
        st.metric("Total Profit (R)", f"{total_profit_r:+.1f} R")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Trade Ledger & Management")
    
    # Management Section
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
