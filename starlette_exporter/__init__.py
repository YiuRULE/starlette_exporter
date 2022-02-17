import os
from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST,
    REGISTRY,
    multiprocess,
    CollectorRegistry,
    start_http_server,
)
from starlette.requests import Request
from starlette.responses import Response

from .middleware import PrometheusMiddleware


def handle_metrics(request: Request) -> Response:
    """A handler to expose Prometheus metrics
    Example usage:

        ```
        app.add_middleware(PrometheusMiddleware)
        app.add_route("/metrics", handle_metrics)
        ```
    """
    registry = REGISTRY
    if (
        'prometheus_multiproc_dir' in os.environ
        or 'PROMETHEUS_MULTIPROC_DIR' in os.environ
    ):
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)

    headers = {'Content-Type': CONTENT_TYPE_LATEST}
    return Response(generate_latest(registry), status_code=200, headers=headers)

def handle_metric_server(prom_port: int = 8000) -> None:
    """A handler to expose Prometheus metrics
    Example usage:
        ```
        app.add_middleware(PrometheusMiddleware)
        app.add_route("/metrics", handle_metrics)
        ```
    """
    start_http_server(prom_port)
