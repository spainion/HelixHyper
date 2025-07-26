"""Stub for an OpenRouter API client used in run_workflow tests."""

class OpenRouterClient:
    """Fake client that always fails connectivity.

    The real implementation would check API keys and network
    connectivity.  For the purpose of the tests this stub simply
    returns ``False`` to allow conditional skipping.
    """

    def check_connection(self) -> bool:
        return False