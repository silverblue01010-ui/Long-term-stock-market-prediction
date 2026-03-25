import yfinance as yf

def sentiment_agent(symbol):
    """
    Simple keyword-based sentiment analysis using news headlines
    """

    try:
        stock = yf.Ticker(symbol)
        news = stock.news

        # No news case
        if not news or len(news) == 0:
            return {
                "agent_name": "Sentiment",
                "signal": "HOLD",
                "confidence": 50,
                "reasoning": "No recent news"
            }

        positive_keywords = ["growth", "profit", "gain", "upgrade", "strong", "beat"]
        negative_keywords = ["loss", "decline", "downgrade", "weak", "miss", "fall"]

        score = 0

        # Analyze top 10 news articles
        for article in news[:10]:
            title = article.get("title", "").lower()

            for word in positive_keywords:
                if word in title:
                    score += 1

            for word in negative_keywords:
                if word in title:
                    score -= 1

        # Decision logic
        if score > 2:
            signal = "BUY"
            confidence = 65
            reasoning = "Positive news sentiment"

        elif score < -2:
            signal = "SELL"
            confidence = 65
            reasoning = "Negative news sentiment"

        else:
            signal = "HOLD"
            confidence = 55
            reasoning = "Neutral sentiment"

        return {
            "agent_name": "Sentiment",
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning
        }

    except Exception as e:
        return {
            "agent_name": "Sentiment",
            "signal": "HOLD",
            "confidence": 50,
            "reasoning": f"Error: {str(e)}"
        }