import yfinance as yf

def fundamental_agent(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        pe = info.get("trailingPE", None)
        roe = info.get("returnOnEquity", None)

        # Safety check
        if pe is None:
            return {
                "agent_name": "Fundamental",
                "signal": "HOLD",
                "confidence": 50,
                "reasoning": "PE not available"
            }

        # Logic
        if pe < 25:
            signal = "BUY"
            confidence = 75
            reasoning = f"Good valuation (PE={pe:.2f})"

        elif pe < 40:
            signal = "HOLD"
            confidence = 60
            reasoning = f"Fair valuation (PE={pe:.2f})"

        else:
            signal = "SELL"
            confidence = 70
            reasoning = f"Overvalued (PE={pe:.2f})"

        # Add ROE insight if available
        if roe is not None:
            reasoning += f", ROE={roe:.2f}"

        return {
            "agent_name": "Fundamental",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        }

    except Exception as e:
        return {
            "agent_name": "Fundamental",
            "signal": "HOLD",
            "confidence": 50,
            "reasoning": str(e)
        }