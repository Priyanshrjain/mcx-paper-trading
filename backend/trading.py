LOT_SIZES = {
    "GOLD": 100,    # grams
    "SILVER": 30   # kg
}


def calculate_pnl(entry_price, current_price, lots, commodity, side):
    multiplier = LOT_SIZES.get(commodity, 1)

    if side == "BUY":
        return (current_price - entry_price) * multiplier * lots
    else:
        return (entry_price - current_price) * multiplier * lots
