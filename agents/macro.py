import yfinance as yf
import pandas as pd

def macro_agent():
    try:
        data = yf.Ticker("^NSEI").history(period="3mo")

        if len(data) < 50:
            return {
                "agent_name": "Macro",
                "signal": "HOLD",
                "confidence": 50,
                "reasoning": "Not enough market data"
            }

        data["ma50"] = data["Close"].rolling(50).mean()

        current = data["Close"].iloc[-1]
        ma50 = data["ma50"].iloc[-1]

        if current > ma50:
            signal = "BUY"
            confidence = 70
            reasoning = f"Market uptrend ({current:.0f} > {ma50:.0f})"
        else:
            signal = "SELL"
            confidence = 70
            reasoning = f"Market downtrend ({current:.0f} < {ma50:.0f})"

        return {
            "agent_name": "Macro",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        }

    except Exception as e:
        return {
            "agent_name": "Macro",
            "signal": "HOLD",
            "confidence": 50,
            "reasoning": str(e)
        }