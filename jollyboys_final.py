import streamlit as st
import pandas as pd
import math
import os

FILE_PATH = "jollyboys.csv"  # Path to your uploaded CSV

# ---------------- Utility Functions ----------------
def num(x):
    try:
        if x is None:
            return 0.0
        if isinstance(x, (int, float)):
            return float(x)
        s = str(x).strip()
        if s == "" or s.lower() == "nan":
            return 0.0
        return float(s)
    except Exception:
        return 0.0

def load_data():
    df = pd.read_csv(FILE_PATH)
    df.rename(columns=lambda x: str(x).strip(), inplace=True)
    for col in df.columns:
        if col not in ["user_id", "NAME", "DESIGNATION"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df

def save_data(df):
    df.to_csv(FILE_PATH, index=False)

# ---------------- Page Settings ----------------
st.set_page_config(page_title="Jollyboys Savings Dashboard", layout="wide")

# ---------------- Custom CSS ----------------
st.markdown("""
    <style>
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .card h3 { margin-bottom: 10px; font-size: 16px; color: gray; }
        .card p { font-size: 22px; font-weight: bold; color: #1a73e8; }
        .dashboard-section {
            background-color: white; padding: 20px;
            border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .section-title { font-size: 18px; font-weight: bold; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# ---------------- Session State ----------------
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# ---------------- Load Data ----------------
df = load_data()

# ---------------- User Section ----------------
st.markdown("## 💰 Jollyboys Savings Dashboard")
user_id = st.text_input("Enter your User ID:")

if user_id:
    if user_id in df["user_id"].astype(str).values:
        user_data = df[df["user_id"].astype(str) == user_id].iloc[0]

        # --- User Dashboard ---
        st.markdown(
            f'<div class="dashboard-section">'
            f'<div class="section-title">🔑 User Dashboard - {user_data["NAME"]} ({user_data["DESIGNATION"]})</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4, col5 , col6 = st.columns(6)
        with col1:
            st.markdown(f'<div class="card"><h3>2024 Credited</h3><p>₹{user_data["2024_Credited"]}</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><h3>Fine Amount</h3><p>₹{user_data["total_FINE"]}</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="card"><h3>2024 Balance</h3><p>₹{user_data["2024_balance"]}</p></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="card"><h3>2025 Balance</h3><p>₹{user_data["2025_balance"]}</p></div>', unsafe_allow_html=True)
        with col5:
            st.markdown(f'<div class="card"><h3>Total</h3><p>₹{user_data["Total"]}</p></div>', unsafe_allow_html=True)
        if "Loan_Amount" in df.columns and user_data["Loan_Amount"] > 0:
            if "Loan_Completed" not in df.columns or user_data["Loan_Completed"] == 0:
                with col6:
                    st.markdown(
                        f'<div class="card"><h3>Loan</h3><p>₹{user_data["Loan_Amount"]}</p></div>',
                        unsafe_allow_html=True
                    )
            elif "Loan_Completed" in df.columns and user_data["Loan_Completed"] > 0:
                with col6:
                    st.markdown(
                        f'<div class="card"><h3>Loan</h3><p>Loan is completed</p></div>',
                        unsafe_allow_html=True
                    )
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Group Dashboard ---
        st.markdown('<div class="dashboard-section"><div class="section-title">👥 Group Dashboard</div>', unsafe_allow_html=True)
        sum_2024_balance   = num(df["2024_balance"].sum()) if "2024_balance" in df else 0.0
        sum_2025_balance   = num(df["2025_balance"].sum()) if "2025_balance" in df else 0.0
        sum_total_fine     = num(df["total_FINE"].sum())   if "total_FINE" in df else 0.0
        sum_Loan_Amount    = num(df["Loan_Amount"].sum())  if "Loan_Amount" in df else 0.0
        sum_PROFIT_AMOUNT  = num(df["PROFIT_AMOUNT"].sum())if "PROFIT_AMOUNT" in df else 0.0
        sum_Loan_Completed = num(df["Loan_Completed"].sum()) if "Loan_Completed" in df else 0.0

        current_amount = sum_2024_balance + sum_2025_balance + sum_total_fine + sum_Loan_Completed + sum_PROFIT_AMOUNT - sum_Loan_Amount

        col6, col7, col8, col9, col10 = st.columns(5)
        with col6:
            st.markdown(f'<div class="card"><h3>Loan Amount</h3><p>₹{sum_Loan_Amount}</p></div>', unsafe_allow_html=True)
        with col7:
            st.markdown(f'<div class="card"><h3>Sum of 2024 Balance</h3><p>₹{sum_2024_balance}</p></div>', unsafe_allow_html=True)
        with col8:
            st.markdown(f'<div class="card"><h3>Sum of 2025 Balance</h3><p>₹{sum_2025_balance}</p></div>', unsafe_allow_html=True)
        with col9:
            st.markdown(f'<div class="card"><h3>Sum of Total Fine</h3><p>₹{sum_total_fine}</p></div>', unsafe_allow_html=True)
        with col10:
            st.markdown(f'<div class="card"><h3>Current Amount</h3><p>₹{current_amount}</p></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ User ID not found. Please check and try again.")

