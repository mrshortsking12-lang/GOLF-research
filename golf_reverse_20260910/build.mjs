import fs from 'node:fs/promises';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const out = new URL('.', import.meta.url).pathname;
const result = JSON.parse(await fs.readFile(`${out}results.json`, 'utf8'));
const wb = Workbook.create();
const s = wb.worksheets.add('Reverse DCF');
const inputs = wb.worksheets.add('Inputs');
const num = '#,##0.0;(#,##0.0);"-"';
const pct = '0.0%;(0.0%);"-"';
const usd = '$0.00;($0.00);"-"';
function value(sheet, cell, v) { sheet.getRange(cell).values = [[v]]; }
function formula(sheet, cell, f) { sheet.getRange(cell).formulas = [[f]]; }
function band(sheet, range, title) {
  sheet.getRange(range).format.fill = '#203E50';
  sheet.getRange(range).format.font.color = '#FFFFFF';
  sheet.getRange(range).format.font.bold = true;
  value(sheet, range.split(':')[0], title);
}
for (const sheet of [s, inputs]) {
  sheet.showGridLines = false;
  sheet.getRange('A1:J65').format.font.name = 'Arial';
  sheet.getRange('A1:J65').format.font.size = 10;
  sheet.getRange('A1:J65').format.rowHeight = 20;
  sheet.getRange('A1:A65').format.columnWidth = 3;
  sheet.getRange('B1:B65').format.columnWidth = 35;
  sheet.getRange('C1:J65').format.columnWidth = 15;
  sheet.getRange('C1:J65').setNumberFormat(num);
  sheet.getRange('B2').format.font.size = 16;
  sheet.getRange('B2').format.font.bold = true;
}
value(s, 'B2', 'GOLF reverse DCF');
value(s, 'B3', 'Acushnet Holdings Corp. September 10, 2026. USD millions except per share.');
band(s, 'B5:C5', 'Market-implied requirements');
const summary = [
  [6, 'Required revenue CAGR', '=C18'],
  [7, 'Market price', "='Inputs'!C6"],
  [8, 'Model value per share', '=C48'],
  [9, 'Year 5 revenue', '=G32'],
  [10, 'Year 5 / starting revenue', '=G32/$C$19'],
  [11, 'Terminal PV / enterprise value', '=C45/C46'],
];
for (const [r,l,f] of summary) { value(s, `B${r}`, l); formula(s, `C${r}`, f); }
s.getRange('C6').setNumberFormat(pct);
s.getRange('C7:C8').setNumberFormat(usd);
s.getRange('C10').setNumberFormat('0.00"x"');
s.getRange('C11').setNumberFormat(pct);
s.getRange('B6:C6').format.fill = '#E6EFE8';
s.getRange('B6:C6').format.font.bold = true;
value(s, 'E6', 'Five normalized forward years, with year-end discounting.');
value(s, 'E8', 'After changing inputs, use Excel Goal Seek:');
value(s, 'E9', 'Set C49 to 0 by changing C18.');
value(s, 'E11', 'C18 is the saved solution. It does not solve itself after edits.');
value(s, 'B13', 'Conditional growth requirement, not a forecast. Terminal assumptions materially drive the answer.');
band(s, 'B16:C16', 'Valuation controls');
const controls = [
 [18,'Revenue growth (Goal Seek input)',result.growth],
 [19,'Starting annual revenue',"=AVERAGE('Inputs'!C8:C9)"],
 [20,'WACC',.085], [21,'Terminal revenue growth',.025],
 [22,'Tax rate',.23], [23,'D&A / revenue',.022],
 [24,'Physical capex / revenue',.035], [25,'Incremental NWC / new sales',.20],
 [26,'Diluted shares proxy',"=SUM('Inputs'!C12:C13)"],
 [27,'Net debt and other claims',"=SUM('Inputs'!C15:C18)-'Inputs'!C19+SUM('Inputs'!C20:C23)"],
];
for (const [r,l,v] of controls) {
  value(s, `B${r}`, l);
  if (typeof v === 'string') { formula(s, `C${r}`, v); s.getRange(`C${r}`).format.font.color = '#008000'; }
  else { value(s, `C${r}`, v); s.getRange(`C${r}`).format.font.color = '#0000FF'; s.getRange(`C${r}`).format.fill = '#FFF2CC'; }
}
for (const r of [18,20,21,22,23,24,25]) s.getRange(`C${r}`).setNumberFormat(pct);
value(s, 'E18', 'Blue / amber = editable assumptions. Green = links to Inputs.');
value(s, 'E20', 'WACC is an assumed required return, not a CAPM estimate.');
value(s, 'E22', 'Margins retain recurring stock compensation as an expense.');
value(s, 'E24', 'ERP is additional net investment, excluding related amortization.');
value(s, 'E25', 'Downloaded 2025 10-K calibration is shown below the model.');
value(s, 'E26', 'July shares plus Q2 incremental dilution. No future buybacks.');
band(s, 'B30:H30', 'Operating forecast');
s.getRange('C30:H30').values = [['Year 1','Year 2','Year 3','Year 4','Year 5','Terminal']];
const labels = {31:'Revenue growth',32:'Revenue',33:'EBIT margin',34:'EBIT',35:'NOPAT',36:'D&A',37:'Physical capital expenditures',38:'Change in operating NWC',39:'Additional net ERP investment',40:'Unlevered free cash flow',41:'Discount period',42:'PV of free cash flow'};
for (const [r,l] of Object.entries(labels)) value(s,`B${r}`,l);
for (let i=0;i<6;i++) {
  const c=String.fromCharCode(67+i), prev=String.fromCharCode(66+i);
  formula(s,`${c}31`,i===5?'=$C$21':'=$C$18');
  formula(s,`${c}32`,i===0?`=$C$19*(1+${c}31)`:`=${prev}32*(1+${c}31)`);
  if(i<5) value(s,`${c}33`,[.125,.1275,.13,.1325,.135][i]);
  else formula(s,`${c}33`,'=G33');
  formula(s,`${c}34`,`=${c}32*${c}33`);
  formula(s,`${c}35`,`=${c}34*(1-$C$22)`);
  formula(s,`${c}36`,`=${c}32*$C$23`);
  formula(s,`${c}37`,`=${c}32*$C$24`);
  formula(s,`${c}38`,`=(${c}32-${i===0?'$C$19':prev+'32'})*$C$25`);
  if(i<5) value(s,`${c}39`,[25,15,10,5,5][i]);
  else formula(s,`${c}39`,'=G39*(1+$C$21)');
  formula(s,`${c}40`,`=SUM(${c}35:${c}36)-SUM(${c}37:${c}39)`);
  value(s,`${c}41`,i+1);
  if(i<5) formula(s,`${c}42`,`=${c}40/(1+$C$20)^${c}41`);
}
for(const r of [31,33]) s.getRange(`C${r}:H${r}`).setNumberFormat(pct);
s.getRange('C41:H41').setNumberFormat('0');
for (const r of [33,39]) { s.getRange(`C${r}:G${r}`).format.font.color='#0000FF'; s.getRange(`C${r}:G${r}`).format.fill='#FFF2CC'; }
s.getRange('B40:H40').format.font.bold=true;
s.getRange('B40:H40').format.borders={top:{style:'thin',color:'#203E50'}};
const valuation = [
 [44,'PV of explicit cash flows','=SUM(C42:G42)'],
 [45,'PV of terminal value','=IF(C20>C21,H40/(C20-C21)/(1+C20)^G41,NA())'],
 [46,'Enterprise value','=SUM(C44:C45)'],
 [47,'Equity value','=C46-C27'],
 [48,'Value per diluted share','=C47/C26'],
 [49,'Model minus market ($/share)',"=C48-'Inputs'!C6"],
];
for (const [r,l,f] of valuation) { value(s,`B${r}`,l); formula(s,`C${r}`,f); }
s.getRange('C48:C49').setNumberFormat('$0.00;($0.00);$0.00');
s.getRange('C49').conditionalFormats.add('cellIs',{operator:'between',formula:[-.01,.01],format:{font:{color:'#000000'}}});
s.getRange('C49').conditionalFormats.addCustom('ABS(C49)>0.01',{fill:'#FCE4D6',font:{color:'#C00000',bold:true}});
value(s,'E45','Terminal cash flow is rebuilt using 2.5% growth (editable C21).');
value(s,'E47','Lower terminal growth releases working-capital investment.');
value(s,'E49','A nonzero difference means the growth input needs re-solving.');
value(s,'B52','Method and limitations');
s.getRange('B52').format.font.bold=true;
const notes = [
 'Starting sales are FY2026 guidance midpoint, used as an annual run-rate proxy. Forecast years are not fiscal years.',
 'EBIT margins are analyst assumptions of 12.5% to 13.5%, excluding recurring tariff refunds. No EBITDA-to-FCFF shortcut.',
 'Terminal growth drops immediately to C21 after Year 5. This materially increases cash conversion as NWC investment slows.',
 'Physical capex exceeds D&A indefinitely. ERP net investment declines to $5m and then grows at the terminal rate.',
 'June balance sheet predates the quote. Debt principal, pension and minority book values approximate economic claims.',
 'All unrestricted cash is added. Operating leases stay in operating costs. No separately valued investments are added.',
 'Residual noncurrent finance leases are not separately quantified. Dilution is approximate. Source details are in Inputs.',
 'Model formulas were recalculated and checked with Artifact Tool. Excel Goal Seek was not tested in the native app.',
];
notes.forEach((n,i)=>value(s,`B${53+i}`,n));

