import streamlit as st
import pandas as pd

st.title("📊 Backtest Tracker")
pair = st.text_input("Pair", "EURUSD")
res = st.selectbox("Result", ["Win", "Loss"])
if st.button("Add"):
    st.success(f"Added {pair} - {res}")
