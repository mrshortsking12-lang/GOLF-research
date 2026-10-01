# GOLF: Company Selection, Forecast, Valuation, and Sensitivity Analysis

Prepared October 1, 2026. Company: Acushnet Holdings Corp. (NYSE: GOLF).

## Why I picked GOLF and why it was suitable to analyze

I picked GOLF because it creates products I like. Acushnet owns Titleist and FootJoy, so studying the company let me connect familiar golf equipment and products with the financial decisions behind them. My interest gave me a reason to investigate the business; it was not, by itself, evidence that the stock was attractively priced.

GOLF was suitable to analyze because it is a public company with annual and quarterly filings, identifiable product categories, historical financial statements, and disclosed investment and financing information. Club launches and replacement demand differ from the repeat purchasing of golf balls. Those differences provide company-specific drivers that can be connected to revenue, profit, reinvestment, and shareholder value. The company also provided useful analytical challenges: accounting reclassifications, product-launch timing, ERP spending, debt, and limited profitable golf-focused peers.

## How the company earns money

Acushnet earns revenue by selling branded golf products through golf shops, retailers, distributors, and direct channels. Titleist equipment includes balls, clubs, wedges, and putters; FootJoy sells golf footwear and apparel; golf gear includes bags and accessories. The economic relationship is units sold multiplied by average selling price, although my models forecast category revenue growth rather than estimating those two inputs separately.

Balls are consumables, so play and replacement purchases support recurring demand. Clubs are more durable and depend more on replacement cycles, fitting, and new launches. Premium pricing and product mix affect revenue and margins; manufacturing, materials, distribution, marketing, and R&D affect costs. Retailer shipments are not automatically the same as final consumer purchases. See [2025 10-K, Item 1](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000057/golf-20251231.htm).

## Sources, reporting periods, and units

The report combines saved analyses with model runs checked on October 1. It does not use a new live stock quote. Fiscal years end December 31. Annual flows cover twelve months; balance-sheet balances are snapshots; interim results are not full-year results.

