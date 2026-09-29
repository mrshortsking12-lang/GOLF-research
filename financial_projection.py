#!/usr/bin/env python3
"""Five-year, three-statement equity model; Python standard library only.

Run the approved GOLF case: python financial_projection.py
Run the original classroom equations: python financial_projection.py assumptions.json
Get an input template: python financial_projection.py --template
Use --show-inputs to inspect the embedded GOLF inputs and their sources.
Rates are decimals (0.08 = 8%); monetary amounts must use one
consistent unit. Shares must use the corresponding unit for value per share.

Other working capital means other assets less other liabilities, excluding
the noncash impairment movement. With flat other liabilities, its annual
change is 0.008 times the change in revenue. Impairment reduces other assets,
not PP&E. The generic case assumes unlimited revolver capacity; GOLF uses
the disclosed facility limit less letters of credit. FCFE used for valuation
is before buybacks and revolver draws/repayments, as specified.

GOLF extensions explicitly model R&D, intangible/cloud amortization, ERP,
debt issuance costs, finance leases, minority claims and known dividends.
The approved 0.8% incremental working-capital convention remains a judgment.
This is a hindsight-informed classroom case valued at December 31, 2025,
not a current-date valuation or a reconstruction of actual 2026 results.
"""

import argparse
import json
import math
import sys


YEARS = tuple(range(2026, 2031))
INPUTS = None  # Optional custom generic dictionary; default is approved GOLF.
K25 = "https://www.sec.gov/Archives/edgar/data/1672013/000167201326000057/golf-20251231.htm"
Q26 = "https://www.sec.gov/Archives/edgar/data/1672013/000167201326000158/golf-20260630.htm"
RELEASE = "https://www.sec.gov/Archives/edgar/data/1672013/000167201326000157/ex991-q22026.htm"
OPENING_KEYS = (
    "cash", "inventory", "ppe", "other_assets", "floor_plan", "debt",
    "revolver", "other_liabilities", "equity",
)
ANNUAL_KEYS = (
    "growth", "gross_margin", "sga_ratio", "depreciation_ratio", "impairment",
    "floor_plan_rate", "debt_rate", "revolver_rate", "tax_rate",
    "inventory_days", "floor_plan_ratio", "capex", "repayment", "buyback",
)


def input_template():
    return {
        "prior_revenue": None,
        "opening": dict.fromkeys(OPENING_KEYS),
        "annual": {str(y): dict.fromkeys(ANNUAL_KEYS) for y in YEARS},
        "minimum_cash": None,
        "cost_of_equity": None,
        "terminal_growth": None,
        "share_count": None,
    }


def number(mapping, key, label):
    value = mapping.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label}.{key} must be a number")
    if not math.isfinite(value):
        raise ValueError(f"{label}.{key} must be finite")
    return float(value)


def balance_gap(bs):
    return (bs["cash"] + bs["inventory"] + bs["ppe"] + bs["other_assets"]
            - bs["floor_plan"] - bs["debt"] - bs["revolver"]
            - bs["other_liabilities"] - bs.get("redeemable_minority_interest", 0)
            - bs["equity"])


def assert_balanced(records, minimum_cash, tolerance=1e-6):
    """Raise with year and gap for an unbalanced BS or minimum-cash failure."""
    for record in records:
        year, bs = record["year"], record["bs"]
        gap = balance_gap(bs)
        if not math.isfinite(gap) or abs(gap) > tolerance:
            raise AssertionError(f"{year}: balance sheet gap = {gap:.10f}")
        cash_gap = bs["cash"] - minimum_cash
        if not math.isfinite(cash_gap) or cash_gap < -tolerance:
            raise AssertionError(f"{year}: cash less minimum gap = {cash_gap:.10f}")


