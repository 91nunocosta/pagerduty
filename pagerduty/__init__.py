"""PagerDuty client API for the interview."""

__version__ = "0.1.0"


def fib(number: int) -> int:
    """Compute an element in the fibonacci sequence.

    >>> fib(0)
    0

    Args:
        number (int): the position in the sequence.

    Returns:
        The number-th element in the fibonacci sequence.
    """
    if number == 0:
        return 0

    if number == 1:
        return 1

    return fib(number - 1) + fib(number - 2)
