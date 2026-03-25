import streamlit as st

from data_pipeline.fetch_data import fetch_stock_price
from agents.fundamental import fundamental_agent
from agents.risk import risk_agent
from agents.technical import technical_agent
from agents.macro import macro_agent
from agents.sentiment import sentiment_agent
from aggregator.decision_engine import aggregate_decision
from database.db import get_connection


# ===== STORE FUNCTION =====
def store_stock_data(data, symbol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM stock_prices WHERE symbol = %s", (symbol,))

    for _, row in data.iterrows():
        cursor.execute(
            """
            INSERT INTO stock_prices (symbol, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                symbol,
                row["Date"].date(),
                float(row["Open"]),
                float(row["High"]),
                float(row["Low"]),
                float(row["Close"]),
                int(row["Volume"])
            )
        )

    conn.commit()
    conn.close()


# ===== UI =====

st.set_page_config(page_title="Stock AI Advisor", layout="centered")

st.title("📈 AI Stock Investment Advisor")

symbol = st.text_input("Enter Stock Symbol (e.g., TCS.NS)", "TCS.NS")

# 💰 Investment input
investment_amount = st.number_input("Enter Investment Amount (₹)", value=100000)

if st.button("Analyze Stock"):

    # ===== DATA FETCH =====
    st.write("Fetching data...")
    data = fetch_stock_price(symbol)
    store_stock_data(data, symbol)
    st.success("✅ Data fetched and stored")

    # ===== RUN AGENTS =====
    st.write("Running analysis...")

    fundamental = fundamental_agent(symbol)
    risk = risk_agent(symbol)
    technical = technical_agent(symbol)
    macro = macro_agent()
    sentiment = sentiment_agent(symbol)

    # ===== AGGREGATE =====
    final = aggregate_decision(
    fundamental,
    risk,
    technical,
    macro,
    sentiment
)

    # ===== DEBUG VIEW =====
    with st.expander("📊 View Detailed Agent Analysis"):
        st.write("Fundamental:", fundamental)
        st.write("Risk:", risk)
        st.write("Technical:", technical)
        st.write("Macro:", macro)
        st.write("Sentiment:", sentiment)

    # ===== CLEAN USER OUTPUT =====
    st.subheader("🚀 Investment Recommendation")

    decision = final["final_decision"]

    # 🎯 DECISION INTERPRETATION
    if decision == "BUY":
        st.success("🟢 Good time to invest")
        action_text = "You can consider investing in this stock."

    elif decision == "HOLD":
        st.warning("🟡 Wait before investing")
        action_text = "Market conditions are not favorable right now."

    elif decision == "SELL":
        st.error("🔴 Avoid this stock")
        action_text = "This stock is not suitable for investment currently."

    # ===== SUMMARY =====
    st.write(f"**Action:** {action_text}")
    st.metric("Confidence", f"{final['confidence_score']}%")

    # 💰 INVESTMENT CALCULATION
    if "30%" in final["position_size"]:
        amount = investment_amount * 0.3
        st.write(f"💰 Suggested Investment: ₹{int(amount)}")

    elif "50%" in final["position_size"]:
        amount = investment_amount * 0.5
        st.write(f"💰 Suggested Investment: ₹{int(amount)}")

    elif "10%" in final["position_size"]:
        amount = investment_amount * 0.1
        st.write(f"💰 Suggested Investment: ₹{int(amount)}")

    # ===== WHY THIS DECISION =====
    st.markdown("### 🧠 Why this decision?")

    st.info(final.get("reasoning_summary", "Based on combined analysis of all factors"))

    # ===== LONG-TERM BADGE =====
    st.markdown("### 🏷️ Investment Type")

    if fundamental["signal"] == "BUY" and risk["signal"] == "BUY":
        st.success("📈 Suitable for Long-Term Investment")
    else:
        st.warning("⚠️ Better for Short-Term / Cautious Investing")

    # ===== DETAILS =====
    st.markdown("### 📊 Details")

    st.markdown(
        "ℹ️ **Position Size**  \nHow much of your money to invest in this stock.",
        help="Example: 30% means invest ₹30,000 out of ₹1,00,000"
    )
    st.write(final["position_size"])

    st.markdown(
        "🛑 **Stop Loss**  \nPrice at which you should exit to avoid big losses.",
        help="If stock falls to this level, consider selling to protect your money"
    )
    st.write(final["stop_loss"] if final["stop_loss"] else "Not applicable")

    st.markdown(
        "🎯 **Target Price**  \nExpected price where you can book profit.",
        help="This is an estimated level based on analysis"
    )
    st.write(final["target_levels"] if final["target_levels"] else "Not defined")