def project(data):
    opening = {k: number(data["opening"], k, "opening") for k in OPENING_KEYS}
    gap = balance_gap(opening)
    if abs(gap) > 1e-6:
        raise AssertionError(f"2025 opening: balance sheet gap = {gap:.10f}")
    prior_revenue = number(data, "prior_revenue", "inputs")
    minimum = number(data, "minimum_cash", "inputs")
    if minimum < 0 or any(opening[k] < 0 for k in ("debt", "revolver", "floor_plan")):
        raise ValueError("Minimum cash and opening borrowing balances must be nonnegative")
    records = []
    for year in YEARS:
        a = {k: number(data["annual"][str(year)], k, str(year)) for k in ANNUAL_KEYS}
        if not 0 <= a["repayment"] <= opening["debt"]:
            raise ValueError(f"{year}: repayment must be between zero and opening debt")
        revenue = prior_revenue * (1 + a["growth"])
        gp = revenue * a["gross_margin"]
        sga = gp * a["sga_ratio"]
        dep = opening["ppe"] * a["depreciation_ratio"]
        impairment = a["impairment"]
        operating = gp - sga - dep - impairment
        interest = (opening["floor_plan"] * a["floor_plan_rate"]
                    + opening["debt"] * a["debt_rate"]
                    + opening["revolver"] * a["revolver_rate"])
        pretax = operating - interest
        tax = max(0, pretax) * a["tax_rate"]
        ni = pretax - tax
        bs = {
            "inventory": (revenue - gp) * a["inventory_days"] / 365,
            "ppe": opening["ppe"] + a["capex"] - dep,
            "other_assets": opening["other_assets"] + .008 * (revenue - prior_revenue) - impairment,
            "debt": opening["debt"] - a["repayment"],
            "other_liabilities": opening["other_liabilities"],
            "equity": opening["equity"] + ni - a["buyback"],
        }
        bs["floor_plan"] = bs["inventory"] * a["floor_plan_ratio"]
        d_inventory = bs["inventory"] - opening["inventory"]
        d_owc = (bs["other_assets"] - opening["other_assets"] + impairment
                 - (bs["other_liabilities"] - opening["other_liabilities"]))
        d_floor_plan = bs["floor_plan"] - opening["floor_plan"]
        fcfe = ni + dep + impairment - a["capex"] - d_inventory - d_owc + d_floor_plan - a["repayment"]
        cash_before_revolver = opening["cash"] + fcfe - a["buyback"]
        draw = max(0, minimum - cash_before_revolver)
        revolver_repayment = min(opening["revolver"], max(0, cash_before_revolver - minimum))
        bs["revolver"] = opening["revolver"] + draw - revolver_repayment
        bs["cash"] = cash_before_revolver + draw - revolver_repayment
        bs["total_assets"] = sum(bs[k] for k in ("cash", "inventory", "ppe", "other_assets"))
        bs["total_liabilities"] = sum(bs[k] for k in ("floor_plan", "debt", "revolver", "other_liabilities"))
        bs["liabilities_and_equity"] = bs["total_liabilities"] + bs["equity"]
        income = dict(revenue=revenue, cogs=revenue-gp, gross_profit=gp,
                      sga=sga, depreciation=dep, impairment=impairment,
                      operating_income=operating, interest=interest,
                      pretax_income=pretax, tax=tax, net_income=ni)
        cf = dict(net_income=ni, depreciation=dep, impairment=impairment,
                  capex=-a["capex"], inventory_change=-d_inventory,
                  other_working_capital_change=-d_owc, floor_plan_change=d_floor_plan,
                  debt_repayment=-a["repayment"], fcfe=fcfe,
                  buyback=-a["buyback"], revolver_draw=draw,
                  revolver_repayment=-revolver_repayment,
                  cash_change=bs["cash"]-opening["cash"],
                  opening_cash=opening["cash"], closing_cash=bs["cash"])
        record = dict(year=year, income=income, bs=bs, cf=cf)
        records.append(record)
        assert_balanced([record], minimum)
        opening, prior_revenue = bs, revenue
    return records


