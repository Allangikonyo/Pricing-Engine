# engine/elasticity.py
# Calculates price elasticity and demand signals

def calculate_elasticity(old_price, new_price, old_units, new_units):
    """
    Price Elasticity of Demand = % change in quantity / % change in price
    Result tells us how sensitive buyers are to price changes.
    """
    if old_price == 0 or old_units == 0:
        return None

    percent_change_price = (new_price - old_price) / old_price
    percent_change_demand = (new_units - old_units) / old_units

    if percent_change_price == 0:
        return None

    elasticity = percent_change_demand / percent_change_price
    return round(elasticity, 2)


def interpret_elasticity(elasticity):
    """
    Turns the elasticity number into a plain-English label.
    """
    if elasticity is None:
        return "unknown"
    
    elasticity = abs(elasticity)

    if elasticity > 2:
        return "highly elastic"       # buyers are very price sensitive
    elif elasticity > 1:
        return "elastic"              # buyers are somewhat price sensitive
    elif elasticity == 1:
        return "unit elastic"
    else:
        return "inelastic"            # buyers don't react much to price changes


def get_margin(price, cost):
    """
    Calculates profit margin as a percentage.
    """
    if price == 0:
        return 0
    margin = (price - cost) / price * 100
    return round(margin, 2)