| Evidence | Reporting period / date | Units and use |
|---|---|---|
| [2022 10-K](https://www.sec.gov/Archives/edgar/data/1672013/000167201323000011/golf-20221231.htm), Item 7 | Year ended December 31, 2022, compared with 2021 | Category sales in USD millions and reported annual growth; first of four growth observations. |
| [2024 10-K](https://www.sec.gov/Archives/edgar/data/1672013/000167201325000009/golf-20241231.htm), Item 7 and Note 2 | 2024, with comparable 2023 and 2022 category figures | Historical growth and expense-presentation changes. |
| [2025 10-K](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000057/golf-20251231.htm), Items 7–8 | Year and balance-sheet date December 31, 2025; filed February 27, 2026 | Financial statements generally in USD thousands, except shares/per-share data; converted to millions in my models. |
| [June 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000158/golf-20260630.htm) | Three and six months ended June 30, 2026; filed August 6 | Interim flows, June balances, investment references, and financing evidence. |
| [Q2 earnings release](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000157/ex991-q22026.htm) | Published August 6, 2026 | Full-year 2026 guidance, not realized annual results. |
| [Saved market-price research](lab08/README.md) / [price history](https://stockanalysis.com/stocks/golf/history/) | September 10, 2026 price; peer evidence collected September 17 | USD per common share; secondary market data, not audited financial-statement evidence. |

The most consequential anchors are 2025 sales of **$2,558.730 million**, EBIT of **$299.428 million** (an **11.70%** margin), and operating cash flow of approximately **$194.4 million**. Physical capex of approximately **$74.3 million** excludes **$38.2 million** of capitalized ERP spending. Operating cash flow less physical capex therefore is not FCFF: it is after financing interest and already reflects some other investment. The 2026 sales guidance range is **$2,650–$2,675 million**, with midpoint **$2,662.5 million**. The earnings outlook includes approximately **$30 million of net tariff refunds**, which I do not assume recur indefinitely. [2025 10-K](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000057/golf-20251231.htm), [Q2 release](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000157/ex991-q22026.htm).

All forecast monetary amounts below are **USD millions**, except values per share in **USD/share**. Share denominators are in millions of shares. A two-percentage-point shift, such as 8.9% to 10.9%, is different from a relative 2% increase.

## Two models, with different purposes

| Model | Forecast and cash-flow definition | Discount basis | Current saved result |
|---|---|---|---|
| Linked pro forma, [financial_projection.py](../financial_projection.py) | Calendar 2026–2030 income statement, balance sheet, cash flow, and supporting schedules; classroom **FCFE** convention | December 31, 2025 opening date; **8% cost of equity** | **$52.30/share** |
| Product-growth DCF, [dcf.py](valuation/dcf.py) | Five normalized forward periods using category growth, EBIT margins, and reinvestment; **FCFF** | Retained September model basis; **8.5% WACC** | **$58.08/share** |

The category-average update applies to the FCFF model. It has not replaced the separate pro forma's calendar-year growth path. The models also differ in investment, financing, shares, and terminal treatment, so their prices are not an isolated test of one assumption. Neither is a precise October 1 valuation using actual-to-date results and remaining-period discounting.

## How history became forecast assumptions

The pro forma starts from the December 31, 2025 balance sheet. It uses the 2026 sales-guidance midpoint, then a judgmental growth fade. Historical ratios provide anchors, not proof of future performance.

| Pro forma input | 2026–2030 assumption | Historical/guidance link and judgment |
|---|---|---|
| Revenue growth | 4.0555%, 4.0%, 3.5%, 3.0%, 2.5% | First year equals 2,662.5 / 2,558.730 − 1; later slowdown is judgment. |
| Gross margin | 47.7% each year | Near 2025's 47.73%; recurring margin rather than permanently extending refunds. |
| SG&A / gross profit | Approximately 68.24% | 2025 reported expense ratio, held constant as judgment; R&D is modeled separately. |
| Inventory days | 170, 168, 166, 166, 166 | Historical ending-balance days were about 178 in 2023 and 166 in 2024–2025; initial stocking then normalization is judgment. |
| PP&E depreciation / opening net PP&E | 13.3% | Rounded 2025 ratio, using PP&E depreciation rather than total company D&A. |
| Physical capex | 95 in 2026; 3.5% of sales thereafter | First-year guidance; later investment intensity is judgment. |
| Capitalized ERP investment | 25, 15, 10, 5, 5 | First-year guidance; taper is judgment. |
| Tax | 23% | Normalized assumption, supported by the approximately 23.3% first-half 2026 observation. |
| Other noninventory working capital | 0.8% of incremental revenue | Classroom convention, not a calibrated company forecast. |

History and classifications are documented in [historical research](research/history_ratios_assumptions_2026-09-29.md), the [accuracy audit](research/assumption_accuracy_audit_2026-09-29.md), and [implemented pro forma results](../outputs/golf_projection_20260929/results.md). The earlier audit predates implementation; the implemented report records later corrections.

For the company-specific FCFF model, four full-year **reported revenue-growth rates** became category bases:

| Category | 2022 | 2023 | 2024 | 2025 | Arithmetic-average forecast base |
|---|---:|---:|---:|---:|---:|
| Clubs | 10.5% | 8.1% | 9.5% | 7.5% | **8.9%** |
| Balls | 1.7% | 12.2% | 3.3% | 4.4% | **5.4%** |

The average is the sum of four published rates divided by four, not a CAGR. The 2024 filing's revised 2023 club presentation is used. The 2022 observation requires a 2021 denominator; partial-year 2026 is excluded. Sources: [2022 10-K](https://www.sec.gov/Archives/edgar/data/1672013/000167201323000011/golf-20221231.htm), [2024 10-K](https://www.sec.gov/Archives/edgar/data/1672013/000167201325000009/golf-20241231.htm), [2025 10-K](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000057/golf-20251231.htm).

Each average is held through normalized Years 1–5; other products retain a judgmental 5%. The starting $2,662.5 million run rate is allocated using 2025 weights: clubs **30.30%**, balls **32.09%**, and the remainder other products. This allocation is a modeling convention, not category-specific 2026 guidance. Historical rates include volume, price, and currency effects. Launch timing and unusually strong demand may not repeat.

## Linked statements and accounting checks

The pro forma links sales to COGS, gross profit, operating expenses, EBIT, interest, taxes, and net income. Inventory follows COGS and inventory days. PP&E rolls forward by adding physical capex and subtracting depreciation. ERP investment and amortization roll through other assets. Net income increases equity; buybacks and dividends reduce cash and equity. Debt balances and repayments affect interest and cash. Excess cash sweeps the revolver after preserving a $50 million cash minimum, reducing subsequent interest.

The implemented model removes historical PP&E depreciation embedded in reported costs before charging forecast depreciation, avoiding a duplicate expense. Intangible amortization has a separate schedule. Cloud amortization stays embedded proportionally in SG&A, is added back in cash flow, and reduces the cloud asset. Notes, short-term facilities, other term debt, finance leases, and issuance costs have separate schedules; lease payments are split between interest and principal. This treatment is more specific than a single blended debt rate or a dealer-style floor-plan assumption.

Checks rerun for this report confirmed:

- Opening debt principal less unamortized costs reconciles to carrying debt.
- Every 2026–2030 balance sheet satisfies **assets − liabilities − redeemable minority claim − equity = 0**, within numerical tolerance.
- Every year meets minimum cash; debt and asset schedules roll forward without an unexplained balancing plug.
- Cash follows operating/investment cash, known distributions, and revolver draws or repayments; equity follows opening equity plus income less distributions.
- The FCFF base, lower/higher scenarios, reverse-price solve, and enterprise-to-equity arithmetic reproduce the saved results.

The 2024 reclassification moved shipping/distribution expense from SG&A into COGS. Comparable historical ratios use the revised presentation; mixing original and revised gross margins would create a false operating trend. See [2024 10-K, Note 2](https://www.sec.gov/Archives/edgar/data/1672013/000167201325000009/golf-20241231.htm).

Passing accounting identities verifies arithmetic and linkages, not economic realism. Flat grouped balances, the 0.8% rule, constant rates, cloud-amortization convention, and fixed shares remain simplifications. Known 2026 buybacks and dividends are included, but additional distributions are assumed zero. The FCFF sensitivity model is a condensed cash-flow model, not a separately balanced three-statement forecast.

## DCF method, discount rates, and terminal value

### Linked pro forma: FCFE convention

The pro forma begins with after-interest net income, adds modeled noncash expenses, and subtracts capex, ERP investment, inventory/other working-capital investment, and nonrevolver principal repayments. It discounts the resulting classroom FCFE series at **8%**, a chosen required equity return rather than a researched CAPM estimate.

```text
Terminal value at 2030 = (2030 FCFE + 2030 nonrevolver principal repayment)
                         × 1.025 / (0.08 − 0.025)
Equity value = PV of 2026–2030 FCFE + PV of terminal value
```

Rerun outputs are **$609.82 million** PV of explicit FCFE plus **$2,442.79 million** PV of terminal value, totaling **$3,052.61 million**, or **$52.30/share** using **58.371822 million** fixed opening shares. In 2030, EBIT is **$342.22 million** and FCFE **$192.59 million**. Terminal value supplies **80.02%** of equity value.

This requested convention excludes revolver draws/sweeps from the valued FCFE series even though they affect cash and future interest; standard FCFE normally includes net borrowing. It also grows the final cash-flow figure rather than rebuilding a fully normalized terminal balance sheet. Consequently, it is a classroom leveraged valuation with material limitations. There is no additional debt subtraction or cash addition to this FCFE equity value.

### Category forecast: FCFF DCF

```text
FCFF = EBIT × (1 − 23%) + D&A − physical capex
       − additional working capital − net ERP investment
Enterprise value = PV of Years 1–5 FCFF + PV of terminal value
Terminal value at Year 5 = Year-6 FCFF / (8.5% − 2.5%)
```

FCFF is before financing payments, so it is discounted at **8.5% WACC**, not the pro forma's 8% cost of equity. WACC is an assumed scenario input, not a completed market-based capital-cost estimate. EBIT margins rise **12.50%, 12.75%, 13.00%, 13.25%, 13.50%**; D&A is **2.2% of sales**, physical capex **3.5%**, and additional working capital **20% of incremental sales**. Net ERP investment is **25, 15, 10, 5, 5**. These are forward judgments.

Terminal growth is **2.5%**, with **13.5% EBIT margin**. The model rebuilds Year-6 cash flow and reinvestment at that growth rate. Updated enterprise value is **$4,378.67 million**; terminal value contributes **79.66%**. The abrupt slowdown reduces working-capital investment, so a smoother fade or greater reinvestment could lower value. A perpetual growth rate below WACC is mathematically necessary, but does not establish a sustainable economic forecast.

## Enterprise-to-equity bridge for the FCFF model

| Bridge component | USD millions |
|---|---:|
| Enterprise value | 4,378.670 |
| Less debt-principal proxy | (965.141) |
| Add unrestricted cash | 66.600 |
| Less pension/postretirement claim | (68.005) |
| Less redeemable minority claim | (1.180) |
| Less other minority claim | (0.761) |
| Less VIE financing | (7.500) |
| Equity value | **3,402.683** |
| Diluted-share proxy, millions | **58.582333** |
| Estimated value, USD/share | **58.08** |

The net adjustment is **$975.987 million**. The debt proxy uses $441.6 million revolver principal, $500 million notes, $22.902 million short-term debt, and $0.639 million current debt. Shares combine July 31 outstanding shares with incremental Q2 dilution. These use [June 2026 filing evidence](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000158/golf-20260630.htm), not the pro forma's opening balances. Principal differs from carrying debt; unrestricted cash excludes restricted balances. Residual finance leases are not fully isolated, claim measurements are approximate, and future dilution/buybacks are not projected. Operating leases remain operating expenses.

## Peer choices and why methods differ

The saved peer policy admitted only golf-focused businesses. **Callaway (CALY, formerly MODG)** overlaps in equipment, but restructuring and Topgolf exposure complicate comparability. **Newton Golf (NWTG)** sells shafts and putters, but is much smaller and has a narrower portfolio and financing risk.

| Candidate | Annual 2025 total diluted EPS, USD/share | Peer P/E decision |
|---|---:|---|
| Callaway | −2.20 | Exclude: negative total earnings do not support a meaningful positive-earnings multiple. |
| Newton Golf | −1.63 | Exclude: negative earnings; scale also limits comparability. |

Sources: [Callaway 2025 10-K, EPS note](https://www.sec.gov/Archives/edgar/data/837465/000083746526000010/modg-20251231.htm), [Newton 2025 10-K, statements of operations](https://www.sec.gov/Archives/edgar/data/1934245/000149315226014164/form10-k.htm). The saved peer calculation was rerun and still has **zero usable peers**, so there is no peer median, implied share price, or numerical peer range. Callaway's positive continuing-operations EPS is not substituted for total EPS, and losses are not converted into positive earnings.

A valid peer P/E method would multiply comparable peers' market price/earnings multiples by GOLF EPS. It values equity directly; no enterprise-to-equity adjustment is added. DCF estimates future cash flows and discounting, while P/E relies on market pricing of comparable earnings. Their assumptions, accounting sensitivity, and timing differ. GOLF's saved own P/E, **$85.27 / $3.11 = 27.418x**, is a descriptive multiple, not an independent peer valuation. See [peer research](lab08/README.md). Lack of a peer estimate does not imply zero value or prove overpricing.

## Saved market price and reverse DCF

The September 10 reverse DCF saved **$85.29/share**. Later peer research recorded a **$85.27 closing price** for that date. The two-cent discrepancy is unresolved and remains disclosed; neither figure is today's quote.

The reverse DCF solves for uniform company revenue growth that reproduces the saved $85.29 input. It requires **14.43% annual growth for five years**, taking the $2,662.5 million starting run rate to approximately **$5,223.1 million**. Held fixed are the EBIT-margin path, 23% tax, 2.2% D&A, 3.5% physical capex, 20% incremental working capital, ERP path, **8.5% WACC**, **2.5% terminal growth**, terminal margin, discount timing, equity bridge, and shares. At WACC of 7.5% or 9.5%, the required growth becomes **9.34%** or **19.13%**, respectively.

This saved reverse result uses uniform company growth, not separate 8.9% club and 5.4% ball forecasts. Terminal value contributes **84.57%** of its enterprise value. It is one conditional combination supporting an input price, not an independent fair-value estimate or a uniquely identified market forecast. Higher margins or less reinvestment could support the same price at lower growth; opposite changes could require higher growth. See [saved reverse report](../outputs/golf_reverse_20260910/GOLF_reverse_DCF.md) and [solver](valuation/reverse_dcf.py).

## Sensitivity analysis: inputs, outputs, and causal effects

The updated FCFF base uses clubs **8.9%**, balls **5.4%**, and other products **5%**. Each category is tested at **±2 percentage points** in every Year 1–5. The other category stays at its own base. WACC, terminal growth, margins, investment ratios, debt/cash, and shares stay fixed; all category growth reverts to 2.5% in the terminal period.

| Run | Changed annual input | Year-5 EBIT, USD m | Year-5 FCFF, USD m | Value, USD/share | Value change vs. base |
|---|---:|---:|---:|---:|---:|
| Base | Clubs 8.9%; balls 5.4% | 489.37 | 280.94 | 58.08 | — |
| Clubs lower | 6.9% | 474.61 | 276.65 | 56.21 | −1.87 |
| Clubs higher | 10.9% | 505.26 | 285.23 | 60.09 | +2.00 |
| Balls lower | 3.4% | 475.67 | 276.45 | 56.34 | −1.75 |
| Balls higher | 7.4% | 504.15 | 285.46 | 59.96 | +1.88 |

Results use unrounded calculations before display rounding. Average annual changes across the five forecast periods are:

| Run | Revenue change, USD m | EBIT change, USD m | FCFF change, USD m |
|---|---:|---:|---:|
| Clubs lower | −59.54 | −7.86 | −0.90 |
| Clubs higher | +62.68 | +8.28 | +0.85 |
| Balls lower | −57.58 | −7.59 | −1.04 |
| Balls higher | +60.66 | +8.00 | +0.99 |

These averages are five annual differences from base divided by five, not cumulative totals. The full input tables, formulas, and calculations are in [Sensitivity Analysis](valuation/Sensitivity%20Analysis.md).

Higher category sales raise company revenue and EBIT at held-fixed margins. After tax, some incremental profit becomes cash, but growth requires inventory/working capital, capex, and ERP investment. That is why FCFF changes less than EBIT and may initially move in the opposite direction. Lower growth reduces those investment needs but weakens later earnings and terminal cash flow. In a linked statement model, these changes also flow through assets, cash, debt needs, interest, and retained earnings; the condensed FCFF sensitivity does not separately recalculate all those financing balances. The stock-value changes are changes in estimated intrinsic value, not guaranteed movements in the traded price.

### What the ranking establishes—and what it does not

Across equal four-percentage-point test ranges, clubs move value by **$3.87/share** (approximately **$0.97 per percentage point**) and balls by **$3.62/share** (approximately **$0.91 per percentage point**). Clubs therefore rank slightly higher by **modeled value-per-share sensitivity** around these updated bases, even though balls have a larger starting revenue weight. Clubs' higher base growth compounds faster. The ranking differs from the earlier shared-5% base, illustrating its dependence on assumptions.

This does not establish that clubs have higher actual margins, that their growth is more likely to change, or that they are the largest risk in the whole valuation. Average FCFF responds somewhat more to balls in these runs; a ranking by another output can differ. The tests change one input at a time, ignore correlations, use common company economics for both categories, and assign no probabilities. Different ranges, category margins, or reinvestment needs could reverse the ranking. Discount-rate and terminal assumptions also matter substantially because most modeled value lies beyond the explicit forecast.

## Two cost and cash-investment drivers and their effect on stock value

The two cash-investment drivers discussed earlier are **physical capital expenditure** and **additional working capital**. They are cash requirements rather than immediate income-statement expenses. I distinguish them from the two revenue-growth drivers, clubs and balls, because growth only creates shareholder value after funding the investment it requires.

| Independent input | Lower | Base | Higher | Periods and range rationale |
|---|---:|---:|---:|---|
| Physical capex / sales | 3.0% | 3.5% | 4.0% | Same ratio in Years 1–5 and terminal period. Labeled ±0.5-percentage-point judgment around the existing model base; historical 2025 physical capex was approximately 2.9% of sales and 2026 guidance approximately 3.6% of midpoint sales. |
| Additional working capital / incremental sales | 15% | 20% | 25% | Same ratio in Years 1–5 and terminal period. Labeled ±5-percentage-point judgment around the model assumption, not a disclosed company target or verified historical range. |

Each test changes one input while category growth, EBIT margins, D&A, tax, ERP investment, discount rate, terminal growth, debt/cash bridge, and shares remain fixed. The denominator matters: capex is a percentage of **total sales**, while additional working capital is a percentage of the **increase in sales**.

| Scenario | Year-5 EBIT, USD millions | Year-5 FCFF, USD millions | Estimated stock value, USD/share | Change vs. $58.08 base, USD/share |
|---|---:|---:|---:|---:|
| Base: capex 3.5%; working capital 20% | 489.37 | 280.94 | 58.08 | — |
| Physical capex lower: 3.0% | 489.37 | 299.06 | 62.67 | +4.59 |
| Physical capex higher: 4.0% | 489.37 | 262.81 | 53.50 | −4.59 |
| Working-capital need lower: 15% | 489.37 | 291.87 | 59.58 | +1.50 |
| Working-capital need higher: 25% | 489.37 | 270.00 | 56.59 | −1.50 |

Changes are computed before rounding displayed prices.

**Physical capex:** Factories, production equipment, and assembly capacity require cash. Higher capex increases assets but reduces current FCFF; lower capex leaves more cash for investors. Discounting that cash-flow difference changes business value and then equity value per share. In a fully linked forecast, investment would also affect PP&E, later depreciation, capacity, and possibly growth. This isolated test holds those responses fixed. Spending less only supports a higher valuation if it does not undermine future production or earnings; higher investment can create value if its future benefits exceed its cost.

**Working capital:** More inventory or receivables, net of supplier financing and other operating liabilities, ties up cash even when sales are profitable. A higher funding ratio reduces FCFF and estimated stock value; faster collections, more efficient inventory, or better supplier terms can release cash and raise value. In the linked pro forma, funding needs affect cash, revolver use, and subsequent interest. The condensed FCFF test holds financing balances fixed and measures the direct operating cash effect.

The cash-flow link is `investment requirement → FCFF → discounted enterprise value → equity value / shares`. EBIT is unchanged in these tests because I change cash-investment ratios rather than the held-fixed profit margin. These calculations measure estimated intrinsic value, not guaranteed movements in the traded stock price. Under the chosen ranges, capex has a larger price effect than working capital, but the ranges and denominators differ; this does not establish a universal ranking of risk or the best spending policy. Run [investment_sensitivity.py](valuation/investment_sensitivity.py) to reproduce the results.

## My investment recommendation and what would change it

**I would not recommend buying GOLF at the saved September 10 price of $85.29.** The updated category-growth DCF estimates **$58.08 per share**, approximately **31.9% below** that saved price. The separate classroom pro forma estimates **$52.30**. Although I like the company's products, my modeled cash flows do not justify paying the saved market price under the current assumptions. This is my conclusion for the dated analysis, not a claim about the stock's current trading price or a recommendation to sell an existing holding.

**I would recommend buying if stronger, sustainable growth raised a defensible valuation sufficiently above the purchase price to provide a margin of safety.** Higher growth would need credible support from club launches, ball demand, pricing, or market-share gains, while preserving margins and allowing for the extra inventory and capacity investment needed to deliver the sales.

A small growth increase is not enough in this model. Increasing both category bases by two percentage points—to **10.9% for clubs and 7.4% for balls**—produces approximately **$61.97 per share**, still below $85.29. The saved reverse DCF requires approximately **14.43% annual company-wide revenue growth for five years**, with other inputs fixed, merely to support $85.29; reaching that rate provides no modeled valuation cushion by itself. It is company-wide growth, not the required rate for each individual product category.

As an illustration, **16% annual company-wide growth** produces approximately **$91.53 per share**, but that is only about 7.3% above the saved price and does not automatically establish an adequate margin of safety. It is an aggressive hypothetical, not management guidance. My recommendation would change when evidence supports enough growth and cash conversion to produce attractive upside after downside testing, rather than simply because a higher growth number can be entered into the model. A lower purchase price could also improve the case without higher growth.

## Rubric review and remaining evidence

This section distinguishes completed analysis from discussion evidence that still needs to be recorded. It does not assign a final course grade. One underlying weakness should be scored once rather than counted again in several criteria.

| Criterion | Evidence in this write-up | Remaining requirement |
|---|---|---|
| Full analysis and ownership | Personal selection reason; business economics; sources; forecast-to-valuation route; dated recommendation and limitations. | I need to review the AI-assisted explanations and be able to explain the calculations in my own words. The document alone does not demonstrate that oral explanation. |
| Valuation reasoning | Separate FCFE/FCFF definitions, discount rates, terminal formulas, equity bridge, peer exclusions, and saved reverse-DCF inputs. | Cost of capital and terminal reinvestment remain judgmental. A current-date investment decision requires refreshed inputs and discount timing. |
| Sensitivity interpretation | Own-model runs; held-fixed inputs; reproducible ranges; statement/cash-flow mechanisms; ranking distinguished from uncertainty. | Product-specific margins and reinvestment could change the ranking; the tests do not establish probabilities. |
| Reviewing the partner | Partner company CROX and discussion date October 1, 2026 are recorded. | Company and date alone do not document the substance of the review. |
| Response and revision | Supported decisions and effects of the revisions made in this project are recorded below. | These revisions are documented project decisions; their connection to the partner discussion is not recorded. |

### Partner Discussion

- Partner's company: **CROX (Crocs, Inc.)**.
- Discussion date: **October 1, 2026**.

### My supported response and revision decisions

These decisions reflect the documented work and user-directed revisions.

| Issue considered | Keep / revise / investigate | Evidence and effect on conclusion or research priority |
|---|---|---|
| Shared 5% growth for both categories | **Revise — completed** | Replace it with 2022–2025 arithmetic averages: clubs 8.9%, balls 5.4%. The FCFF base rises from $54.20 to $58.08 per share; it remains below the saved $85.29 price, so the dated no-buy conclusion remains. |
| Treating $52.30 and $58.08 as outputs of the same model | **Revise — completed** | Separate the linked calendar-year FCFE model at 8% from the normalized category-growth FCFF model at 8.5%. The values cannot be interpreted as one-variable sensitivity or averaged into a consensus. |
| “Higher growth means I would buy” without a threshold | **Revise — completed** | Add the conditions of credible, sustainable growth, adequate reinvestment, and a valuation cushion. Increasing both category growth rates by two points gives $61.97, still below $85.29; higher growth alone does not reverse the recommendation. |
| Cash needed to fund growth | **Revise — completed** | Add physical-capex and working-capital sensitivities. Their price effects show why increased sales need not translate proportionally into free cash flow or value. |
| Loss-making golf peers | **Keep** | Preserve the golf-only policy and exclude negative total-EPS multiples. Report no peer estimate rather than inventing numerical corroboration. |
| September 10 price discrepancy, $85.29 versus $85.27 | **Investigate** | Preserve the saved solver input and disclose the two-cent difference. Check quote definition/provider evidence before using a refreshed market comparison. |
| WACC, sustainable margins, terminal reinvestment, and category economics | **Investigate — priority** | The large terminal-value share and held-fixed company ratios leave the economic forecast uncertain. Research product-level cash conversion and capacity needs, estimate a dated cost of capital, and test a smoother growth fade before changing the investment recommendation. |

## Overall interpretation and reproducible work

My interest in GOLF motivated the analysis, while the financial evidence determined the forecasts and valuation limits. Historical-average category growth gives a more company-specific base than applying 5% to everything. It does not remove uncertainty about launches, pricing, margins, or reinvestment. The linked pro forma checks accounting mechanics; the FCFF model tests operating drivers; the reverse DCF translates a saved price into conditional expectations; and the peer analysis documents why no independent earnings-multiple estimate was available.

The key question is whether GOLF can sustain profitable growth and convert it into cash after the investment needed to support it. My dated recommendation is not to buy at $85.29; stronger substantiated growth and a sufficient valuation cushion could change that decision.

```bash
python3 financial_projection.py --schedules
python3 GOLF/valuation/product_growth_sensitivity.py
python3 GOLF/valuation/investment_sensitivity.py
python3 GOLF/valuation/reverse_dcf.py
python3 GOLF/lab08/peer_pe.py
```

This write-up was prepared with AI assistance using the saved research and executable models. Arithmetic and stated model checks were rerun. Partner company and discussion date were supplied by me; no additional discussion outcomes, new personal source review, or independent second-review completion are claimed.
