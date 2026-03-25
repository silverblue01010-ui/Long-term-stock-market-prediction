import re


def score_signal(signal):
    if signal in ["BUY", "GOOD_ENTRY"]:
        return 1
    elif signal in ["HOLD", "WAIT_FOR_PULLBACK"]:
        return 0
    elif signal in ["SELL", "OVEREXTENDED"]:
        return -1
    return 0


def extract_entry_price(reasoning):
    """
    Safely extract entry price from reasoning string.
    Example expected format: "Breakout near (105 < resistance)"
    """
    try:
        match = re.search(r"\((\d+\.?\d*)", reasoning or "")
        if match:
            return float(match.group(1))
    except:
        pass
    return 0


def aggregate_decision(fundamental, risk, technical, macro=None, sentiment=None):

    # 🚨 HARD RULE: Macro override
    if macro and macro.get("signal") == "SELL":
        return {
            "final_decision": "HOLD",
            "confidence_score": 40,
            "entry_strategy": "WAIT",
            "position_size": "0%",
            "stop_loss": None,
            "target_levels": [],
            "reasoning_summary": "Market in downtrend - avoid buying"
        }

    # Safe defaults
    macro_score = score_signal(macro.get("signal")) if macro else 0
    sentiment_score = score_signal(sentiment.get("signal")) if sentiment else 0

    # Individual scores
    f_score = score_signal(fundamental.get("signal"))
    r_score = score_signal(risk.get("signal"))
    t_score = score_signal(technical.get("signal"))

    # Weighted scoring
    total_score = (
        f_score * 0.4 +
        macro_score * 0.3 +
        sentiment_score * 0.1 +
        t_score * 0.1 +
        r_score * 0.1
    )

    # Final decision
    if total_score > 0.5:
        decision = "BUY"
    elif total_score < -0.3:
        decision = "SELL"
    else:
        decision = "HOLD"

    # 📊 Extract entry price safely
    entry_price = extract_entry_price(technical.get("reasoning", ""))

    # 💰 Position sizing (dynamic)
    if decision == "BUY":
        if total_score > 0.7:
            position_size = "40% of capital"
        else:
            position_size = "25-30% of capital"
    elif decision == "HOLD":
        position_size = "10-20% of capital"
    else:
        position_size = "0-10% of capital"

    # 🛑 Stop loss & 🎯 Target
    if entry_price > 0:
        stop_loss = round(entry_price * 0.93, 2)   # ~7% downside
        target = round(entry_price * 1.15, 2)      # ~15% upside
        targets = [target]
    else:
        stop_loss = None
        targets = []

    return {
        "final_decision": decision,
        "confidence_score": round((total_score + 1) * 50, 2),
        "entry_strategy": technical.get("signal"),
        "position_size": position_size,
        "stop_loss": stop_loss,
        "target_levels": targets,
        "reasoning_summary": "Weighted multi-agent decision with risk control"
    }