value(inputs,'B2','GOLF source inputs');
value(inputs,'B3','USD millions except price. Data retrieved September 10, 2026.');
band(inputs,'B5:C5','Market and company data');
const sourceRows = [
 [6,'Share price',85.29,'September 10, 2026 quote; not represented as a live price.'],
 [8,'2026 revenue guidance: low',2650,'August 6, 2026 results.'],
 [9,'2026 revenue guidance: high',2675,'August 6, 2026 results.'],
 [10,'2026 tariff refunds in guidance',30,'Excluded from recurring margin assumptions.'],
 [12,'Common shares outstanding',58.405044,'July 31, 2026 outstanding shares.'],
 [13,'Incremental diluted shares',.177289,'Q2 diluted 59.929313 less basic 59.752024.'],
 [15,'Revolving debt principal',441.6,'June 30, 2026; rounded disclosed principal.'],
 [16,'Senior notes principal',500,'June 30, 2026; principal proxy.'],
 [17,'Short-term debt',22.902,'June 30, 2026 balance sheet.'],
 [18,'Current long-term debt',.639,'June 30, 2026 balance sheet.'],
 [19,'Unrestricted cash',66.6,'June 30, 2026; includes VIE cash, excludes restricted cash.'],
 [20,'Pension / postretirement liability',68.005,'June 30, 2026 carrying value.'],
 [21,'Redeemable minority interest',1.180,'June 30, 2026 carrying value.'],
 [22,'Other minority interest',.761,'June 30, 2026 carrying value.'],
 [23,'VIE financing',7.5,'Lionscore note in other noncurrent liabilities.'],
 [25,'2026 physical capex guidance',95,'Calibration only; forecast uses 3.5% of revenue.'],
 [26,'2026 ERP spending guidance',25,'Gross guidance; model assumes a separate net investment schedule.'],
];
for (const [r,l,v,n] of sourceRows) {value(inputs,`B${r}`,l);value(inputs,`C${r}`,v);value(inputs,`E${r}`,n); inputs.getRange(`C${r}`).format.font.color='#0000FF';}
inputs.getRange('C6').setNumberFormat(usd);
inputs.getRange('C12:C13').setNumberFormat('0.000000');
value(inputs,'B29','Sources'); inputs.getRange('B29').format.font.bold=true;
value(inputs,'B30','Quote (row 6)');
value(inputs,'B31','https://stockanalysis.com/stocks/golf/history/');
value(inputs,'B33','Q2 2026 results (rows 8–13)');
value(inputs,'B34','https://www.sec.gov/Archives/edgar/data/1672013/000167201326000157/ex991-q22026.htm');
value(inputs,'B36','Q2 2026 10-Q (rows 15–26)');
value(inputs,'B37','https://www.sec.gov/Archives/edgar/data/1672013/000167201326000158/golf-20260630.htm');
value(inputs,'B40','Operating assumptions follow the existing September 8 GOLF valuation. They are estimates, not company guidance.');
inputs.getRange('B40').format.font.italic=true;
band(inputs,'B43:C43','Downloaded 2025 10-K actuals');
const history = [
 [44,'2025 revenue',2558.730,'Statements of operations, F-4; MD&A, page 50.'],
 [45,'2024 revenue',2457.091,'Statements of operations, F-4; MD&A, page 50.'],
 [46,'2023 revenue',2381.995,'Statements of operations, F-4; MD&A, page 50.'],
 [47,'2025 operating income',299.428,'Statements of operations, F-4; MD&A, page 50.'],
 [48,'2025 depreciation / amortization',55.292,'Cash flows, F-7. Excludes separate cloud ERP amortization.'],
 [49,'2025 physical capex',74.342,'Cash flows, F-7.'],
 [50,'2025 operating cash flow',194.370,'Cash flows, F-7. After interest and includes ERP spending.'],
 [51,'2025 capitalized ERP investment',38.2,'MD&A, Recent Developments and Capital Expenditures.'],
 [52,'2025 effective tax rate',.219,'MD&A, Income Tax Expense.'],
];
for (const [r,l,v,n] of history) {value(inputs,`B${r}`,l);value(inputs,`C${r}`,v);value(inputs,`E${r}`,n); inputs.getRange(`C${r}`).format.font.color='#0000FF';}
inputs.getRange('C52').setNumberFormat(pct);
value(inputs,'B55','Primary historical source: downloaded “golf 10k HTML.html”, year ended December 31, 2025.');
value(inputs,'B56','Corresponding SEC filing:');
value(inputs,'B57','https://www.sec.gov/Archives/edgar/data/1672013/000167201326000057/golf-20251231.htm');
value(inputs,'B59','Historical figures were read directly from the downloaded filing, not a third-party financial data table.');
band(s,'B63:C63','10-K calibration');
const calibration = [
 [64,'2025 revenue growth',"='Inputs'!C44/'Inputs'!C45-1",'Compare with the required five-year CAGR above.'],
 [65,'2023–2025 revenue CAGR',"=('Inputs'!C44/'Inputs'!C46)^(1/2)-1",'Historical annualized growth across two years.'],
 [66,'2025 EBIT margin',"='Inputs'!C47/'Inputs'!C44",'Model assumes improvement to 12.5%–13.5%.'],
 [67,'2025 D&A / revenue',"='Inputs'!C48/'Inputs'!C44",'Forecast rounds this historical ratio to 2.2%.'],
 [68,'2025 physical capex / revenue',"='Inputs'!C49/'Inputs'!C44",'Model uses 3.5%, supported by higher 2026 capex guidance.'],
 [69,'2026 capex guidance / sales',"='Inputs'!C25/C19",'ERP investment is modeled separately.'],
 [70,'2026 guided revenue growth',"=C19/'Inputs'!C44-1",'Guidance midpoint versus reported 2025 sales.'],
 [71,'2025 CFO less physical capex',"='Inputs'!C50-'Inputs'!C49",'After-interest cash flow, not unlevered FCFF.'],
];
s.getRange('B63:J74').format.font.name='Arial';
s.getRange('B63:J74').format.font.size=10;
s.getRange('B63:J74').format.rowHeight=20;
for(const [r,l,f,n] of calibration) {value(s,`B${r}`,l);formula(s,`C${r}`,f);value(s,`E${r}`,n);}
s.getRange('C64:C70').setNumberFormat(pct); s.getRange('C71').setNumberFormat(num);
// Derive the rounded forecast D&A assumption from the downloaded 10-K ratio.
formula(s,'C23','=ROUND(C67,3)');
s.getRange('C23').format.font.color='#000000'; s.getRange('C23').format.fill='#FFFFFF';
value(s,'B73','Working-capital intensity, ERP fade, margins and WACC are forward estimates, not reported 10-K facts.');
s.getRange('B76:J102').format.font.name='Arial';
s.getRange('B76:J102').format.font.size=10;
s.getRange('B76:J102').format.rowHeight=20;
band(s,'B76:D76','WACC sensitivity');
s.getRange('B77:D77').values=[['WACC','Required growth','Price check']];
s.getRange('B78:D80').values=result.sensitivity.map(x=>[x.wacc,x.growth,x.price]);
s.getRange('B78:C80').setNumberFormat(pct); s.getRange('D78:D80').setNumberFormat(usd);
value(s,'B82','Saved September 10 sensitivity results. Each rate was solved using the same five-year model and 2.5% terminal growth.');
value(s,'B83','To refresh in Excel, change C20 and Goal Seek C49 to 0 using C18 for each WACC. This table is a dated snapshot.');
band(s,'B86:C86','Enterprise-to-equity bridge');
const bridgeRows=[
 [87,'Enterprise value','=C46'],
 [88,'Less: debt principal',"=-SUM('Inputs'!C15:C18)"],
 [89,'Add: unrestricted cash',"='Inputs'!C19"],
 [90,'Less: pension / postretirement',"=-'Inputs'!C20"],
 [91,'Less: redeemable minority',"=-'Inputs'!C21"],
 [92,'Less: other minority',"=-'Inputs'!C22"],
 [93,'Less: VIE financing',"=-'Inputs'!C23"],
 [94,'Equity value','=C47'],
 [95,'Diluted shares proxy','=C26'],
 [96,'Value per share','=C48'],
 [99,'Bridge reconciliation','=SUM(C87:C93)-C94'],
];
for(const [r,l,f] of bridgeRows){value(s,`B${r}`,l);formula(s,`C${r}`,f);}
s.getRange('C87:C95').setNumberFormat('#,##0.000;(#,##0.000);"-"');
s.getRange('C96').setNumberFormat(usd);s.getRange('C99').setNumberFormat('0.00;(0.00);0.00');
value(s,'E99','Enterprise value plus signed balance-sheet adjustments must equal equity value.');
inputs.tabColor='#D8C8AE'; s.tabColor='#203E50';
wb.recalculate();
const actual=s.getRange('C48').values[0][0];
if(Math.abs(actual-result.price)>1e-7) throw Error(`Price mismatch: ${actual}`);
if(Math.abs(s.getRange('G32').values[0][0]-result.rows[4].revenue)>1e-7) throw Error('Revenue mismatch');
// Confirm that editing the discount rate changes the same forecast valuation.
value(s,'C20',.095); wb.recalculate();
if(!(s.getRange('C48').values[0][0]<actual)) throw Error('WACC recalculation failed');
value(s,'C20',.085); wb.recalculate();
console.log((await wb.inspect({kind:'region',sheetId:s.name,range:'B6:C11',maxChars:2000,tableMaxRows:8,tableMaxCols:2})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:20},summary:'Formula error scan'})).ndjson);
for(const [sheet,range,name] of [[s,'B2:J27','summary'],[s,'B30:J60','forecast'],[s,'B63:J74','calibration'],[s,'B76:J100','sensitivity_bridge'],[inputs,'B2:J40','inputs'],[inputs,'B43:J59','history']]) {
  const preview=await wb.render({sheetName:sheet.name,range,scale:1.5,format:'png'});
  await fs.writeFile(`${out}${name}.png`,new Uint8Array(await preview.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(`${out}GOLF_reverse_DCF.xlsx`);
const n=x=>x.toLocaleString('en-US',{minimumFractionDigits:1,maximumFractionDigits:1});
const p=x=>(x*100).toFixed(2)+'%';
const rows=result.rows;
const line=(label,fn)=>`| ${label} | ${rows.map(fn).join(' | ')} |`;
const terminalRevenue=rows[4].revenue*(1+result.terminal_growth);
const terminalEbit=terminalRevenue*.135;
const report=`# GOLF full reverse discounted cash flow

Valuation date: September 10, 2026. All amounts are USD millions except share prices. This report updates the earlier September 8 analysis.

At **$85.29 per share**, this model requires **${p(result.growth)} annual revenue growth for five years**, reaching **$${n(rows[4].revenue)} million** of sales. This is a conditional requirement, not a prediction.

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
${line('Revenue growth',()=>p(result.growth))}
${line('Revenue',r=>n(r.revenue))}
${line('EBIT margin',r=>p(r.ebit/r.revenue))}
${line('EBIT',r=>n(r.ebit))}
${line('NOPAT',r=>n(r.nopat))}
${line('Add: D&A',r=>n(r.da))}
${line('Less: physical capex',r=>'('+n(r.capex)+')')}
${line('Less: additional NWC',r=>'('+n(r.nwc)+')')}
${line('Less: net ERP',r=>'('+n(r.erp)+')')}
${line('Free cash flow',r=>n(r.fcff))}
${line('Present value',r=>n(r.pv))}

Present value of explicit cash flows: **$${n(rows.reduce((a,r)=>a+r.pv,0))} million**.

## Terminal calculation

| Year 6 calculation | Amount |
|---|---:|
| Revenue | ${n(terminalRevenue)} |
| EBIT | ${n(terminalEbit)} |
| NOPAT | ${n(terminalEbit*.77)} |
| Add: D&A | ${n(terminalRevenue*.022)} |
| Less: physical capex | (${n(terminalRevenue*.035)}) |
| Less: additional NWC | (${n((terminalRevenue-rows[4].revenue)*.20)}) |
| Less: net ERP | (${n(5*1.025)}) |
| Free cash flow | **${n(result.terminal_fcff)}** |

Terminal value at Year 5 = Year 6 FCFF / (WACC − terminal growth) = **$${n(result.terminal_fcff/(result.wacc-result.terminal_growth))} million**.

Discounting this value five years at 8.5% produces **$${n(result.pv_terminal)} million**.

Year 6 FCFF rises because additional working-capital investment falls when growth slows immediately to 2.5%. The model rebuilds this investment rather than simply growing Year 5 FCFF.

## Enterprise value to equity value

| Calculation | Amount |
|---|---:|
| PV of explicit cash flows | ${n(rows.reduce((a,r)=>a+r.pv,0))} |
| PV of terminal value | ${n(result.pv_terminal)} |
| Enterprise value | **${n(result.ev)}** |
| Less: debt principal proxy | (965.141) |
| Add: unrestricted cash | 66.600 |
| Less: pension and postretirement | (68.005) |
| Less: redeemable minority interest | (1.180) |
| Less: other minority interest | (0.761) |
| Less: VIE financing | (7.500) |
| Equity value | **${n(result.equity)}** |
| Diluted shares proxy (millions) | 58.582333 |
| Value per share | **$85.29** |

Debt comprises $441.6 million revolving borrowings, $500 million notes, $22.902 million short-term debt and $0.639 million current long-term debt. Shares combine 58.405044 million outstanding on July 31 with 0.177289 million incremental Q2 dilution. Source: [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1672013/000167201326000158/golf-20260630.htm).

## WACC sensitivity

Each scenario independently solves the same model for the $85.29 price. Other inputs remain fixed, including 2.5% terminal growth.

| WACC | Required annual revenue growth |
|---|---:|
${result.sensitivity.map(x=>`| ${p(x.wacc)} | ${p(x.growth)} |`).join('\n')}

## Interpretation and limitations

Required revenue growth of ${p(result.growth)} substantially exceeds 2025 growth of 4.1%. Sales nearly double from the starting run rate, while EBIT margins rise above the 2025 level of 11.7%.

Terminal value contributes **${p(result.terminal_share)}** of enterprise value. The immediate growth slowdown reduces working-capital investment materially. A smoother growth fade or more capacity investment could increase required growth.

June balance-sheet figures predate the quote. All unrestricted cash is added. Principal and carrying values approximate debt, pension and minority claims. Residual noncurrent finance leases are not separately quantified. Operating leases remain operating expenses, and no separately appraised investments are added. No future buyback benefit is assumed.

This is one combination of growth, margins and investment that supports the price. It does not establish a unique market forecast or prove the shares are overpriced.

## Reproduction and checks

Run \`python3 GOLF/valuation/reverse_dcf.py\` from the workspace root. It prints the full forecast and sensitivities and checks each solved price against $85.29.

In Excel, after changing assumptions, set C49 to zero by changing C18 using Goal Seek. The WACC table is a dated snapshot; re-solve each WACC to refresh it. Workbook formulas were recalculated and matched to Python, including the equity bridge. Native Excel Goal Seek was not tested.
`;
await fs.writeFile(`${out}GOLF_reverse_DCF.md`,report);
await fs.writeFile(new URL('../../GOLF/valuation/DCF_2026-09-08.md',import.meta.url),report.replace('../../GOLF/golf%2010k%20HTML.html','../golf%2010k%20HTML.html'));
