
def is_sequence(x):
    """
    Returns True if the argument is an iterable sequence that isn't a character string.
    """
    try:
        return iter(x) and not isinstance(x, str) and not isinstance(x, unicode)
    except TypeError:
        return False