def golf_inputs():
    """Approved historical anchors and explicitly labeled forecast judgments.

    No new share-price target, CAPM estimate or future buyback price is assumed.
    Known 2026 distributions are included; additional distributions are zero
    in this scenario, not predictions of the company's capital-return policy.
    Cloud amortization stays proportional to gross profit at its historical
    embedded SG&A ratio, avoiding an invented in-service date/useful life.
    """
    annual = {}
    revenue = 2558.730
    for i, year in enumerate(YEARS):
        growth = [2662.5 / 2558.730 - 1, .04, .035, .03, .025][i]
        revenue *= 1 + growth
        annual[str(year)] = {
            "growth": growth,
            "gross_margin": .477,
            "sga_ratio": 833.419 / 1221.254,
            "rd_to_gross_profit": 76.506 / 1221.254,
            # Total PP&E depreciation embedded across reported costs is
            # removed at its historical GP ratio, then reforecast explicitly.
            "embedded_depreciation_to_gp": 43.4 / 1221.254,
            "embedded_cloud_amortization_to_gp": 2.4 / 1221.254,
            "depreciation_ratio": .133,
            "intangible_amortization": [8.449, 7.605, 6.978, 6.962, 6.962][i],
            "impairment": 0.0,
            "inventory_days": [170, 168, 166, 166, 166][i],
            "capex": 95.0 if year == 2026 else .035 * revenue,
            "erp_investment": [25.0, 15.0, 10.0, 5.0, 5.0][i],
            "other_working_capital_ratio": .008,
            "note_coupon": .05625,
            "note_effective_rate": .05788,
            "local_facility_rate": .0126,
            "other_term_rate": .055,
            "revolver_rate": .0488,
            "term_repayment": [.660, .715, .693, .027, 0.0][i],
            "lease_cash_payment": [.616, .514, .306, .118, .005][i],
            "tax_rate": .23,
            "buyback": 26.003 if year == 2026 else 0.0,
            "dividend": 30.766 if year == 2026 else 0.0,
        }
    return {
        "model": "golf",
        "prior_revenue": 2558.730,
        "opening": {
            "cash": 48.7, "inventory": 608.571, "ppe": 356.575,
            "other_assets": 1328.853, "floor_plan": 0.0,
            "debt": 512.159, "revolver": 431.301,
            "other_liabilities": 613.903,
            "redeemable_minority_interest": 1.770, "equity": 783.566,
        },
        "opening_schedules": {
            "notes_principal": 500.0, "local_facility_principal": 16.005,
            "other_term_principal": 2.095, "finance_lease_principal": 1.433,
            "unamortized_note_costs": 7.374,
            "cloud_assets": 57.3, "amortizing_intangibles": 82.379,
        },
        "annual": annual,
        "minimum_cash": 50.0,
        "revolver_limit_after_letters_of_credit": 946.0,
        "cost_of_equity": .10,
        "terminal_growth": .025,
        "share_count": 58.371822,
        "assumption_notes": [
            "USD millions; shares in millions. Opening unrestricted cash is rounded.",
            "History: 2025 opening balances, debt principal, coupons and note yield; " + K25,
            "Guidance: 2026 revenue midpoint 2662.5; " + RELEASE,
            "Guidance: 2026 physical capex 95 plus ERP 25; " + Q26,
            "History: 2026 first-half buybacks 26.003 and dividends 30.766; " + Q26,
            "No additional buybacks/dividends are assumed; these are known-distribution "
            "floors, not a forecast that the company stops returning capital.",
            "History: latest observed revolver/local rates 4.88%/1.26%; holding them "
            "constant is judgment. The 5.5% proxy applies only to small other-term debt.",
            "Guidance: intangible amortization follows 2025 Note 9; lease payments "
            "follow Note 4; the lease yield is calculated for annual end-year timing.",
            "Judgment: 47.7% margin, 13.3% PP&E depreciation, 23% tax, 170/168/166 "
            "inventory days, growth fade, future capex 3.5% of sales and ERP taper.",
            "Reported SG&A and R&D ratios use 2025. Embedded depreciation is removed "
            "before the explicit charge; cloud amortization remains embedded in SG&A.",
            "Judgment: incremental noninventory working capital is 0.8% of sales change; "
            "other assets/liabilities otherwise flat except explicit schedules.",
            "Judgment: no impairment, minimum cash 50, local debt rolled over, remaining "
            "revolver refinanced in 2030 subject to the unchanged 946 net facility cap.",
            "Judgment: 10% required equity return and 2.5% terminal growth; not CAPM estimates.",
            "58.371822 is a fixed opening basic-share proxy, not future diluted shares. "
            "The model does not forecast issuance, repurchase prices or dilution.",
            "Redeemable minority claim is held flat; projected net income is assigned "
            "to common equity. No minority income or distributions are forecast.",
            "Other omissions: cash FX, OCI, stock issuance, nonrecurring tariff refunds, "
            "and financing-fee movements outside the separately modeled note costs.",
            "December 31, 2025 discount base with later information: classroom valuation.",
            "FCFE and terminal formula follow the requested convention; revolver draws "
            "and sweeps affect cash/debt and subsequent interest, but are outside FCFE.",
        ],
    }


