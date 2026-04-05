# CFA Calculator CLI

A lightweight, fast, and user-friendly command-line tool for CFA (Chartered Financial Analyst) financial calculations.

## Features

- **Time Value of Money (TVM)**: Future Value, Present Value, Annuities, Perpetuities, EAR
- **Portfolio Management**: Sharpe Ratio, Treynor Ratio, Jensen's Alpha, Beta, CAPM, Sortino Ratio
- **Fixed Income**: Bond Price, YTM, YTC, Current Yield, Macaulay Duration, Modified Duration, Convexity
- **Equity Valuation**: DDM, FCFE, P/E valuation (coming soon)
- **Derivatives**: Black-Scholes, Option pricing (coming soon)
- **Statistics**: Mean, Standard Deviation, Correlation, Covariance (coming soon)

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

## Input Formats

### Rates
- Use decimal format: `0.05` for 5%
- Or percentage format: `5` (will be converted to 0.05)

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
│   │   ├── tvm.py
│   │   └── portfolio.py
│   ├── formulas/            # Core calculation logic
│   │   ├── tvm_formulas.py
│   │   └── portfolio_formulas.py
│   └── utils/               # Utilities
│       ├── formatters.py
│       └── validators.py
└── tests/                   # Test suite
```

## Roadmap

### ✅ Phase 1 (Completed)
- Time Value of Money calculations
- Portfolio Management calculations
- Fixed Income calculations (Bond pricing, YTM, YTC, Duration, Convexity)

### Phase 2 (Coming Soon)
- Statistics module (Mean, Std Dev, Skewness, Kurtosis, Confidence Intervals)
- Other calculations (NPV, IRR, Money-weighted vs Time-weighted Return)

### Phase 3 (Future)
- Equity Valuation (DDM, FCFE, P/E)
- Derivatives (Black-Scholes, Binomial model, Put-Call Parity)

### Phase 4 (Advanced Features)
- Save/load calculation sessions
- Export results to CSV/JSON
- Formula reference lookup
- Multi-currency support

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
