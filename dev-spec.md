以下是 **Command Line CFA Calculator Tool** **Software Specification ：

-----

**Project Specification: CFA Calculator CLI Tool**

### 1. Project Overview

**Project Name:** CFA Calculator CLI  
**Version:** 1.0  
**Type:** Command Line Interface (CLI) Tool  
**Purpose:**  
A lightweight, fast, and user-friendly command-line tool that helps users calculate various metrics commonly used in Chartered Financial Analyst (CFA) curriculum, particularly in Quantitative Methods, Fixed Income, Equity Valuation, Derivatives, and Portfolio Management.

### 2. Objectives

- Provide accurate calculations for key CFA formulas
- Support both interactive mode and one-liner command mode
- Be easy to install and use (single binary preferred)
- Offer clear, well-formatted output with explanations
- Support future extensibility for more CFA topics

### 3. Target Users

- CFA Level I, II, and III candidates
- Finance students and professionals
- Self-study users who need quick formula validation or scenario testing

### 4. Core Features

#### 4.1 Calculation Modules

The tool shall support the following categories and formulas:

**A. Time Value of Money (TVM)**

- Future Value (FV)
- Present Value (PV)
- Annuity (Ordinary & Due)
- Perpetuity
- Growing Perpetuity
- Number of periods (N)
- Interest rate (I/Y)

**B. Statistical & Probability Concepts**

- Mean, Median, Mode
- Standard Deviation & Variance (population & sample)
- Covariance and Correlation
- Skewness and Kurtosis
- Probability (basic + Bayes’ Theorem)
- Z-score, T-score
- Confidence Intervals

**C. Portfolio Management**

- Expected Return (portfolio)
- Portfolio Variance & Standard Deviation (2+ assets)
- Sharpe Ratio
- Treynor Ratio
- Jensen’s Alpha
- Sortino Ratio
- Beta
- CAPM (Required Return)

**D. Fixed Income**

- Bond Price
- Yield to Maturity (YTM)
- Yield to Call (YTC)
- Current Yield
- Macaulay Duration
- Modified Duration
- Convexity
- Effective Duration / Convexity

**E. Equity Valuation**

- Dividend Discount Model (DDM) – Gordon Growth, Multi-stage
- Free Cash Flow to Equity (FCFE) Valuation
- Price/Earnings (P/E) Ratio valuation
- Enterprise Value / EBITDA

**F. Derivatives**

- Option Payoff (Call & Put)
- Put-Call Parity
- Black-Scholes Option Pricing (European)
- Binomial Option Pricing Model (basic)

**G. Other Common Calculations**

- Net Present Value (NPV)
- Internal Rate of Return (IRR)
- Money-weighted vs Time-weighted Return
- Effective Annual Rate (EAR) vs Stated Rate
- Forward Price, Futures Price
- Currency Forward / Spot / Interest Rate Parity

### 5. User Interface Requirements

#### 5.1 Command Structure

The CLI shall support two modes:

1. **Interactive Mode** (default when no arguments)
- User is guided through menus or prompts
2. **Command Mode** (one-liner)
- Example:
  
  ```bash
  cfa tvm fv --pv 1000 --rate 0.05 --n 10
  cfa portfolio sharpe --ret 0.12 --rf 0.03 --std 0.15
  cfa bond price --face 1000 --coupon 50 --ytm 0.04 --n 10 --freq 2
  ```

#### 5.2 Command Design Principles

- Use clear, intuitive subcommands (e.g. `cfa tvm`, `cfa portfolio`, `cfa bond`, `cfa option`)
- Support both long options (`--present-value`) and short options (`-p`) where appropriate
- Consistent parameter naming across modules
- Support both decimal (0.05) and percentage (5%) input where logical
- Output should include:
  - Input summary
  - Final calculated value(s)
  - Brief formula explanation (optional with `--explain` flag)
  - Key assumptions

### 6. Technical Requirements

- **Language:** Python 3.10+ (recommended) or Go (for single binary)
- **CLI Framework:**
  - Python → Typer or Click (preferred)
  - Go → Cobra
- **Math Library:** NumPy / SciPy for complex calculations (Python)
- **Output Format:** Clean, color-coded terminal output (using Rich or similar)
- **Configuration:** Optional config file for default settings (e.g., currency, rounding)
- **Installation:**
  - `pip install cfa-calculator` (Python)
  - Or single executable (`cfa` command)

### 7. Key Commands Examples

```bash
# TVM
cfa tvm fv --pv 10000 --rate 0.08 --n 5 --freq 1

# Sharpe Ratio
cfa portfolio sharpe --port-return 0.145 --rf-rate 0.035 --port-std 0.18

# Bond Price
cfa bond price --face 1000 --coupon-rate 0.06 --ytm 0.055 --years 8 --frequency 2

# Black-Scholes
cfa option blackscholes call --spot 100 --strike 95 --time 0.5 --rf 0.03 --vol 0.25
```

### 8. Additional Features (Phase 2)

- Save/load calculation sessions
- Export results to CSV / JSON
- Formula reference lookup (`cfa lookup sharpe`)
- Unit tests for all formulas
- Support for continuous compounding
- Multi-currency support
- Custom formula builder

### 9. Non-Functional Requirements

- Accuracy: Must match CFA curriculum formulas exactly
- Performance: Near-instant response (< 200ms)
- Usability: Clear help text and examples for every command
- Error Handling: Friendly error messages with suggestions
- Documentation: Full `--help` support + README with examples
- Cross-platform: Windows, macOS, Linux

### 10. Deliverables for AI Developer

1. This specification document
2. Detailed list of all formulas with exact mathematical definitions
3. Sample input/output for each major command
4. Proposed command tree structure
5. Test cases (edge cases included)


