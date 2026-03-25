import pandas as pd
from database.db import get_connection

def technical_agent(symbol):
    try:
        conn = get_connection()

        query = """
        SELECT date, close FROM stock_prices
        WHERE symbol = %s
        ORDER BY date;
        """

        df = pd.read_sql(query, conn, params=(symbol,))
        conn.close()

        if len(df) < 20:
            return {
                "agent_name": "Technical",
                "signal": "WAIT_FOR_PULLBACK",
                "confidence": 50,
                "reasoning": "Not enough data for MA20"
            }

        # Calculate moving average
        df["ma20"] = df["close"].rolling(window=20).mean()

        current_price = df["close"].iloc[-1]
        ma20 = df["ma20"].iloc[-1]

        if current_price < ma20:
            signal = "GOOD_ENTRY"
            confidence = 70
            reasoning = f"Price below MA20 ({current_price:.2f} < {ma20:.2f})"

        elif current_price > ma20 * 1.08:
            signal = "OVEREXTENDED"
            confidence = 75
            reasoning = f"Price too high above MA20 ({current_price:.2f} > {ma20:.2f})"

        else:
            signal = "WAIT_FOR_PULLBACK"
            confidence = 60
            reasoning = f"Near average ({current_price:.2f} ≈ {ma20:.2f})"

        return {
            "agent_name": "Technical",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        }

    except Exception as e:
        return {
            "agent_name": "Technical",
            "signal": "WAIT_FOR_PULLBACK",
            "confidence": 50,
            "reasoning": str(e)
        }