"""Wildcard type helper for ComfyUI nodes.

``AnyType`` is a ``str`` subclass whose inequality comparison is always ``False``,
which makes ComfyUI accept a wildcard socket for any upstream type. The pattern
originates from pythongosssss / rgthree (both MIT).
"""


class AnyType(str):
    def __ne__(self, other):
        return False


any_type = AnyType("*")
