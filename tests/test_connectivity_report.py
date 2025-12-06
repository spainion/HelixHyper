import os

from hyperhelix.connectivity.check import collect_connectivity_report


def _restore_env(var_name: str, previous: str | None) -> None:
    if previous is None:
        os.environ.pop(var_name, None)
    else:
        os.environ[var_name] = previous


def test_collect_connectivity_report_with_present_key() -> None:
    previous_value = os.environ.get("EXAMPLE_KEY")
    os.environ["EXAMPLE_KEY"] = "token"

    try:
        report = collect_connectivity_report(
            service_urls=["https://service/health"],
            api_key_targets={
                "EXAMPLE_KEY": {
                    "test_url": "https://service/api",
                    "header_name": "X-Test",
                    "header_prefix": "",
                }
            },
            internet_check=lambda timeout: True,
            url_checker=lambda url, timeout: url == "https://service/health",
            key_validator=lambda key_name, test_url, header_name, header_prefix, default, api_key: api_key
            == "token"
            and test_url
            == "https://service/api",
        )
    finally:
        _restore_env("EXAMPLE_KEY", previous_value)

    assert report["internet"] is True
    assert report["services"] == {"https://service/health": True}

    key_report = report["api_keys"]["EXAMPLE_KEY"]
    assert key_report["present"] is True
    assert key_report["valid"] is True
    assert key_report["test_url"] == "https://service/api"


def test_collect_connectivity_report_with_missing_key() -> None:
    previous_value = os.environ.get("MISSING_KEY")
    os.environ.pop("MISSING_KEY", None)

    try:
        report = collect_connectivity_report(
            api_key_targets={"MISSING_KEY": "https://service/api"},
            internet_check=lambda timeout: False,
            url_checker=lambda url, timeout: False,
            key_validator=lambda *args, **kwargs: True,
        )
    finally:
        _restore_env("MISSING_KEY", previous_value)

    assert report["internet"] is False
    assert report["services"] == {}

    key_report = report["api_keys"]["MISSING_KEY"]
    assert key_report["present"] is False
    assert key_report["valid"] is False
    assert key_report["test_url"] == "https://service/api"
