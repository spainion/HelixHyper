"""Common API dependencies."""

from fastapi import Request

from ..core import HyperHelix


def get_graph(request: Request) -> HyperHelix:
    """Return the app's graph instance."""
    return request.app.state.graph
