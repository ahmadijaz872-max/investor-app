import streamlit as st
import time
import os

# Page Config (Full Screen App Feel)
st.set_page_config(page_title="Investor Trader Panel", page_icon="📈", layout="centered")

# Custom CSS for Dark App Theme
st.markdown("""
    <style>
    .main { background-color: #121212; }
    h2 { color: #00BFFF; text-align: center; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #008CBA; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h2>INVESTOR TRADER PANEL</h2>", unsafe_allow_html=True)

# Gold Price Card
st.markdown("""
    <div style='background-color: #1E1E24; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <p style='color: #888; margin: 0; font-size: 12px;'>GOLD (XAU/USD) REAL-TIME</p>
        <h1 style='color: #FFD700; margin: 0;'>$2,401.66</h1>
    </div>
""", unsafe_allow_html=True)

# 1. Mine Button & 30s Mining Logic
if 'mining' not in st.session_state:
    st.session_state.mining = False

if not st.session_state.mining:
    if st.button("🚀 MINE (30s CHART)"):
        st.session_state.mining = True
        st.rerun()
else:
    st.info("⚡ LIVE CANDLESTICK CHART MINING IN PROGRESS...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(30, 0, -1):
        status_text.subheader(f"Time Remaining: {i}s")
        progress_bar.progress((30 - i) / 30)
        time.sleep(1)
        
    st.success("🎉 SUCCESS! You Have Successfully Made $1")
    if st.button("Back to Dashboard"):
        st.session_state.mining = False
        st.rerun()

st.write("---")

# Stats Section
col1, col2 = st.columns(2)
with col1:
    st.write("**Current Amount**")
    st.write("**Deposit Amount**")
    st.write("**Live Equity**")
    st.write("**Live Withdrawal**")

with col2:
    st.write("<p style='color: #00E676; text-align: right;'><b>$10,500.00</b></p>", unsafe_allow_html=True)
    st.write("<p style='color: #00E676; text-align: right;'><b>$8,000.00</b></p>", unsafe_allow_html=True)
    st.write("<p style='color: #00E676; text-align: right;'><b>$11,250.50</b></p>", unsafe_allow_html=True)
    st.write("<p style='color: #00E676; text-align: right;'><b>$2,500.00</b></p>", unsafe_allow_html=True)

st.write("---")

# Bottom Buttons
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("Add Funds"):
        if os.path.exists("qr_code.jpeg"):
            st.image("qr_code.jpeg", caption="Deposit Address & QR")
        else:
            st.error("qr_code.jpeg missing")

with btn_col2:
    if os.path.exists("rules.pdf"):
        with open("rules.pdf", "rb") as pdf_file:
            st.download_button(
                label="Rules & Legal PDF",
                data=pdf_file,
                file_name="rules.pdf",
                mime="application/pdf"
            )
