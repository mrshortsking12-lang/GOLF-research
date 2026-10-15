"""Check candidate reserve allocations. All weights are percentage points."""

from collections import defaultdict
from math import isclose


# Editable inputs
HOLDINGS = [
    # Holding, issuer, business days to redeem, reserve-eligible
    ("Cash", "none", 0, True),
    ("Treasury bills", "U.S. Treasury", 1, True),
    ("Treasury 10-year note", "U.S. Treasury", 1, True),
    ("Global equity index fund", "diversified fund", 2, False),
    ("Investment-grade bond fund", "diversified fund", 3, False),
    ("Private real estate fund", "diversified fund", 90, False),
    ("Acme Corp bonds", "Acme Corp", 4, False),
    ("Acme Corp stock", "Acme Corp", 1, False),
]

# Weights in percent, in the same order as HOLDINGS.
CANDIDATES = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
}

RESERVE_SIZE = 100  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5  # Business days
MINIMUM_LIQUID_SHARE = 90  # Percent
ISSUER_LIMIT = 8  # Percent
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def main():
    reserve_minimum = (
        QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    )
    print(f"Reserve minimum: {reserve_minimum:.1f}%")

    for candidate, weights in CANDIDATES.items():
        if len(weights) != len(HOLDINGS):
            raise ValueError(f"Candidate {candidate} needs one weight per holding")

        eligible_weight = 0
        liquid_weight = 0
        company_weights = defaultdict(float)
        for (_, issuer, days, eligible), weight in zip(HOLDINGS, weights):
            if eligible:
                eligible_weight += weight
            if days <= LIQUIDITY_WINDOW:
                liquid_weight += weight
            if issuer not in EXEMPT_ISSUERS:
                company_weights[issuer] += weight

        total = sum(weights)
        lowest = min(weights)
        largest_company = max(company_weights.values(), default=0)
        checks = [
            ("Weights sum to 100", total,
             isclose(total, 100, rel_tol=0, abs_tol=1e-9)),
            ("Lowest weight (long-only)", lowest, lowest >= 0),
            ("Reserve-eligible weight", eligible_weight,
             eligible_weight >= reserve_minimum),
            (f"Weight redeemable within {LIQUIDITY_WINDOW} business days",
             liquid_weight, liquid_weight >= MINIMUM_LIQUID_SHARE),
            ("Largest single company", largest_company,
             largest_company <= ISSUER_LIMIT),
        ]

        print(f"\nCandidate {candidate}")
        for label, measured, passed in checks:
            print(f"{label}: {measured:.1f}% — {'pass' if passed else 'FAIL'}")
        print("Calendar-year loss rule: requires CIO clarification")
        failures = sum(not passed for _, _, passed in checks)
        print(
            "passes every checkable rule"
            if failures == 0
            else f"fails {failures} rule(s)"
        )


if __name__ == "__main__":
    main()
