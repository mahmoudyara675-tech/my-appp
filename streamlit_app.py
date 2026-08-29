import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# Page configuration
st.set_page_config(
    page_title="MARAH // M-POWER TERMINAL", 
    page_icon="🏎️", 
    layout="wide"
)

# Ultra-Supreme Red & Black BMW M-Power Design Overhaul
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    .main {
        background-color: #020203;
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Supreme BMW Red & Black Cyber Banner */
    .bmw-master-banner {
        background: linear-gradient(135deg, rgba(3,3,5,0.92) 0%, rgba(40,3,8,0.85) 100%), 
                    url('https://images.unsplash.com/photo-1617814076367-b759c7d7e738?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border: 2px solid #ff1744;
        padding: 50px 40px;
        border-radius: 28px;
        box-shadow: 0 0 50px rgba(255, 23, 68, 0.25), inset 0 0 30px rgba(255, 23, 68, 0.1);
        margin-bottom: 35px;
        position: relative;
    }

    .bmw-master-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 38px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 0 20px rgba(255, 23, 68, 0.8);
    }

    .bmw-master-sub {
        color: #fda4af;
        font-size: 15px;
        font-weight: 600;
        margin: 10px 0 0 0;
        letter-spacing: 1px;
    }

    .m-power-tag {
        display: inline-block;
        background: #ff1744;
        color: white;
        padding: 6px 18px;
        border-radius: 6px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 3px;
        margin-bottom: 14px;
        box-shadow: 0 0 15px #ff1744;
    }

    /* Red Accent Metric Cards */
    .stMetric {
        background: linear-gradient(145deg, #09090c 0%, #140407 100%);
        border: 1px solid #2d070f;
        border-top: 3px solid #ff1744;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }

    /* Custom Red Sidebar */
    [data-testid="stSidebar"] {
        background-color: #050508;
        border-right: 1px solid #1a0408;
    }

    /* Supreme Red Action Buttons */
    .stButton button {
        background: linear-gradient(135deg, #ff1744 0%, #b91c1c 100%);
        color: white;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        border-radius: 10px;
        border: none;
        padding: 12px 24px;
        box-shadow: 0 0 20px rgba(255, 23, 68, 0.5);
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #ff4081 0%, #ff1744 100%);
        box-shadow: 0 0 30px rgba(255, 23, 68, 0.8);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Master Header
st.markdown("""
    <div class="bmw-master-banner">
        <div class="m-power-tag">M-POWER RED EDITION</div>
        <h1 class="bmw-master-title">MARAH'S TERMINAL</h1>
        <p class="bmw-master-sub">Elite Prop Firm Backtesting & High-Speed Execution Suite</p>
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

# Sidebar Form (Cleaned & Styled)
st.sidebar.markdown("### 🏎️ New Trade Setup")
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
    submitted = st.form_submit_button("🚀 EXECUTE TRADE")

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
    st.success("Trade executed and recorded successfully!")
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
