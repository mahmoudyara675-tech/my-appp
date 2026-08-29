import streamlit as st
import pandas as pd
st.set_page_config(page_title="Prop Firm Backtest Tracker", layout="wide")
st.title("📊 Auto Backtest Tracker (Prop Firms)")
if 'trades' not in st.session_state:
    st.session_state.trades = []
    st.sidebar.header("➕ Add New Trade")
with st.sidebar.form("trade_form", clear_on_submit=True):
    session = st.selectbox("Session", ["NYC", "London", "Asia"])
    result = st.selectbox("Result", ["Win", "Loss"])
lot_size = st.number_input("Lot Size", min_value=0.01, value=1.00, step=0.1)
rr = st.number_input("Risk : Reward (R:R Ratio)", min_value=0.1, value=2.0, step=0.5)
pair = st.text_input("Pair / Instrument", "EURUSD")
notes = st.text_input("Notes / Confluence", "Silver Bullet 10AM FVG")
submitted = st.form_submit_button("🚀 Add Trade")
if submitted:
    trade_num = len(st.session_state.trades) + 1
    st.session_state.trades.append({
        "Trade #": trade_num, 
        "Session": session, 
        "Pair": pair.upper(),
        "Result": result, 
        "Lot Size": lot_size, 
        "R:R": f"1:{rr}",
        "R_Value": rr if result == "Win" else -1.0, 
        "Notes": notes })
    if st.session_state.trades:
     df = pd.DataFrame(st.session_state.trades)
    col1, col2, col3 = st.columns(3)
    col1.metric("Win Rate", f"{(len(df[df['Result'] == 'Win'])/len(df))*100:.1f}%")
    col2.metric("Total Trades", f"{len(df)}")
    col3.metric("Total Profit (R)", f"{df['R_Value'].sum():+.1f} R")
st.dataframe(df.drop(columns=['R_Value']), use_container_width=True)
else:
    st.info("Use the sidebar to add your first trade!")
