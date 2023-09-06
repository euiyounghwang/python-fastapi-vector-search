
from prometheus_client import Counter, Histogram

# Define a counter metric
REQUESTS_COUNT = Counter(
    "requests_total", "Total number of requests", ["method", "endpoint", "status_code"]
)
# Define a histogram metric
REQUESTS_TIME = Histogram("requests_time", "Request processing time", ["method", "endpoint"])
api_request_summary = Histogram("api_request_summary", "Request processing time", ["method", "endpoint"])
api_request_counter = Counter("api_request_counter", "Request processing time", ["method", "endpoint", "http_status"])