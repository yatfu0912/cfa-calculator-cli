"""Utility functions for parsing mathematical expressions."""

import re


def parse_math_expression(value: str) -> float:
    """
    Parse and evaluate a mathematical expression.

    Supports:
    - Basic arithmetic: +, -, *, /
    - Parentheses: ()
    - Exponentiation: ** or ^
    - Fractions: 1/12

    Args:
        value: String containing a mathematical expression

    Returns:
        Evaluated result as float

    Examples:
        parse_math_expression("13*3*365") -> 14235.0
        parse_math_expression("100000*(1+0.05)") -> 105000.0
        parse_math_expression("1/12") -> 0.0833...
        parse_math_expression("2^3") -> 8.0
    """
    # Replace ^ with ** for exponentiation
    value = value.replace('^', '**')

    # Security: only allow safe mathematical operations
    # Remove any characters that aren't numbers, operators, parentheses, or decimal points
    if not re.match(r'^[\d\+\-\*\/\(\)\.\s\*]+$', value):
        raise ValueError(f"Invalid characters in expression: {value}")

    try:
        # Evaluate the expression safely
        result = eval(value, {"__builtins__": {}}, {})
        return float(result)
    except Exception as e:
        raise ValueError(f"Cannot evaluate expression '{value}': {str(e)}")


def parse_numeric_input(value: str) -> float:
    """
    Parse numeric input that may be a simple number or a mathematical expression.

    Args:
        value: String containing a number or expression

    Returns:
        Evaluated result as float
    """
    value = value.strip()

    # If it contains operators, treat as expression
    if any(op in value for op in ['+', '-', '*', '/', '(', ')', '^']):
        return parse_math_expression(value)

    # Otherwise, parse as simple number
    return float(value)