def lease_yield(principal, payments):
    """Annual end-period yield implied by disclosed lease balance/payments."""
    if principal <= 0 or any(p < 0 for p in payments) or sum(payments) < principal:
        raise ValueError("Lease schedule requires positive principal and sufficient payments")
    low, high = 0.0, 1.0
    def pv(rate):
        return sum(p / (1 + rate) ** t for t, p in enumerate(payments, 1))
    while pv(high) > principal:
        high *= 2
    for _ in range(100):
        mid = (low + high) / 2
        if pv(mid) > principal:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def project_golf(data):
    """Extended GOLF case; project() preserves the original generic equations."""
    opening = {k: number(data["opening"], k, "opening") for k in OPENING_KEYS}
    opening["redeemable_minority_interest"] = number(
        data["opening"], "redeemable_minority_interest", "opening")
    if abs(balance_gap(opening)) > 1e-6:
        raise AssertionError(f"2025 opening: balance sheet gap = {balance_gap(opening):.10f}")
    schedule = {k: number(data["opening_schedules"], k, "opening_schedules")
                for k in data["opening_schedules"]}
    debt_keys = ("notes_principal", "local_facility_principal",
                 "other_term_principal", "finance_lease_principal")
    if abs(sum(schedule[k] for k in debt_keys) - schedule["unamortized_note_costs"]
           - opening["debt"]) > 1e-6:
        raise ValueError("Opening debt principal/carrying-value reconciliation failed")
    lease_rate = lease_yield(schedule["finance_lease_principal"],
                            [data["annual"][str(y)]["lease_cash_payment"] for y in YEARS])
    minimum = number(data, "minimum_cash", "inputs")
    limit = number(data, "revolver_limit_after_letters_of_credit", "inputs")
    prior_revenue = number(data, "prior_revenue", "inputs")
    records = []
    for year in YEARS:
        a = {k: number(data["annual"][str(year)], k, str(year))
             for k in data["annual"][str(year)]}
        revenue = prior_revenue * (1 + a["growth"])
        gp = revenue * a["gross_margin"]
        sga = gp * a["sga_ratio"]
        rd = gp * a["rd_to_gross_profit"]
        embedded_dep = gp * a["embedded_depreciation_to_gp"]
        dep = opening["ppe"] * a["depreciation_ratio"]
        intangible_amort = min(schedule["amortizing_intangibles"], a["intangible_amortization"])
        cloud_amort = gp * a["embedded_cloud_amortization_to_gp"]
        if cloud_amort > schedule["cloud_assets"]:
            raise ValueError(f"{year}: embedded cloud amortization exceeds opening cloud assets")
        impairment = a["impairment"]
        operating = gp - sga - rd + embedded_dep - dep - intangible_amort - impairment

        note_cash_interest = schedule["notes_principal"] * a["note_coupon"]
        note_book_interest = ((schedule["notes_principal"] - schedule["unamortized_note_costs"])
                              * a["note_effective_rate"])
        fee_amort = min(schedule["unamortized_note_costs"],
                        max(0.0, note_book_interest - note_cash_interest))
        lease_interest = schedule["finance_lease_principal"] * lease_rate
        local_interest = schedule["local_facility_principal"] * a["local_facility_rate"]
        term_interest = schedule["other_term_principal"] * a["other_term_rate"]
        revolver_interest = opening["revolver"] * a["revolver_rate"]
        cash_interest = note_cash_interest + local_interest + term_interest + lease_interest + revolver_interest
        interest = cash_interest + fee_amort
        pretax = operating - interest
        tax = max(0.0, pretax) * a["tax_rate"]
        ni = pretax - tax

        lease_principal_paid = a["lease_cash_payment"] - lease_interest
        if not -1e-8 <= lease_principal_paid <= schedule["finance_lease_principal"] + 1e-8:
            raise ValueError(f"{year}: invalid finance-lease principal payment")
        lease_principal_paid = max(0.0, min(lease_principal_paid, schedule["finance_lease_principal"]))
        if not 0 <= a["term_repayment"] <= schedule["other_term_principal"] + 1e-8:
            raise ValueError(f"{year}: term repayment exceeds opening principal")
        repayment = a["term_repayment"] + lease_principal_paid
        next_schedule = dict(schedule)
        next_schedule["other_term_principal"] = max(0.0, schedule["other_term_principal"] - a["term_repayment"])
        next_schedule["finance_lease_principal"] = max(0.0, schedule["finance_lease_principal"] - lease_principal_paid)
        next_schedule["unamortized_note_costs"] -= fee_amort
        next_schedule["amortizing_intangibles"] -= intangible_amort
        next_schedule["cloud_assets"] += a["erp_investment"] - cloud_amort

        d_owc = a["other_working_capital_ratio"] * (revenue - prior_revenue)
        bs = {
            "cash": 0.0,
            "inventory": (revenue - gp) * a["inventory_days"] / 365,
            "ppe": opening["ppe"] + a["capex"] - dep,
            "other_assets": (opening["other_assets"] + d_owc + a["erp_investment"]
                             - intangible_amort - cloud_amort - impairment),
            "floor_plan": 0.0,
            "debt": sum(next_schedule[k] for k in debt_keys) - next_schedule["unamortized_note_costs"],
            "revolver": 0.0,
            "other_liabilities": opening["other_liabilities"],
            "redeemable_minority_interest": opening["redeemable_minority_interest"],
            "equity": opening["equity"] + ni - a["buyback"] - a["dividend"],
        }
        d_inventory = bs["inventory"] - opening["inventory"]
        fcfe = (ni + dep + intangible_amort + cloud_amort + fee_amort + impairment
                - a["capex"] - a["erp_investment"] - d_inventory - d_owc - repayment)
        cash_before_revolver = opening["cash"] + fcfe - a["buyback"] - a["dividend"]
        draw = max(0.0, minimum - cash_before_revolver)
        sweep = min(opening["revolver"], max(0.0, cash_before_revolver - minimum))
        bs["revolver"] = opening["revolver"] + draw - sweep
        if bs["revolver"] > limit + 1e-6:
            raise ValueError(f"{year}: revolver capacity gap = {limit - bs['revolver']:.10f}")
        bs["cash"] = cash_before_revolver + draw - sweep
        bs["total_assets"] = sum(bs[k] for k in ("cash", "inventory", "ppe", "other_assets"))
        bs["total_liabilities"] = sum(bs[k] for k in ("floor_plan", "debt", "revolver", "other_liabilities"))
        bs["liabilities_claims_and_equity"] = bs["total_liabilities"] + bs["redeemable_minority_interest"] + bs["equity"]
        income = dict(revenue=revenue, cogs=revenue-gp, gross_profit=gp,
                      sga=sga, research_and_development=rd,
                      embedded_depreciation_reversal=-embedded_dep,
                      depreciation=dep, intangible_amortization=intangible_amort,
                      impairment=impairment, operating_income=operating,
                      interest=interest, pretax_income=pretax, tax=tax, net_income=ni)
        cf = dict(net_income=ni, depreciation=dep, intangible_amortization=intangible_amort,
                  cloud_amortization=cloud_amort, debt_cost_amortization=fee_amort,
                  impairment=impairment, capex=-a["capex"], erp_investment=-a["erp_investment"],
                  inventory_change=-d_inventory, other_working_capital_change=-d_owc,
                  floor_plan_change=0.0, debt_repayment=-repayment, fcfe=fcfe,
                  buyback=-a["buyback"], dividends=-a["dividend"],
                  revolver_draw=draw, revolver_repayment=-sweep,
                  cash_change=bs["cash"]-opening["cash"],
                  opening_cash=opening["cash"], closing_cash=bs["cash"])
        supporting = dict(next_schedule)
        supporting.update(note_cash_interest=note_cash_interest,
                          local_interest=local_interest, term_interest=term_interest,
                          lease_interest=lease_interest, revolver_interest=revolver_interest,
                          cash_interest=cash_interest, debt_cost_amortization=fee_amort,
                          term_principal_paid=a["term_repayment"],
                          lease_principal_paid=lease_principal_paid,
                          lease_cash_payment=a["lease_cash_payment"],
                          revolver_headroom=limit-bs["revolver"])
        record = dict(year=year, income=income, bs=bs, cf=cf, schedules=supporting)
        assert_balanced([record], minimum)
        records.append(record)
        opening, schedule, prior_revenue = bs, next_schedule, revenue
    return records


