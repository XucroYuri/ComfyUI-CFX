"""Numeric expression evaluation with an AST allowlist."""

import ast
import math

MAX_EXPRESSION = 4096

FUNCTIONS = {
    "min": min,
    "max": max,
    "abs": abs,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
    "sqrt": math.sqrt,
    "pow": pow,
    "sum": sum,
    "len": len,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "true": True,
    "false": False,
}

ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.BoolOp,
    ast.IfExp,
    ast.Call,
    ast.Name,
    ast.Constant,
    ast.Load,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.Not,
    ast.And,
    ast.Or,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
)


def evaluate(expression: str, variables: dict):
    """Evaluate ``expression`` with only allowlisted syntax and names."""
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("math: expression is empty")
    if len(expression) > MAX_EXPRESSION:
        raise ValueError(f"math: expression exceeds {MAX_EXPRESSION} characters")

    tree = ast.parse(expression, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"math: unsupported syntax {type(node).__name__}")

    scope = {**CONSTANTS, **FUNCTIONS, **variables}
    try:
        result = eval(compile(tree, "<cfx-math>", "eval"), {"__builtins__": {}}, scope)
    except ZeroDivisionError as exc:
        raise ValueError("math: division by zero") from exc
    except NameError as exc:
        raise ValueError(f"math: unknown name ({exc})") from exc

    if isinstance(result, bool):
        result = int(result)
    if not isinstance(result, (int, float)):
        raise ValueError(f"math: expression returned {type(result).__name__}, expected a number")
    if isinstance(result, float) and (math.isnan(result) or math.isinf(result)):
        raise ValueError("math: expression produced a non-finite value")
    return result


class CFXMath:
    """Evaluate a math expression over up to three numeric inputs."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "expression": ("STRING", {"default": "a + b", "multiline": False}),
            },
            "optional": {
                "a": ("INT,FLOAT", {"default": 0}),
                "b": ("INT,FLOAT", {"default": 0}),
                "c": ("INT,FLOAT", {"default": 0}),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT")
    RETURN_NAMES = ("int", "float")
    FUNCTION = "compute"
    CATEGORY = "ComfyUI-Primitives/Math"

    def compute(self, expression, a=0, b=0, c=0):
        result = evaluate(expression, {"a": a, "b": b, "c": c})
        return (int(result), float(result))


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_math": CFXMath,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_math": "ComfyUI-Primitives · Math",
}
