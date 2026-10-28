"""Prometheus metrics. Defined once at module level."""
from prometheus_client import Counter, Gauge, Histogram

REQUESTS = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "path", "status"]
)
LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP request latency in seconds", ["method", "path"]
)
DB_UP = Gauge("app_db_up", "1 if the database is reachable, 0 otherwise")
