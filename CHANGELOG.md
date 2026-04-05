# Changelog

All notable changes to the CFA Calculator CLI project will be documented in this file.

## [1.0.0] - 2026-04-06

### Added - Phase 4: Interactive Mode

- **Interactive Mode**: Full bilingual (English/Chinese) menu-driven interface
  - Launch with `cfa --interactive`, `cfa -i`, or just `cfa`
  - Step-by-step parameter input with prompts
  - Beautiful formatted output using Rich library
  - 22 interactive calculations across 7 modules

- **Interactive Modules**:
  - TVM: Future Value, Present Value, Annuity, Perpetuity, EAR
  - Portfolio: Sharpe Ratio, Treynor Ratio, Jensen's Alpha, Beta, CAPM
  - Bond: Bond Price, YTM, Duration
  - Stats: Descriptive Statistics, Z-Score
  - Other: NPV, IRR
  - Equity: Gordon Growth Model, P/E Valuation, PEG Ratio
  - Option: Option Payoff, Black-Scholes

### Added - Phase 3: Equity Valuation & Derivatives

- **Equity Valuation Module** (6 calculations):
  - Gordon Growth Model (constant growth DDM)
  - Two-Stage DDM (high growth + stable growth)
  - FCFE valuation model
  - P/E ratio valuation
  - Justified P/E ratio calculation
  - PEG ratio analysis

- **Derivatives Module** (4 calculations):
  - Option payoff calculations (call/put with premium)
  - Put-Call Parity solver (solve for any missing variable)
  - Black-Scholes-Merton option pricing with Greeks (Delta, Gamma, Vega, Theta, Rho)
  - Binomial tree option pricing (European and American options)

- **Testing**:
  - 53 new tests added (24 equity + 29 derivatives)
  - Total: 160 tests, 100% pass rate
  - Formula coverage: equity 100%, options 82%

### Added - Phase 2: Statistics & Other Calculations

- **Statistics Module** (10 calculations):
  - Descriptive statistics (mean, median, mode, variance, std dev)
  - Covariance and correlation
  - Skewness and kurtosis
  - Z-score
  - Confidence intervals
  - Percentiles
  - Coefficient of variation

- **Other Calculations Module** (7 calculations):
  - Net Present Value (NPV)
  - Internal Rate of Return (IRR)
  - Money-Weighted Return
  - Time-Weighted Return
  - Payback Period
  - Profitability Index
  - Modified IRR (MIRR)

### Added - Phase 1: Core Modules

- **Time Value of Money Module** (5 calculations):
  - Future Value (FV)
  - Present Value (PV)
  - Annuity FV/PV (ordinary and due)
  - Perpetuity (constant and growing)
  - Effective Annual Rate (EAR)

- **Portfolio Management Module** (8 calculations):
  - Portfolio return and variance
  - Sharpe Ratio
  - Treynor Ratio
  - Jensen's Alpha
  - Sortino Ratio
  - Beta calculation
  - CAPM required return
  - Covariance and correlation

- **Fixed Income Module** (6 calculations):
  - Bond price
  - Yield to Maturity (YTM)
  - Yield to Call (YTC)
  - Current Yield
  - Macaulay Duration
  - Modified Duration
  - Convexity

### Infrastructure

- **CLI Framework**: Typer with Rich formatting
- **Testing**: pytest with 160 tests (100% pass rate)
- **Documentation**: Comprehensive README with examples
- **Project Structure**: Modular design with separate formula and command modules

## Project Statistics

- **Total Commands**: 50+ financial calculations
- **Total Tests**: 160 (100% passing)
- **Modules**: 7 (TVM, Portfolio, Bond, Stats, Other, Equity, Option)
- **Lines of Code**: ~2,500+ (excluding tests)
- **Test Coverage**: 
  - TVM: 100%
  - Portfolio: 77%
  - Bond: 93%
  - Stats: 96%
  - Other: 95%
  - Equity: 100%
  - Option: 82%

## Future Plans (Phase 5)

- Save/load calculation sessions
- Export results to CSV/JSON
- Formula reference lookup
- Multi-currency support
- Historical data integration
- Batch calculations from CSV
