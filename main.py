# 1. Imports
from data_pipeline.fetch_data import fetch_stock_price
from database.db import get_connection
from agents.risk import risk_agent
from agents.technical import technical_agent
from agents.fundamental import fundamental_agent
from agents.macro import macro_agent
from aggregator.decision_engine import aggregate_decision
from agents.sentiment import sentiment_agent

# 2. Store function (keep as is)
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
    print("✅ Stock data stored")


# ===== MAIN FLOW =====

symbol = "TCS.NS"

# 1. Fetch + store
print("Fetching data...")
data = fetch_stock_price(symbol)
store_stock_data(data, symbol)

# 2. Run all agents

print("Running Fundamental Agent...")
fundamental = fundamental_agent(symbol)
print("Fundamental:", fundamental)

print("Running Risk Agent...")
risk = risk_agent(symbol)
print("Risk:", risk)

print("Running Technical Agent...")
technical = technical_agent(symbol)
print("Technical:", technical)

print("Running Macro Agent...")
macro = macro_agent()
print("Macro:", macro)

print("Running Sentiment Agent...")
sentiment = sentiment_agent(symbol)
print("Sentiment:", sentiment)

# 3. 🔥 FINAL AGGREGATION (PUT HERE ONLY)

print("Running Aggregator...")

final = aggregate_decision(
    fundamental,
    risk,
    technical,
    macro,
    sentiment
)

print("Final Decision:", final)