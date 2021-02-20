# NOTE: in 3.8+ this should be Literal["yes", "no"]
def bool_to_str(val: bool) -> str:
    """Convert a boolean into a yes/no value."""
    return "yes" if val else "no"

