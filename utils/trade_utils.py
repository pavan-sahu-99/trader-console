import pandas as pd
def calculate_risk(entry_price, stop_loss, qty):
    """
    Calculate trade risk in ₹
    """
    return abs(entry_price - stop_loss) * qty

def calculate_reward(entry_price, target_price, qty):
    """
    Calculate potential reward in ₹
    """
    return abs(target_price - entry_price) * qty

def calculate_rr_ratio(entry_price, stop_loss, target_price):
    """
    Calculate R:R ratio
    """
    risk = abs(entry_price - stop_loss)
    reward = abs(target_price - entry_price)
    if risk == 0:
        return None
    return round(reward / risk, 2)

def execution_score(row):
    """
    Score the trade execution quality: 
    - Followed plan: 1 point
    - Emotion under 3: 1 point
    - Notes filled: 1 point
    """
    score = 0
    if row["followed_plan"] == "Yes":
        score += 1
    if row["emotion_score"] <= 3:
        score += 1
    if isinstance(row["notes"], str) and len(row["notes"].strip()) > 0:
        score += 1
    return score
