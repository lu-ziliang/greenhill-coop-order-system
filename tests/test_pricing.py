"""Automated tests for the pricing service (GOS-14).

Run with:  pytest -v
"""

from app.services.pricing import (
    calculate_line_total,
    calculate_order_total,
    format_currency,
)


class TestPerUnitPricing:
    def test_three_units_at_9_80(self):
        # 3 x $9.80 = $29.40
        result = calculate_line_total(9.80, 3, 'unit')
        assert result == 29.40

    def test_one_unit_at_19_60(self):
        result = calculate_line_total(19.60, 1, 'unit')
        assert result == 19.60

    def test_ten_units_at_2_50(self):
        result = calculate_line_total(2.50, 10, 'unit')
        assert result == 25.00


class TestPerKgPricing:
    def test_one_and_half_kg_at_3_40(self):
        # 1.5 x $3.40 = $5.10
        result = calculate_line_total(3.40, 1.5, 'kg')
        assert result == 5.10

    def test_quarter_kg_at_3_40(self):
        # 0.25 x $3.40 = $0.85
        result = calculate_line_total(3.40, 0.25, 'kg')
        assert result == 0.85

    def test_two_kg_at_5_20(self):
        result = calculate_line_total(5.20, 2, 'kg')
        assert result == 10.40


class TestOrderTotal:
    def test_sum_of_multiple_lines(self):
        items = [
            {'line_total': 29.40},
            {'line_total': 5.10},
            {'line_total': 10.40},
        ]
        result = calculate_order_total(items)
        assert result == 44.90  # 29.40 + 5.10 + 10.40

    def test_empty_order(self):
        result = calculate_order_total([])
        assert result == 0.00


class TestCurrencyFormatting:
    def test_format_whole_number(self):
        assert format_currency(25.0) == "$25.00"

    def test_format_decimal(self):
        assert format_currency(5.1) == "$5.10"

    def test_format_rounds_to_two_decimals(self):
        assert format_currency(29.4) == "$29.40"


class TestFloatingPoint:
    def test_no_floating_point_error(self):
        # 0.1 + 0.2 style errors should not occur with explicit rounding
        result = calculate_line_total(0.1, 3, 'unit')
        assert result == 0.30
        assert result != 0.30000000000000004

    def test_unknown_pricing_unit_raises(self):
        import pytest
        with pytest.raises(ValueError):
            calculate_line_total(5.0, 1, 'litre')