def print_table(title, records, section):
    rows = list(records[0][section])
    label_width = max(32, max(len(k.replace("_", " ")) for k in rows))
    width = max(14, max(len(f"{r[section][k]:,.1f}") + 2 for r in records for k in rows))
    print("\n" + title)
    print(" " * label_width + "".join(f"{r['year']:>{width}}" for r in records))
    for key in rows:
        label = {"ppe": "PP&E", "sga": "SG&A", "cogs": "COGS", "fcfe": "FCFE",
                 "erp_investment": "ERP investment"}.get(key, key.replace("_", " ").capitalize())
        values = [0.0 if abs(r[section][key]) < .05 else r[section][key] for r in records]
        print(f"{label:<{label_width}}" + "".join(f"{v:>{width},.1f}" for v in values))


def valuation(data, records):
    if tuple(r["year"] for r in records) != YEARS:
        raise ValueError("Valuation requires exactly the five years 2026 through 2030")
    assert_balanced(records, number(data, "minimum_cash", "inputs"))
    rate = number(data, "cost_of_equity", "inputs")
    growth = number(data, "terminal_growth", "inputs")
    shares = number(data, "share_count", "inputs")
    if rate <= -1 or growth <= -1 or rate <= growth or shares <= 0:
        raise ValueError("Require cost of equity > terminal growth > -1 and share count > 0")
    pv_fcfe = sum(r["cf"]["fcfe"] / (1 + rate) ** t for t, r in enumerate(records, 1))
    last = records[-1]["cf"]
    terminal = (last["fcfe"] - last["debt_repayment"]) * (1 + growth) / (rate - growth)
    pv_terminal = terminal / (1 + rate) ** 5
    equity_value = pv_fcfe + pv_terminal
    print(f"\nPV of 2026-2030 FCFE: {pv_fcfe:,.2f}")
    print(f"PV of terminal value: {pv_terminal:,.2f}")
    print(f"\nEquity value: {equity_value:,.2f}")
    share = f"{pv_terminal / equity_value:.2%}" if equity_value != 0 else "undefined (zero equity value)"
    print(f"Share of value after 2030: {share}")
    print(f"Value per share: {equity_value / shares:,.2f}")
    return equity_value, pv_terminal, equity_value / shares


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("assumptions", nargs="?", help="JSON input file; use - for stdin")
    parser.add_argument("--template", action="store_true", help="print the required JSON input template")
    parser.add_argument("--show-inputs", action="store_true", help="print input values, assumptions and source URLs")
    parser.add_argument("--schedules", action="store_true", help="also print GOLF supporting debt and asset schedules")
    args = parser.parse_args()
    if args.template:
        print(json.dumps(input_template(), indent=2))
        return
    if args.assumptions == "-":
        data = json.load(sys.stdin)
    elif args.assumptions:
        with open(args.assumptions, encoding="utf-8") as source:
            data = json.load(source)
    elif INPUTS is not None:
        data = INPUTS
    else:
        data = golf_inputs()
    if args.show_inputs:
        print(json.dumps(data, indent=2))
        return
    is_golf = data.get("model") == "golf"
    if is_golf:
        print("GOLF: approved classroom case; USD millions except per-share values.")
        print("Discount base: December 31, 2025, using later 2026 evidence (not a current-date valuation).")
        print("No floor plan. Minimum cash 50.0; cost of equity 10%; terminal growth 2.5%.")
        print("Known distributions only: 2026 buybacks 26.003 and dividends 30.766; additional distributions assumed zero.")
        print("Fixed opening basic-share proxy: 58.371822 million; no projected dilution/share-count change.")
        print("Other working capital uses the approved 0.8% classroom convention; it is not calibrated guidance.")
        print("Expense reversal removes historical embedded depreciation before the explicit depreciation charge.")
        print("See --show-inputs for all source URLs, judgments and limitations.")
    records = project_golf(data) if is_golf else project(data)
    print_table("INCOME STATEMENT (expenses shown positive)", records, "income")
    print_table("BALANCE SHEET", records, "bs")
    print_table("CASH FLOW (outflows shown negative)", records, "cf")
    if is_golf and args.schedules:
        print_table("SUPPORTING DEBT AND ASSET SCHEDULES", records, "schedules")
    print("\nANNUAL CHECKS")
    for r in records:
        gap = balance_gap(r["bs"])
        if abs(gap) < 1e-6:
            gap = 0.0
        cash_gap = r["bs"]["cash"] - data["minimum_cash"]
        claims_label = " - minority claim" if is_golf else ""
        print(f"{r['year']}: assets - liabilities{claims_label} - equity = {gap:.1f}; "
              f"cash - minimum = {cash_gap:.1f}; "
              f"minimum cash met: {'PASS' if cash_gap >= -1e-6 else 'FAIL'}")
    assert_balanced(records, data["minimum_cash"])
    valuation(data, records)


if __name__ == "__main__":
    main()
