"""Peer P/E valuation. Run with: python3 peer_pe.py"""

# EDIT INPUTS HERE. Use matching currencies and diluted-EPS periods.
# None means missing. Replace the example peer tickers with your chosen peers.
# Prices and diluted EPS are per share; no cash/debt adjustment is used.
TARGET = {"ticker": "GOLF", "price": None, "diluted_eps": None}
PEERS = [
    {"ticker": "PEER_A", "price": None, "diluted_eps": None},
    {"ticker": "PEER_B", "price": None, "diluted_eps": None},
    {"ticker": "PEER_C", "price": None, "diluted_eps": None},
]

import math
from statistics import median


def positive(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value > 0
    )


def ticker(company):
    return str(company.get("ticker") or "").strip().upper()


def pe(company):
    price = company.get("price")
    eps = company.get("diluted_eps")
    if not positive(price) or not positive(eps):
        return None
    multiple = price / eps
    return multiple if positive(multiple) else None


def main():
    target_ticker = ticker(TARGET)
    target_eps = TARGET.get("diluted_eps")
    target_pe = pe(TARGET)
    print(f"Target: {target_ticker or '(missing ticker)'}")
    print(
        f"Target P/E: {target_pe:.6f}x"
        if target_pe is not None
        else "Target P/E: not meaningful (missing, nonpositive, or invalid price/EPS)"
    )

    # Match tickers without regard to case or surrounding whitespace.
    # Keep the first occurrence of a peer, even if its data are invalid.
    peers = []
    seen = set()
    for company in PEERS:
        symbol = ticker(company)
        if not symbol:
            print("Excluded peer: missing ticker")
        elif symbol == target_ticker:
            print(f"Excluded target from peers: {symbol}")
        elif symbol in seen:
            print(f"Excluded duplicate peer: {symbol} (first occurrence retained)")
        else:
            seen.add(symbol)
            peers.append((symbol, pe(company)))

    print("\nPeer P/E multiples")
    for symbol, multiple in peers:
        if multiple is None:
            print(f"{symbol}: not meaningful (missing, nonpositive, or invalid price/EPS)")
        else:
            print(f"{symbol}: {multiple:.6f}x")

    valid = [multiple for _, multiple in peers if multiple is not None]
    full_estimate = None
    print(f"\nValid peers: {len(valid)}")
    if not valid:
        print("No usable peers. Peer median P/E and implied prices: not meaningful.")
    else:
        middle = median(valid)
        print(f"Peer median P/E: {middle:.6f}x")
        if not positive(target_eps):
            print("Implied prices: not meaningful (missing, nonpositive, or invalid target EPS).")
            if len(valid) == 1:
                print("One valid peer: reference multiple only; no range.")
        else:
            full_estimate = middle * target_eps
            if len(valid) == 1:
                print(f"Reference estimate (one valid peer): ${full_estimate:.2f}; no range.")
            else:
                for label, multiple in [("Minimum", min(valid)), ("Median", middle), ("Maximum", max(valid))]:
                    print(f"{label} peer P/E: {multiple:.6f}x; implied price: ${multiple * target_eps:.2f}")

    print("\nLeave-one-peer-out analysis")
    print("Dollar change = remaining median-implied price minus full-peer estimate.")
    for removed, _ in peers:
        remaining = [multiple for symbol, multiple in peers if symbol != removed and multiple is not None]
        if not remaining:
            print(f"Remove {removed}: no estimate (no usable peers remain); dollar change: not meaningful.")
        elif not positive(target_eps):
            print(f"Remove {removed}: implied price and dollar change not meaningful (invalid target EPS).")
        else:
            estimate = median(remaining) * target_eps
            change = estimate - full_estimate  # Round only when displaying.
            note = " (one remaining peer; reference estimate)" if len(remaining) == 1 else ""
            print(f"Remove {removed}: ${estimate:.2f}; dollar change: {change:+.2f} dollars{note}")
    if not peers:
        print("No peers to remove.")


if __name__ == "__main__":
    main()
