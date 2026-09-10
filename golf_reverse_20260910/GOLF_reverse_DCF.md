# GOLF full reverse discounted cash flow

Valuation date: September 10, 2026. All amounts are USD millions except share prices. This report updates the earlier September 8 analysis.

At **$85.29 per share**, this model requires **14.43% annual revenue growth for five years**, reaching **$5,223.1 million** of sales. This is a conditional requirement, not a prediction.

A reverse DCF starts with the share price and solves for the growth needed to support it, holding other assumptions fixed.

## Historical foundation

Read directly from the downloaded [2025 10-K](../../GOLF/golf%2010k%20HTML.html). Corresponding [SEC 10-K](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000057/golf-20251231.htm).

| Reported measure | Value |
|---|---:|
| 2023 revenue | $2,382.0 |
| 2024 revenue | $2,457.1 |
| 2025 revenue | $2,558.7 |
| 2025 revenue growth | 4.1% |
| 2023–2025 revenue CAGR | 3.6% |
| 2025 operating income | $299.4 |
| 2025 operating margin | 11.7% |
| Depreciation and amortization | $55.3 |
| Physical capex | $74.3 |
| Capitalized ERP investment | $38.2 |
| Operating cash flow | $194.4 |
| Effective tax rate | 21.9% |

Operating cash flow less physical capex was $120.0 million. It is after interest and includes ERP spending, so it is not unlevered free cash flow.

## Updated information and assumptions

The starting revenue run rate is $2,662.5 million, the midpoint of [2026 revenue guidance](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000157/ex991-q22026.htm). Guidance includes approximately $30 million of tariff refunds; recurring margins in this model do not assume refunds continue. The [$85.29 quote](https://stockanalysis.com/stocks/golf/history/) is dated September 10, 2026 and is not a live quote.

| Assumption | Value |
|---|---|
| Forecast period | Five normalized forward annual periods |
| Revenue growth | Solve for constant annual growth |
| EBIT margins | 12.50%, 12.75%, 13.00%, 13.25%, 13.50% |
| Tax rate | 23.0% |
| D&A / sales | 2.2%, rounded from 2025 actual ratio |
| Physical capex / sales | 3.5% |
| Additional NWC / incremental sales | 20% |
| Additional net ERP investment | $25, $15, $10, $5, $5 |
| WACC | 8.5%, assumed rather than estimated using CAPM |
| Terminal revenue growth | 2.5% |
| Terminal EBIT margin | 13.5% |
| Discount timing | End of each year |

These forward assumptions are estimates, not reported facts. The [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000158/golf-20260630.htm) provides approximately $95 million of physical capex guidance and $25 million of capitalized ERP spending guidance. ERP in the model is additional net investment, net of related amortization. Recurring stock compensation remains an operating expense.

The model uses guidance as a starting annual run rate. Years 1–5 are not calendar fiscal years or a precise partial-year forecast.

## Cash-flow calculation

Revenue = prior-year revenue × (1 + growth).

EBIT = revenue × operating margin. NOPAT = EBIT × (1 − tax rate).

FCFF = NOPAT + D&A − physical capex − additional working capital − net ERP investment.

FCFF is cash flow available to debt and equity investors before financing payments.

## Five-year reverse forecast

| Measure | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---|---:|---:|---:|---:|---:|
| Revenue growth | 14.43% | 14.43% | 14.43% | 14.43% | 14.43% |
| Revenue | 3,046.6 | 3,486.1 | 3,989.1 | 4,564.6 | 5,223.1 |
| EBIT margin | 12.50% | 12.75% | 13.00% | 13.25% | 13.50% |
| EBIT | 380.8 | 444.5 | 518.6 | 604.8 | 705.1 |
| NOPAT | 293.2 | 342.3 | 399.3 | 465.7 | 542.9 |
| Add: D&A | 67.0 | 76.7 | 87.8 | 100.4 | 114.9 |
| Less: physical capex | (106.6) | (122.0) | (139.6) | (159.8) | (182.8) |
| Less: additional NWC | (76.8) | (87.9) | (100.6) | (115.1) | (131.7) |
| Less: net ERP | (25.0) | (15.0) | (10.0) | (5.0) | (5.0) |
| Free cash flow | 151.8 | 194.0 | 236.9 | 286.3 | 338.3 |
| Present value | 139.9 | 164.8 | 185.4 | 206.6 | 225.0 |

Present value of explicit cash flows: **$921.7 million**.

## Terminal calculation

| Year 6 calculation | Amount |
|---|---:|
| Revenue | 5,353.7 |
| EBIT | 722.7 |
| NOPAT | 556.5 |
| Add: D&A | 117.8 |
| Less: physical capex | (187.4) |
| Less: additional NWC | (26.1) |
| Less: net ERP | (5.1) |
| Free cash flow | **455.7** |

Terminal value at Year 5 = Year 6 FCFF / (WACC − terminal growth) = **$7,594.6 million**.

Discounting this value five years at 8.5% produces **$5,050.7 million**.

Year 6 FCFF rises because additional working-capital investment falls when growth slows immediately to 2.5%. The model rebuilds this investment rather than simply growing Year 5 FCFF.

## Enterprise value to equity value

| Calculation | Amount |
|---|---:|
| PV of explicit cash flows | 921.7 |
| PV of terminal value | 5,050.7 |
| Enterprise value | **5,972.5** |
| Less: debt principal proxy | (965.141) |
| Add: unrestricted cash | 66.600 |
| Less: pension and postretirement | (68.005) |
| Less: redeemable minority interest | (1.180) |
| Less: other minority interest | (0.761) |
| Less: VIE financing | (7.500) |
| Equity value | **4,996.5** |
| Diluted shares proxy (millions) | 58.582333 |
| Value per share | **$85.29** |

Debt comprises $441.6 million revolving borrowings, $500 million notes, $22.902 million short-term debt and $0.639 million current long-term debt. Shares combine 58.405044 million outstanding on July 31 with 0.177289 million incremental Q2 dilution. Source: [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000158/golf-20260630.htm).

## WACC sensitivity

Each scenario independently solves the same model for the $85.29 price. Other inputs remain fixed, including 2.5% terminal growth.

| WACC | Required annual revenue growth |
|---|---:|
| 7.50% | 9.34% |
| 8.50% | 14.43% |
| 9.50% | 19.13% |

## Interpretation and limitations

Required revenue growth of 14.43% substantially exceeds 2025 growth of 4.1%. Sales nearly double from the starting run rate, while EBIT margins rise above the 2025 level of 11.7%.

Terminal value contributes **84.57%** of enterprise value. The immediate growth slowdown reduces working-capital investment materially. A smoother growth fade or more capacity investment could increase required growth.

June balance-sheet figures predate the quote. All unrestricted cash is added. Principal and carrying values approximate debt, pension and minority claims. Residual noncurrent finance leases are not separately quantified. Operating leases remain operating expenses, and no separately appraised investments are added. No future buyback benefit is assumed.

This is one combination of growth, margins and investment that supports the price. It does not establish a unique market forecast or prove the shares are overpriced.

## Reproduction and checks

Run `python3 GOLF/valuation/reverse_dcf.py` from the workspace root. It prints the full forecast and sensitivities and checks each solved price against $85.29.

In Excel, after changing assumptions, set C49 to zero by changing C18 using Goal Seek. The WACC table is a dated snapshot; re-solve each WACC to refresh it. Workbook formulas were recalculated and matched to Python, including the equity bridge. Native Excel Goal Seek was not tested.
