def score_color(score):
    if score >= 75:
        return "#2ECC71"  # Green
    elif score >= 65:
        return "#F1C40F"  # Yellow
    elif score >= 55:
        return "#E67E22"  # Orange
    else:
        return "#E74C3C"  # Red
