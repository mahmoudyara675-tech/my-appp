import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# Page configuration
st.set_page_config(
    page_title="MARAH // BMW M-POWER ELITE TERMINAL", 
    page_icon="🏎️", 
    layout="wide"
)

# Ultra-Professional Red & Black BMW M-Power Theme with Sleek Sidebar
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    .main {
        background-color: #030305;
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Supreme BMW Master Banner */
    .bmw-master-banner {
        background: linear-gradient(135deg, rgba(3,3,5,0.88) 0%, rgba(35,3,8,0.85) 100%), 
                    url('https://images.unsplash.com/photo-1555215695-3004980ad54e?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border: 2px solid #ff1744;
        padding: 45px 40px;
        border-radius: 24px;
        box-shadow: 0 0 45px rgba(255, 23, 68, 0.3);
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .bmw-master-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 34px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 0 20px rgba(255, 23, 68, 0.9);
    }

    .bmw-master-sub {
        color: #fda4af;
        font-size: 14px;
        font-weight: 600;
        margin: 8px 0 0 0;
        letter-spacing: 1px;
    }

    .m-power-tag {
        display: inline-block;
        background: #ff1744;
        color: white;
        padding: 6px 16px;
        border-radius: 6px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 3px;
        margin-bottom: 10px;
        box-shadow: 0 0 12px #ff1744;
    }

    /* Status Badge */
    .trader-status-badge {
        background: rgba(255, 23, 68, 0.15);
        border: 1px solid rgba(255, 23, 68, 0.4);
        color: #ff8a80;
        padding: 10px 20px;
        border-radius: 12px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 13px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 23, 68, 0.2);
    }

    /* Metric Cards */
    .stMetric {
        background: linear-gradient(145deg, #09090c 0%, #140407 100%);
        border: 1px solid #2d070f;
        border-top: 3px solid #ff1744;
        padding: 20px;
        border-radius: 14px;
    }

    /* Professional Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #060609;
        border-right: 1px solid #1a0408;
        padding-top: 20px;
    }

    /* Supreme Red Action Buttons */
    .stButton button {
        background: linear-gradient(135deg, #ff1744 0%, #b91c1c 100%);
        color: white;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 0 15px rgba(255, 23, 68, 0.5);
        width: 100%;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #ff4081 0%, #ff1744 100%);
        box-shadow: 0 0 25px rgba(255, 23, 68, 0.8);
    }
    </style>
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

# Calculate dynamic status based on trades
total_trades = len(st.session_state.trades)
wins = len([t for t in st.session_state.trades if t['Result'] == 'Win'])
win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

if total_trades == 0:
    status_text = "STATUS: READY TO LAUNCH 🚀"
elif win_rate >= 60:
    status_text = "🔥 TIER: ELITE M-POWER TRADER"
elif win_rate >= 40:
    status_text = "⚡ TIER: PRO PROP TRADER"
else:
    status_text = "🛡️ TIER: RISK MANAGEMENT MODE"

# Master Header with Dynamic Badge
st.markdown(f"""
    <div class="bmw-master-banner">
        <div>
            <div class="m-power-tag">M-POWER RED EDITION</div>
            <h1 class="bmw-master-title">MARAH'S TERMINAL</h1>
            <p class="bmw-master-sub">Elite Prop Firm Backtesting & High-Speed Execution Suite</p>
        </div>
        <div>
            <div class="trader-status-badge">{status_text}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Professional Sidebar Trade Execution Form
with st.sidebar:
    st.markdown("### 🏎️ EXECUTION PANEL")
    st.markdown("---")
    
    with st.form("trade_form"):
        st.markdown("##### 📅 Trade Parameters")
        trade_date = st.date_input("Trade Date", value=date.today())
        direction = st.selectbox("Direction", ["Long (Buy)", "Short (Sell)"])
        session = st.selectbox("Session", ["NYC", "London", "Asia"])
        pair = st.text_input("Pair / Instrument", "XAUUSD")
        
        st.markdown("##### 📊 Performance")
        result = st.selectbox("Result", ["Win", "Loss"])
        lot_size = st.number_input("Lot Size", min_value=0.01, value=1.00, step=0.1)
        rr = st.number_input("Risk : Reward (R:R)", min_value=0.1, value=2.0, step=0.5)
        notes = st.text_input("Notes / Confluence", "FVG / Session Setup")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 EXECUTE & RECORD")

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
    
    total_profit_r = df['R_Value'].sum()

    # Calculate Max Consecutive Losses
    max_consecutive_losses = 0
    current_losses = 0
    for res in df['Result']:
        if res == 'Loss':
            current_losses += 1
            if current_losses > max_consecutive_losses:
                max_consecutive_losses = current_losses
        else:
            current_losses = 0

    # Metrics Layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    with col2:
        st.metric("100 Trades Challenge", f"{total_trades} / 100")
    with col3:
        st.metric("Total Profit (R)", f"{total_profit_r:+.1f} R")
    with col4:
        st.metric("Max Cons. Losses", f"{max_consecutive_losses} Losses")

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
    
    # Styled Dataframe (Green for Win, Red for Loss)
    def style_results(val):
        if val == 'Win':
            return 'background-color: rgba(16, 185, 129, 0.2); color: #34d399; font-weight: bold;'
        elif val == 'Loss':
            return 'background-color: rgba(239, 68, 68, 0.2); color: #f87171; font-weight: bold;'
        return ''

    display_df = df.drop(columns=['R_Value'])
    styled_df = display_df.style.map(style_results, subset=['Result'])
    
    st.dataframe(styled_df, use_container_width=True)
else:
    st.info("No trades recorded yet. Use the sidebar execution panel on the left to add your first trade!")
