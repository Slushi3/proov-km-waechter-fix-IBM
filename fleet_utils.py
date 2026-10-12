# fleet_utils.py
# Utility helpers for KM-Waechter. Modernised 2025.
# Dead functions removed: parse_service_date (2014 garage form), chunk_list (unused since 2013),
# is_due (duplicate of km_wachter.needs_service).

MILES_PER_KM = 0.621371   # was 1.609 (that is km-per-mile, the reciprocal — wrong)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a percentage string."""
    return f"{int(value)}%"


def mean(values: list) -> float:
    """Return the arithmetic mean of a list of numbers, or 0 for an empty list.

    Note: statistics.mean() has existed since Python 3.4; prefer that in new code.
    """
    if not values:
        return 0
    return sum(values) / len(values)
