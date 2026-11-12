"""
Tests for reports API endpoints.
"""
import pytest

from main import quarter_label, quarter_months
from mock_data import orders


class TestReportsEndpoints:
    """Test suite for reports endpoints."""

    def test_get_quarterly_reports_structure(self, client):
        """Test that quarterly reports have the expected fields and order."""
        response = client.get("/api/reports/quarterly")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for quarter in data:
            for field in ["quarter", "total_orders", "total_revenue", "delivered_orders",
                          "avg_order_value", "fulfillment_rate"]:
                assert field in quarter

        keys = [(q["quarter"][-4:], q["quarter"][:2]) for q in data]
        assert keys == sorted(keys)

    def test_quarterly_orders_total_matches_raw_orders(self, client):
        """Test that quarterly order counts add up to all orders with a valid date."""
        response = client.get("/api/reports/quarterly")
        data = response.json()

        total = sum(q["total_orders"] for q in data)
        expected = sum(1 for o in orders if quarter_label(o.get("order_date", "")))
        assert total == expected

    def test_quarterly_reports_filter_by_warehouse(self, client):
        """Test that the warehouse filter restricts quarterly totals."""
        response = client.get("/api/reports/quarterly?warehouse=Tokyo")
        assert response.status_code == 200

        total = sum(q["total_orders"] for q in response.json())
        expected = sum(1 for o in orders if o.get("warehouse") == "Tokyo")
        assert total == expected

    def test_quarterly_reports_filter_by_status(self, client):
        """Test that the status filter restricts quarterly totals."""
        response = client.get("/api/reports/quarterly?status=Delivered")
        assert response.status_code == 200

        for quarter in response.json():
            assert quarter["fulfillment_rate"] == 100.0

    def test_quarterly_reports_filter_by_quarter(self, client):
        """Test that a quarter filter returns only that quarter."""
        response = client.get("/api/reports/quarterly?month=Q2-2025")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["quarter"] == "Q2-2025"

    def test_get_monthly_trends_structure(self, client):
        """Test that monthly trends have the expected fields and order."""
        response = client.get("/api/reports/monthly-trends")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for month in data:
            for field in ["month", "order_count", "revenue", "delivered_count"]:
                assert field in month

        months = [m["month"] for m in data]
        assert months == sorted(months)

    def test_monthly_trends_filter_by_warehouse(self, client):
        """Test that the warehouse filter restricts monthly order counts."""
        response = client.get("/api/reports/monthly-trends?warehouse=London")
        assert response.status_code == 200

        total = sum(m["order_count"] for m in response.json())
        expected = sum(1 for o in orders if o.get("warehouse") == "London")
        assert total == expected

    def test_monthly_trends_filter_by_single_month(self, client):
        """Test that a month filter returns only that month."""
        response = client.get("/api/reports/monthly-trends?month=2025-01")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["month"] == "2025-01"

    def test_monthly_trends_combined_filters(self, client):
        """Test that warehouse and status filters apply together."""
        response = client.get("/api/reports/monthly-trends?warehouse=Tokyo&status=Delivered")
        assert response.status_code == 200

        total = sum(m["delivered_count"] for m in response.json())
        expected = sum(
            1 for o in orders
            if o.get("warehouse") == "Tokyo" and o.get("status") == "Delivered"
        )
        assert total == expected


class TestQuarterHelpers:
    """Test suite for quarter label helpers."""

    def test_quarter_label_for_each_quarter(self):
        """Test that month numbers map to the correct quarter."""
        assert quarter_label("2025-01-15") == "Q1-2025"
        assert quarter_label("2025-04-01") == "Q2-2025"
        assert quarter_label("2025-09-30") == "Q3-2025"
        assert quarter_label("2025-12-31") == "Q4-2025"

    def test_quarter_label_uses_order_year(self):
        """Test that quarters are not limited to 2025."""
        assert quarter_label("2026-11-12") == "Q4-2026"

    def test_quarter_label_invalid_date_returns_none(self):
        """Test that missing or malformed dates produce no quarter."""
        assert quarter_label("") is None
        assert quarter_label("2025-13-01") is None
        assert quarter_label("not-a-date") is None

    def test_quarter_months_expands_label(self):
        """Test that a quarter label expands to its three month prefixes."""
        assert quarter_months("Q3-2026") == ["2026-07", "2026-08", "2026-09"]

    def test_quarter_months_rejects_malformed_label(self):
        """Test that malformed quarter labels are rejected."""
        assert quarter_months("Q5-2025") is None
        assert quarter_months("2025-Q1") is None
