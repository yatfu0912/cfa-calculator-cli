"""Statistics CLI commands."""

import typer
from typing import List
from cfa_calculator.formulas.stats_formulas import (
    calculate_mean,
    calculate_median,
    calculate_mode,
    calculate_variance,
    calculate_std_dev,
    calculate_covariance_stats,
    calculate_correlation_stats,
    calculate_skewness,
    calculate_kurtosis,
    calculate_z_score,
    calculate_confidence_interval,
    calculate_percentile,
    calculate_range,
    calculate_coefficient_of_variation,
)
from cfa_calculator.utils.formatters import format_result, print_error
from cfa_calculator.utils.validators import validate_list_length, validate_equal_length

app = typer.Typer(help="Statistical calculations")


@app.command()
def descriptive(
    data: str = typer.Option(..., "--data", "-d", help="Data values as comma-separated (e.g., 10,15,12,18,20)"),
    sample: bool = typer.Option(True, "--sample", help="Use sample statistics (default: True)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate descriptive statistics (mean, median, mode, std dev, variance)."""
    try:
        values = [float(x.strip()) for x in data.split(",")]
        validate_list_length(values, 2, "Data")

        mean = calculate_mean(values)
        median = calculate_median(values)
        try:
            mode = calculate_mode(values)
        except:
            mode = None
        variance = calculate_variance(values, sample)
        std_dev = calculate_std_dev(values, sample)
        data_range = calculate_range(values)

        inputs = {
            "Data Points": len(values),
            "Type": "Sample" if sample else "Population",
        }

        results = {
            "Mean": f"{mean:.4f}",
            "Median": f"{median:.4f}",
            "Mode": f"{mode:.4f}" if mode is not None else "N/A",
            "Std Deviation": f"{std_dev:.4f}",
            "Variance": f"{variance:.4f}",
            "Range": f"{data_range:.4f}",
        }

        formula = "Sample: s = √[Σ(x-x̄)²/(n-1)]; Population: σ = √[Σ(x-μ)²/n]" if explain else None

        format_result("Descriptive Statistics", inputs, results, formula)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def covariance(
    data1: str = typer.Option(..., "--data1", help="First dataset as comma-separated values"),
    data2: str = typer.Option(..., "--data2", help="Second dataset as comma-separated values"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate covariance and correlation between two datasets."""
    try:
        values1 = [float(x.strip()) for x in data1.split(",")]
        values2 = [float(x.strip()) for x in data2.split(",")]

        validate_list_length(values1, 2, "Data1")
        validate_list_length(values2, 2, "Data2")
        validate_equal_length(values1, values2, "Data1", "Data2")

        cov = calculate_covariance_stats(values1, values2)
        corr = calculate_correlation_stats(values1, values2)

        inputs = {
            "Data Points": len(values1),
        }

        results = {
            "Covariance": f"{cov:.6f}",
            "Correlation": f"{corr:.4f}",
        }

        formula = "Cov(X,Y) = Σ[(x-x̄)(y-ȳ)]/(n-1); r = Cov(X,Y)/(σx×σy)" if explain else None
        notes = "Correlation ranges from -1 (perfect negative) to +1 (perfect positive)"

        format_result("Covariance & Correlation", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def skewness(
    data: str = typer.Option(..., "--data", "-d", help="Data values as comma-separated"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate skewness (measure of asymmetry)."""
    try:
        values = [float(x.strip()) for x in data.split(",")]
        validate_list_length(values, 3, "Data")

        skew = calculate_skewness(values)

        inputs = {
            "Data Points": len(values),
        }

        results = {
            "Skewness": f"{skew:.4f}",
        }

        formula = "Skewness = E[(X-μ)³]/σ³" if explain else None
        notes = "Positive: right-skewed; Negative: left-skewed; Zero: symmetric"

        format_result("Skewness", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def kurtosis(
    data: str = typer.Option(..., "--data", "-d", help="Data values as comma-separated"),
    excess: bool = typer.Option(True, "--excess", help="Calculate excess kurtosis (default: True)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate kurtosis (measure of tail heaviness)."""
    try:
        values = [float(x.strip()) for x in data.split(",")]
        validate_list_length(values, 4, "Data")

        kurt = calculate_kurtosis(values, excess)

        inputs = {
            "Data Points": len(values),
            "Type": "Excess Kurtosis" if excess else "Raw Kurtosis",
        }

        results = {
            "Kurtosis": f"{kurt:.4f}",
        }

        formula = "Excess Kurtosis = E[(X-μ)⁴]/σ⁴ - 3" if explain else None
        notes = "Excess > 0: heavy tails (leptokurtic); < 0: light tails (platykurtic)"

        format_result("Kurtosis", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def zscore(
    value: float = typer.Option(..., "--value", "-v", help="Value to standardize"),
    mean: float = typer.Option(..., "--mean", "-m", help="Mean of the distribution"),
    std_dev: float = typer.Option(..., "--std", "-s", help="Standard deviation"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate z-score (standardized score)."""
    try:
        z = calculate_z_score(value, mean, std_dev)

        inputs = {
            "Value (x)": value,
            "Mean (μ)": mean,
            "Std Dev (σ)": std_dev,
        }

        results = {
            "Z-Score": f"{z:.4f}",
        }

        formula = "z = (x - μ) / σ" if explain else None
        notes = "Z-score indicates how many standard deviations from the mean"

        format_result("Z-Score", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def confidence_interval(
    data: str = typer.Option(..., "--data", "-d", help="Data values as comma-separated"),
    confidence: float = typer.Option(0.95, "--confidence", "-c", help="Confidence level (e.g., 0.95 for 95%)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate confidence interval for the mean."""
    try:
        values = [float(x.strip()) for x in data.split(",")]
        validate_list_length(values, 2, "Data")

        if confidence <= 0 or confidence >= 1:
            raise ValueError("Confidence level must be between 0 and 1")

        mean, lower, upper = calculate_confidence_interval(values, confidence)

        inputs = {
            "Data Points": len(values),
            "Confidence Level": f"{confidence * 100:.1f}%",
        }

        results = {
            "Mean": f"{mean:.4f}",
            "Lower Bound": f"{lower:.4f}",
            "Upper Bound": f"{upper:.4f}",
            "Margin of Error": f"{(upper - lower) / 2:.4f}",
        }

        formula = "CI = x̄ ± t(α/2) × (s/√n)" if explain else None
        notes = f"We are {confidence*100:.0f}% confident the true mean lies in this interval"

        format_result("Confidence Interval", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def percentile(
    data: str = typer.Option(..., "--data", "-d", help="Data values as comma-separated"),
    percentile: float = typer.Option(..., "--percentile", "-p", help="Percentile to calculate (0-100)"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate percentile."""
    try:
        values = [float(x.strip()) for x in data.split(",")]
        validate_list_length(values, 2, "Data")

        result = calculate_percentile(values, percentile)

        inputs = {
            "Data Points": len(values),
            "Percentile": f"{percentile}th",
        }

        results = {
            "Value": f"{result:.4f}",
        }

        formula = None
        notes = f"{percentile}% of values are below {result:.4f}"

        format_result("Percentile", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command()
def cv(
    data: str = typer.Option(..., "--data", "-d", help="Data values as comma-separated"),
    explain: bool = typer.Option(False, "--explain", help="Show formula explanation"),
):
    """Calculate coefficient of variation."""
    try:
        values = [float(x.strip()) for x in data.split(",")]
        validate_list_length(values, 2, "Data")

        result = calculate_coefficient_of_variation(values)

        inputs = {
            "Data Points": len(values),
        }

        results = {
            "Coefficient of Variation": f"{result:.2f}%",
        }

        formula = "CV = (σ / μ) × 100%" if explain else None
        notes = "CV measures relative variability; useful for comparing datasets with different units"

        format_result("Coefficient of Variation", inputs, results, formula, notes)

    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)
