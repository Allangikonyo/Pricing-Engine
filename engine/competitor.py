# engine/competitor.py
# Analyzes competitor pricing and your market position

def analyze_competitors(your_price, competitor_prices):
    """
    Takes your price and a list of competitor prices.
    Returns key stats about your market position.
    """
    if not competitor_prices:
        return None

    avg_competitor_price = round(sum(competitor_prices) / len(competitor_prices), 2)
    lowest_competitor = min(competitor_prices)
    highest_competitor = max(competitor_prices)

    price_gap = round(your_price - avg_competitor_price, 2)
    price_gap_percent = round((price_gap / avg_competitor_price) * 100, 2)

    position = get_market_position(price_gap_percent)

    return {
        "avg_competitor_price": avg_competitor_price,
        "lowest_competitor": lowest_competitor,
        "highest_competitor": highest_competitor,
        "price_gap": price_gap,
        "price_gap_percent": price_gap_percent,
        "position": position
    }


def get_market_position(price_gap_percent):
    """
    Turns the price gap into a plain-English market position label.
    """
    if price_gap_percent > 10:
        return "priced above market"
    elif price_gap_percent < -10:
        return "priced below market"
    else:
        return "priced at market"