"""Pricing service for the Greenhill Food Co-op Ordering System.

This module implements the order-total calculation logic described in
GOS-12. It supports two pricing models:

* ``unit``  -- price is charged per whole unit (e.g. a jar of tahini
               at $9.80 each). Quantities are integers.
* ``kg``    -- price is charged per kilogram (e.g. rolled oats at
               $3.40/kg). Quantities are decimals.

All monetary values are rounded to two decimal places using
``round(..., 2)`` so that floating-point artefacts such as
0.1 + 0.2 = 0.30000000000000004 never reach the user.
"""

from __future__ import annotations


def calculate_line_total(price: float, quantity, pricing_unit: str) -> float:
    """Calculate the total price for a single order line.

    :param price: unit price (per unit) or price per kilogram.
    :param quantity: number of units (int) or kilograms (float).
    :param pricing_unit: ``'unit'`` or ``'kg'``.
    :return: the line total, rounded to 2 decimal places.
    :raises ValueError: if ``pricing_unit`` is not recognised.
    """
    if pricing_unit == 'unit':
        return round(price * int(quantity), 2)
    elif pricing_unit == 'kg':
        return round(price * float(quantity), 2)
    else:
        raise ValueError(f"Unknown pricing unit: {pricing_unit}")


def calculate_order_total(line_items) -> float:
    """Calculate the grand total for an order.

    :param line_items: iterable of dicts, each containing a
        ``'line_total'`` key.
    :return: sum of all line totals, rounded to 2 decimal places.
    """
    total = sum(item['line_total'] for item in line_items)
    return round(total, 2)


def format_currency(amount: float) -> str:
    """Format a monetary amount as ``$X.XX`` with exactly 2 decimals."""
    return f"${amount:.2f}"
