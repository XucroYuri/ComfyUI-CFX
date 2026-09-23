"""Boolean logic primitives."""

OPERATIONS = (
    "and",
    "or",
    "xor",
    "nand",
    "nor",
    "a_implies_b",
    "not_a",
    "not_b",
)


def _apply(operation: str, a: bool, b: bool) -> bool:
    if operation == "and":
        return a and b
    if operation == "or":
        return a or b
    if operation == "xor":
        return bool(a) ^ bool(b)
    if operation == "nand":
        return not (a and b)
    if operation == "nor":
        return not (a or b)
    if operation == "a_implies_b":
        return (not a) or b
    if operation == "not_a":
        return not a
    if operation == "not_b":
        return not b
    raise ValueError(f"boolean: unknown operation {operation!r}")


class CFXBoolean:
    """Boolean algebra on two inputs; real bools only, no string truthiness."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("BOOLEAN", {"default": False}),
                "operation": (list(OPERATIONS), {"default": "and"}),
            },
            "optional": {
                "b": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("result",)
    FUNCTION = "compute"
    CATEGORY = "ComfyUI-Primitives/Logic"

    def compute(self, a, operation, b=False):
        return (_apply(operation, bool(a), bool(b)),)


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_boolean": CFXBoolean,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_boolean": "ComfyUI-Primitives · Boolean",
}
