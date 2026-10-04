"""
src/starter/tools.py

MCP tool implementations for the starter repository.

This module contains exactly ONE tool — the calculator — which exists
purely to demonstrate the MCP tool lifecycle:

    Tool definition
          ↓
    Tool registration   (done in server.py)
          ↓
    Tool discovery      (client calls tools/list)
          ↓
    Tool invocation     (client calls tools/call)
          ↓
    Tool result

Safety note
-----------
We do NOT use Python's built-in eval().  Instead we parse the expression
using the `ast` module which lets us inspect and reject anything that is
not a safe arithmetic operation before evaluating it.
"""

from __future__ import annotations

import ast
import operator
from typing import Any

# ──────────────────────────────────────────────────────────────────────────────
# Allowed operators — only simple arithmetic is permitted
# ──────────────────────────────────────────────────────────────────────────────
_SAFE_OPS: dict[type[ast.operator], Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,  # unary minus  e.g. -5
}


class UnsafeExpressionError(ValueError):
    """Raised when the expression contains a disallowed construct."""


def _eval_node(node: ast.expr) -> float:
    """Recursively evaluate a safe AST node.

    Only numeric literals and the operators in _SAFE_OPS are allowed.
    Any other construct raises UnsafeExpressionError.
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise UnsafeExpressionError(f"Non-numeric constant: {node.value!r}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise UnsafeExpressionError(f"Unsupported operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _SAFE_OPS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise UnsafeExpressionError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return _SAFE_OPS[op_type](operand)

    raise UnsafeExpressionError(f"Disallowed AST node: {type(node).__name__}")


def safe_calculate(expression: str) -> str:
    """Evaluate a simple arithmetic expression and return the result as a string.

    Parameters
    ----------
    expression:
        A plain arithmetic expression such as ``"2 + 3"``, ``"10 * 5"``,
        or ``"(10 + 5) / 3"``.

    Returns
    -------
    str
        The numeric result formatted as a string.

    Raises
    ------
    ValueError
        If the expression is empty, syntactically invalid, unsafe, or
        causes a division-by-zero.
    """
    expression = expression.strip()
    if not expression:
        raise ValueError("Expression must not be empty.")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc

    try:
        result = _eval_node(tree.body)
    except UnsafeExpressionError as exc:
        raise ValueError(str(exc)) from exc
    except ZeroDivisionError:
        raise ValueError("Division by zero is not allowed.")

    # Return integer representation when the result is a whole number.
    if result == int(result):
        return str(int(result))
    return str(result)


# ──────────────────────────────────────────────────────────────────────────────
# MCP tool descriptor (used by server.py for registration)
# ──────────────────────────────────────────────────────────────────────────────
CALCULATOR_TOOL_DESCRIPTION = {
    "name": "calculate",
    "description": (
        "Evaluate a simple arithmetic expression. "
        "Supports +, -, *, /, //, %, and ** operators, and parentheses. "
        "Example: '2 + 3', '10 * 5', '(10 + 5) / 3'."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The arithmetic expression to evaluate.",
            }
        },
        "required": ["expression"],
    },
}
