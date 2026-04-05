# CFA Calculator CLI

A comprehensive, fast, and user-friendly command-line tool for CFA (Chartered Financial Analyst) financial calculations.

[![Tests](https://img.shields.io/badge/tests-160%20passed-brightgreen)](https://github.com/yatfu0912/cfa-calculator-cli)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Features

### ✅ Complete Implementation

- **Interactive Mode**: Bilingual (English/Chinese) menu-driven interface with step-by-step parameter input
- **Mathematical Expression Support**: Use expressions like `13*3*365` or `0.05+0.02` in any numeric parameter - no need to pre-calculate!
- **Time Value of Money (TVM)**: Future Value, Present Value, Annuities, Perpetuities, EAR
- **Portfolio Management**: Sharpe Ratio, Treynor Ratio, Jensen's Alpha, Beta, CAPM, Sortino Ratio
- **Fixed Income**: Bond Price, YTM, YTC, Current Yield, Macaulay Duration, Modified Duration, Convexity
- **Statistics**: Descriptive Statistics, Covariance, Correlation, Skewness, Kurtosis, Z-Score, Confidence Intervals, Percentiles, Coefficient of Variation
- **Other Calculations**: NPV, IRR, Money-Weighted Return, Time-Weighted Return, Payback Period, Profitability Index, MIRR
- **Equity Valuation**: Gordon Growth Model (DDM), Two-Stage DDM, FCFE, P/E Valuation, Justified P/E, PEG Ratio
- **Derivatives**: Black-Scholes-Merton, Binomial Option Pricing, Put-Call Parity, Option Payoffs with Greeks

### 🎯 Key Highlights

- **160 Tests** - 100% passing with high coverage
- **50+ Calculations** - Covering all major CFA topics
- **Bilingual Support** - English and Chinese throughout
- **Expression Parser** - Built-in calculator for complex inputs
- **Beautiful Output** - Rich formatting with tables and colors

## Quick Start

### Interactive Mode (Recommended for Beginners)

Launch the interactive mode with bilingual prompts (English/Chinese):

```bash
cfa --interactive
# or simply
cfa -i
# or just
cfa
```

The interactive mode provides:
- Step-by-step parameter input
- Menu-driven interface
- Bilingual support (English/Chinese)
- Beautiful formatted output
- No need to remember command syntax

### Command-Line Mode (For Advanced Users)

```bash
# Time Value of Money
cfa tvm fv --pv 1000 --rate 0.05 --n 10

# Mathematical expressions supported!
cfa tvm fv --pv "13*3*365" --rate 0.07 --n 1
cfa tvm fv --pv 10000 --rate "0.05+0.02" --n 5
cfa tvm fv --pv 100000 --rate 0.07 --n "1/12" --freq 12

# Portfolio Management
cfa portfolio sharpe --return 0.12 --rf 0.03 --std 0.15

# Equity Valuation
cfa equity ddm --dividend 5.0 --required-return 0.12 --growth 0.05

# Derivatives
cfa option black-scholes --type call --spot 100 --strike 100 --time 1.0 --rf 0.05 --vol 0.20

# Get help
cfa --help
cfa equity --help
cfa option --help
```

**Mathematical Expression Support:**

All numeric parameters support mathematical expressions - no need to pre-calculate values!

**Supported Operators:**
- Basic arithmetic: `+`, `-`, `*`, `/`
- Parentheses: `()`
- Exponentiation: `**` or `^`
- Fractions: `1/12`

**Examples:**
```bash
# Calculate with expressions
cfa tvm fv --pv "13*3*365" --rate 0.07 --n 1
# Output: Present Value (PV) = 14235.00 (13*3*365)

# Combine rates
cfa tvm fv --pv 10000 --rate "0.05+0.02" --n 5
# Output: Interest Rate (r) = 7.00% (0.05+0.02)

# Use fractions
cfa tvm fv --pv 100000 --rate 0.07 --n "1/12" --freq 12
# Output: Number of Years (n) = 0.0833 (1/12)

# Complex expressions
cfa tvm pv --fv "1000*(1+0.05)^2" --rate 0.06 --n 10

# Parentheses for order of operations
cfa tvm fv --pv "(100+200)*3" --rate 0.05 --n 5
```

**Benefits:**
- ✅ No need to use a calculator first
- ✅ Transparent - shows both expression and result
- ✅ Secure - only allows mathematical operations
- ✅ Works with all numeric parameters

## Installation

### Requirements

- Python 3.10 or higher
- pip

### Install from source

```bash
cd "Calculator CLI"
pip install -e .
```

This will install the `cfa` command globally.

## Usage

### General Help

```bash
cfa --help
cfa tvm --help
cfa portfolio --help
```

### Time Value of Money Examples

**Future Value:**
```bash
cfa tvm fv --pv 1000 --rate 0.05 --n 10
# Calculate FV of $1,000 at 5% for 10 years
# Result: ~$1,628.89
```

**Present Value:**
```bash
cfa tvm pv --fv 15000 --rate 0.06 --n 10
# Calculate PV of $15,000 discounted at 6% for 10 years
```

**Annuity:**
```bash
cfa tvm annuity --pmt 1000 --rate 0.05 --n 20 --type pv --annuity-type ordinary
# Calculate PV of ordinary annuity with $1,000 payments
```

**Perpetuity:**
```bash
cfa tvm perpetuity --pmt 100 --rate 0.05
# Calculate PV of perpetuity with $100 annual payments

cfa tvm perpetuity --pmt 100 --rate 0.08 --growth 0.03
# Calculate PV of growing perpetuity
```

**Effective Annual Rate:**
```bash
cfa tvm ear --stated-rate 0.08 --freq 2
# Calculate EAR with 8% stated rate, semi-annual compounding
```

### Portfolio Management Examples

**Sharpe Ratio:**
```bash
cfa portfolio sharpe --return 0.12 --rf 0.03 --std 0.15
# Calculate Sharpe ratio
# Result: 0.60
```

**Treynor Ratio:**
```bash
cfa portfolio treynor --return 0.15 --rf 0.03 --beta 1.2
# Calculate Treynor ratio
```

**Jensen's Alpha:**
```bash
cfa portfolio alpha --return 0.15 --rf 0.03 --beta 1.2 --market-return 0.11
# Calculate Jensen's Alpha
```

**Beta:**
```bash
cfa portfolio beta --asset-returns "0.10,0.15,0.12,0.08,0.14" --market-returns "0.08,0.12,0.10,0.06,0.11"
# Calculate beta from historical returns
```

**CAPM:**
```bash
cfa portfolio capm --rf 0.03 --beta 1.2 --market-return 0.11
# Calculate required return using CAPM
```

**Portfolio Return:**
```bash
cfa portfolio portfolio-return --weights "0.6,0.4" --returns "0.10,0.15"
# Calculate expected portfolio return
```

**Covariance & Correlation:**
```bash
cfa portfolio covariance --returns1 "0.10,0.12,0.14" --returns2 "0.08,0.10,0.12"
# Calculate covariance and correlation between two assets
```

### Fixed Income Examples

**Bond Price:**
```bash
cfa bond price --face 1000 --coupon-rate 0.06 --ytm 0.055 --years 8 --freq 2
# Calculate bond price with 6% coupon, 5.5% YTM, 8 years to maturity
# Result: ~$1,032.01 (premium bond)
```

**Yield to Maturity (YTM):**
```bash
cfa bond ytm --price 1050 --face 1000 --coupon-rate 0.06 --years 5 --freq 2
# Calculate YTM for a bond trading at $1,050
# Result: ~4.86%
```

**Duration:**
```bash
cfa bond duration --face 1000 --coupon-rate 0.05 --ytm 0.06 --years 10 --freq 2
# Calculate Macaulay and Modified Duration
# Macaulay: ~7.90 years, Modified: ~7.67
```

**Convexity:**
```bash
cfa bond convexity --face 1000 --coupon-rate 0.06 --ytm 0.06 --years 10 --freq 2
# Calculate convexity to measure price-yield curvature
```

### Statistics Examples

**Descriptive Statistics:**
```bash
cfa stats descriptive --data "10,15,12,18,20,14,16"
# Calculate mean, median, mode, std dev, variance, range
# Result: Mean=15.0, Median=15.0, Std Dev=3.42
```

**Covariance & Correlation:**
```bash
cfa stats covariance --data1 "10,12,14,16" --data2 "8,10,12,14"
# Calculate covariance and correlation between two datasets
```

**Skewness:**
```bash
cfa stats skewness --data "1,2,3,4,5,6,7,8,9,10"
# Measure asymmetry of distribution
```

**Z-Score:**
```bash
cfa stats zscore --value 110 --mean 100 --std 10
# Calculate standardized score
# Result: z = 1.0
```

**Confidence Interval:**
```bash
cfa stats confidence-interval --data "10,12,14,16,18,20" --confidence 0.95
# Calculate 95% confidence interval for the mean
```

### Other Calculations Examples

**Net Present Value (NPV):**
```bash
cfa other npv --rate 0.10 --cash-flows "-1000,300,400,500,600"
# Calculate NPV with 10% discount rate
# Result: $388.77 (Accept project)
```

**Internal Rate of Return (IRR):**
```bash
cfa other irr --cash-flows "-1000,400,400,400"
# Calculate IRR
# Result: 9.70%
```

**Money-Weighted Return:**
```bash
cfa other money-weighted --beginning 1000 --ending 1200
# Calculate money-weighted return (similar to IRR)
```

**Time-Weighted Return:**
```bash
cfa other time-weighted --beginning "1000,1100" --ending "1100,1210"
# Calculate time-weighted return (eliminates cash flow timing effects)
# Result: 21.00%
```

**Payback Period:**
```bash
cfa other payback --investment 1000 --cash-flows "400,400,400"
# Calculate payback period
# Result: 2.50 years
```

**Profitability Index:**
```bash
cfa other profitability-index --rate 0.10 --investment 1000 --cash-flows "500,500,500"
# Calculate PI (PV of future CFs / Initial Investment)
# Result: PI > 1 means accept project
```

**Modified IRR (MIRR):**
```bash
cfa other mirr --cash-flows "-1000,300,400,500,600" --finance-rate 0.10 --reinvest-rate 0.12
# Calculate MIRR with different financing and reinvestment rates
```

**Yield to Call (YTC):**
```bash
cfa bond ytc --price 1050 --face 1000 --coupon-rate 0.08 --years-to-call 5 --call-price 1030 --freq 2
# Calculate yield if bond is called at earliest call date
```

**Current Yield:**
```bash
cfa bond current-yield --price 1050 --face 1000 --coupon-rate 0.06
# Calculate current yield (annual coupon / current price)
# Result: ~5.71%
```

### Equity Valuation Examples

**Gordon Growth Model (DDM):**
```bash
cfa equity ddm --dividend 5.0 --required-return 0.12 --growth 0.05
# Calculate stock value using constant growth DDM
# Result: $71.43
```

**Two-Stage DDM:**
```bash
cfa equity multistage-ddm --current-dividend 2.0 --high-growth 0.15 --high-years 5 --stable-growth 0.05 --required-return 0.12
# Calculate stock value with high growth period followed by stable growth
```

**FCFE Valuation:**
```bash
cfa equity fcfe --fcfe 10.0 --required-return 0.12 --growth 0.05
# Calculate equity value using Free Cash Flow to Equity
# Result: $142.86
```

**P/E Valuation:**
```bash
cfa equity pe-valuation --eps 5.0 --pe 15.0
# Calculate stock value using P/E ratio
# Result: $75.00
```

**Justified P/E Ratio:**
```bash
cfa equity justified-pe --payout 0.40 --required-return 0.12 --growth 0.05
# Calculate justified P/E ratio using Gordon Growth Model
# Result: 6.00
```

**PEG Ratio:**
```bash
cfa equity peg --pe 20.0 --growth 0.15
# Calculate PEG ratio (P/E to Growth)
# Result: 1.33 (PEG < 1: undervalued, PEG > 1: overvalued)
```

### Derivatives Examples

**Option Payoff:**
```bash
cfa option payoff --type call --spot 110 --strike 100 --premium 3.0
# Calculate call option profit at expiration
# Result: $7.00 profit

cfa option payoff --type put --spot 90 --strike 100
# Calculate put option payoff
# Result: $10.00
```

**Put-Call Parity:**
```bash
cfa option put-call-parity --put 5.0 --spot 100 --strike 100 --rf 0.05 --time 1.0
# Solve for call price using put-call parity
# Result: Call = $9.88
```

**Black-Scholes Option Pricing:**
```bash
cfa option black-scholes --type call --spot 100 --strike 100 --time 1.0 --rf 0.05 --vol 0.20
# Calculate call option price and Greeks
# Result: Option Price ~$10.45, Delta ~0.64, Gamma, Vega, Theta, Rho

cfa option black-scholes --type put --spot 100 --strike 100 --time 1.0 --rf 0.05 --vol 0.20 --div 0.02
# Calculate put option price with dividend yield
```

**Binomial Option Pricing:**
```bash
cfa option binomial --type call --spot 100 --strike 100 --time 1.0 --rf 0.05 --vol 0.20 --steps 100
# Calculate European call using binomial tree (100 steps)

cfa option binomial --type put --spot 100 --strike 100 --time 1.0 --rf 0.05 --vol 0.20 --steps 100 --american
# Calculate American put option (allows early exercise)
```

### Using the --explain Flag

Add `--explain` to any command to see the formula:

```bash
cfa tvm fv --pv 1000 --rate 0.05 --n 10 --explain
# Shows: FV = PV × (1 + r/freq)^(n×freq)

cfa bond duration --face 1000 --coupon-rate 0.05 --ytm 0.06 --years 10 --freq 2 --explain
# Shows: ModDur = MacDur / (1 + YTM/freq)
```

## Command Reference

### Time Value of Money (tvm)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `fv` | Future Value | `--pv`, `--rate`, `--n`, `--freq` |
| `pv` | Present Value | `--fv`, `--rate`, `--n`, `--freq` |
| `annuity` | Annuity FV/PV | `--pmt`, `--rate`, `--n`, `--type`, `--annuity-type` |
| `perpetuity` | Perpetuity PV | `--pmt`, `--rate`, `--growth` (optional) |
| `ear` | Effective Annual Rate | `--stated-rate`, `--freq` |

### Portfolio Management (portfolio)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `sharpe` | Sharpe Ratio | `--return`, `--rf`, `--std` |
| `treynor` | Treynor Ratio | `--return`, `--rf`, `--beta` |
| `alpha` | Jensen's Alpha | `--return`, `--rf`, `--beta`, `--market-return` |
| `sortino` | Sortino Ratio | `--return`, `--target`, `--downside-std` |
| `beta` | Beta | `--asset-returns`, `--market-returns` |
| `capm` | CAPM Required Return | `--rf`, `--beta`, `--market-return` |
| `portfolio-return` | Portfolio Return | `--weights`, `--returns` |
| `covariance` | Covariance & Correlation | `--returns1`, `--returns2` |

### Fixed Income (bond)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `price` | Bond Price | `--face`, `--coupon-rate`, `--ytm`, `--years`, `--freq` |
| `ytm` | Yield to Maturity | `--price`, `--face`, `--coupon-rate`, `--years`, `--freq` |
| `ytc` | Yield to Call | `--price`, `--face`, `--coupon-rate`, `--years-to-call`, `--call-price`, `--freq` |
| `current-yield` | Current Yield | `--price`, `--face`, `--coupon-rate` |
| `duration` | Macaulay & Modified Duration | `--face`, `--coupon-rate`, `--ytm`, `--years`, `--freq` |
| `convexity` | Convexity | `--face`, `--coupon-rate`, `--ytm`, `--years`, `--freq` |

### Statistics (stats)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `descriptive` | Descriptive Statistics | `--data`, `--sample` |
| `covariance` | Covariance & Correlation | `--data1`, `--data2` |
| `skewness` | Skewness | `--data` |
| `kurtosis` | Kurtosis | `--data`, `--excess` |
| `zscore` | Z-Score | `--value`, `--mean`, `--std` |
| `confidence-interval` | Confidence Interval | `--data`, `--confidence` |
| `percentile` | Percentile | `--data`, `--percentile` |
| `cv` | Coefficient of Variation | `--data` |

### Other Calculations (other)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `npv` | Net Present Value | `--rate`, `--cash-flows` |
| `irr` | Internal Rate of Return | `--cash-flows`, `--guess` |
| `money-weighted` | Money-Weighted Return | `--beginning`, `--ending`, `--cash-flows`, `--times` |
| `time-weighted` | Time-Weighted Return | `--beginning`, `--ending` |
| `payback` | Payback Period | `--investment`, `--cash-flows` |
| `profitability-index` | Profitability Index | `--rate`, `--investment`, `--cash-flows` |
| `mirr` | Modified IRR | `--cash-flows`, `--finance-rate`, `--reinvest-rate` |

### Equity Valuation (equity)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `ddm` | Gordon Growth Model | `--dividend`, `--required-return`, `--growth` |
| `multistage-ddm` | Two-Stage DDM | `--current-dividend`, `--high-growth`, `--high-years`, `--stable-growth`, `--required-return` |
| `fcfe` | FCFE Valuation | `--fcfe`, `--required-return`, `--growth` |
| `pe-valuation` | P/E Valuation | `--eps`, `--pe` |
| `justified-pe` | Justified P/E Ratio | `--payout`, `--required-return`, `--growth` |
| `peg` | PEG Ratio | `--pe`, `--growth` |

### Derivatives (option)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `payoff` | Option Payoff | `--type`, `--spot`, `--strike`, `--premium` (optional) |
| `put-call-parity` | Put-Call Parity | Provide 5 of 6: `--call`, `--put`, `--spot`, `--strike`, `--rf`, `--time` |
| `black-scholes` | Black-Scholes Pricing | `--type`, `--spot`, `--strike`, `--time`, `--rf`, `--vol`, `--div` (optional) |
| `binomial` | Binomial Tree Pricing | `--type`, `--spot`, `--strike`, `--time`, `--rf`, `--vol`, `--steps`, `--american` (flag) |

## Input Formats

### Rates
- Use decimal format: `0.05` for 5%
- Or percentage format: `5` (will be converted to 0.05)
- Expressions supported: `"0.05+0.02"` for 7%

### Numbers
- Simple numbers: `1000`, `15000`
- Expressions: `"13*3*365"`, `"1000*(1+0.05)"`
- Fractions: `"1/12"` for 1 month, `"6/12"` for 6 months

### Lists
- Comma-separated values: `"0.10,0.15,0.12"`
- No spaces (or use quotes if spaces included)

### Frequencies
- Annual: `1`
- Semi-annual: `2`
- Quarterly: `4`
- Monthly: `12`
- Weekly: `52`
- Daily: `365`

### Expression Examples

**Time Calculations:**
```bash
# 1 month
--n "1/12"

# 6 months  
--n "6/12"

# 18 months
--n "18/12"
```

**Amount Calculations:**
```bash
# Daily savings for a year
--pv "13*365"

# Monthly payment times periods
--pmt "1000*12"

# Compound calculation
--fv "1000*(1+0.05)^2"
```

**Rate Calculations:**
```bash
# Add risk premium
--rate "0.05+0.02"

# Average of two rates
--rate "(0.05+0.07)/2"
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Running Tests with Coverage

```bash
pytest tests/ -v --cov=src/cfa_calculator --cov-report=term-missing
```

### Project Structure

```
Calculator CLI/
├── src/cfa_calculator/
│   ├── main.py              # CLI entry point
│   ├── commands/            # Command modules
│   │   ├── tvm.py           # Time Value of Money
│   │   ├── portfolio.py     # Portfolio Management
│   │   ├── bond.py          # Fixed Income
│   │   ├── stats.py         # Statistics
│   │   ├── other.py         # NPV, IRR, etc.
│   │   ├── equity.py        # Equity Valuation
│   │   └── option.py        # Derivatives
│   ├── formulas/            # Core calculation logic
│   │   ├── tvm_formulas.py
│   │   ├── portfolio_formulas.py
│   │   ├── bond_formulas.py
│   │   ├── stats_formulas.py
│   │   ├── other_formulas.py
│   │   ├── equity_formulas.py
│   │   └── option_formulas.py
│   ├── utils/               # Utilities
│   │   ├── formatters.py    # Rich output formatting
│   │   └── validators.py    # Input validation
│   └── interactive.py       # Interactive mode (coming soon)
└── tests/                   # Test suite (160 tests, 100% pass)
    ├── test_tvm.py
    ├── test_portfolio.py
    ├── test_bond.py
    ├── test_stats.py
    ├── test_other.py
    ├── test_equity.py
    └── test_option.py
```

## Roadmap

### ✅ Phase 1 (Completed)
- Time Value of Money calculations (FV, PV, Annuities, Perpetuities, EAR)
- Portfolio Management calculations (Sharpe, Treynor, Jensen's Alpha, Beta, CAPM, Sortino)
- Fixed Income calculations (Bond pricing, YTM, YTC, Duration, Convexity)

### ✅ Phase 2 (Completed)
- Statistics module (Descriptive stats, Covariance, Correlation, Skewness, Kurtosis, Z-Score, Confidence Intervals, Percentiles, CV)
- Other calculations (NPV, IRR, Money-weighted Return, Time-weighted Return, Payback Period, Profitability Index, MIRR)

### ✅ Phase 3 (Completed)
- Equity Valuation (Gordon Growth Model, Two-Stage DDM, FCFE, P/E Valuation, Justified P/E, PEG Ratio)
- Derivatives (Black-Scholes-Merton with Greeks, Binomial Option Pricing, Put-Call Parity, Option Payoffs)

### ✅ Phase 4 (Completed)
- Interactive mode with guided prompts (bilingual: English/Chinese)
- Complete menu system for all 7 modules
- Step-by-step parameter input
- Beautiful formatted output with Rich library
- Mathematical expression support for all numeric parameters
- Enhanced help documentation with examples and formula references

## Test Coverage

- **Total Tests**: 160
- **Pass Rate**: 100%
- **Coverage by Module**:
  - TVM: 100%
  - Portfolio: 77%
  - Bond: 93%
  - Stats: 96%
  - Other: 95%
  - Equity: 100%
  - Option: 82%

## Contributing

Contributions are welcome! Please ensure:
- All formulas match CFA curriculum exactly
- Tests are included for new features
- Code follows existing style conventions

## License

MIT License

## Support

For issues or questions, please open an issue on the project repository.

## Acknowledgments

Built for CFA candidates and finance professionals worldwide.
