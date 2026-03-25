import pandas as pd
from database.db import get_connection

def risk_agent(symbol):
    try:
        conn = get_connection()

        query = """
        SELECT date, close FROM stock_prices
        WHERE symbol = %s
        ORDER BY date;
        """

        df = pd.read_sql(query, conn, params=(symbol,))
        conn.close()

        if df.empty:
            return {
                "agent_name": "Risk",
                "signal": "HOLD",
                "confidence": 50,
                "reasoning": "No data found in DB"
            }

        df["returns"] = df["close"].pct_change()
        volatility = df["returns"].std()

        if volatility > 0.03:
            signal = "SELL"
            confidence = 70
            reasoning = f"High volatility ({volatility:.4f})"
        elif volatility > 0.015:
            signal = "HOLD"
            confidence = 60
            reasoning = f"Moderate volatility ({volatility:.4f})"
        else:
            signal = "BUY"
            confidence = 70
            reasoning = f"Low volatility ({volatility:.4f})"

        return {
            "agent_name": "Risk",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        }

    except Exception as e:
        return {
            "agent_name": "Risk",
            "signal": "HOLD",
            "confidence": 50,
            "reasoning": str(e)
        }