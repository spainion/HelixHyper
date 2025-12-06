"""Connectivity checking utilities for network and API availability."""

from __future__ import annotations

import logging
import socket
import time
import urllib.request
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Tuple, Union

import requests

from ..utils import get_api_key

logger = logging.getLogger(__name__)

def is_internet_available(timeout: float = 3.0) -> bool:
    """Check if internet connection is available.
    
    Args:
        timeout: Maximum time to wait for connection in seconds.
        
    Returns:
        True if internet is available, False otherwise.
    """
    try:
        # Try connecting to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        try:
            # Fallback to Cloudflare's DNS
            socket.create_connection(("1.1.1.1", 53), timeout=timeout)
            return True
        except OSError:
            logger.warning("No internet connection available")
            return False

def check_url_availability(url: str, timeout: float = 3.0) -> bool:
    """Check if a URL is available.
    
    Args:
        url: The URL to check.
        timeout: Maximum time to wait for response in seconds.
        
    Returns:
        True if the URL is available, False otherwise.
    """
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code < 400
    except (requests.RequestException, urllib.error.URLError) as e:
        logger.warning(f"Failed to connect to {url}: {str(e)}")
        return False

def check_api_key_validity(
    key_name: str,
    test_url: str,
    header_name: str = "Authorization",
    header_prefix: str = "Bearer ",
    default: Optional[str] = None,
    api_key: Optional[str] = None,
) -> bool:
    """Check if an API key is valid by making a test request.

    Args:
        key_name: Environment variable name containing the API key.
        test_url: URL to test the API key against.
        header_name: Name of the header to include the key in.
        header_prefix: Prefix to add before the key in the header.
        default: Default value if key is not found in environment.
        api_key: Optional key to use instead of reloading from environment.

    Returns:
        True if the API key is valid, False otherwise.
    """
    api_key = api_key or get_api_key(key_name, default)
    if not api_key:
        return False
        
    headers = {header_name: f"{header_prefix}{api_key}"}
    try:
        response = requests.get(test_url, headers=headers, timeout=5.0)
        return response.status_code < 400
    except requests.RequestException as e:
        logger.warning(f"API key validation failed for {key_name}: {str(e)}")
        return False

def wait_for_connectivity(services: List[str], max_retries: int = 30,
                         retry_interval: float = 2.0) -> Dict[str, bool]:
    """Wait for connectivity to specified services.
    
    This function is particularly useful during container startup to ensure
    that all required services are available before proceeding.
    
    Args:
        services: List of service URLs to check.
        max_retries: Maximum number of retry attempts.
        retry_interval: Time to wait between retries in seconds.
        
    Returns:
        Dictionary mapping service URLs to their availability status.
    """
    results = {service: False for service in services}
    retry_count = 0
    
    while retry_count < max_retries and not all(results.values()):
        for service in services:
            if not results[service]:
                results[service] = check_url_availability(service)
                
        if all(results.values()):
            logger.info("All required services are available")
            break
            
        retry_count += 1
        if retry_count < max_retries:
            logger.info(f"Waiting for services to become available. "
                      f"Retry {retry_count}/{max_retries}")
            time.sleep(retry_interval)
    
    for service, available in results.items():
        if not available:
            logger.warning(f"Service {service} is not available after {max_retries} attempts")

    return results


ApiKeyTarget = Union[str, Mapping[str, str]]


def _normalize_api_key_target(target: ApiKeyTarget) -> Tuple[str, str, str, Optional[str]]:
    if isinstance(target, str):
        return target, "Authorization", "Bearer ", None

    return (
        target["test_url"],
        target.get("header_name", "Authorization"),
        target.get("header_prefix", "Bearer "),
        target.get("default"),
    )


def collect_connectivity_report(
    service_urls: Optional[Iterable[str]] = None,
    api_key_targets: Optional[Mapping[str, ApiKeyTarget]] = None,
    *,
    internet_check: Callable[[float], bool] = is_internet_available,
    url_checker: Callable[[str, float], bool] = check_url_availability,
    key_validator: Callable[[str, str, str, str, Optional[str], Optional[str]], bool] = check_api_key_validity,
    timeout: float = 3.0,
) -> Dict[str, Union[bool, Dict[str, Dict[str, Union[bool, str]]]]]:
    """Build a connectivity report for internet, services, and configured API keys.

    The report is structured to surface whether internet is reachable, which
    services respond, and whether required API keys are both present and valid.

    Args:
        service_urls: URLs to probe for availability.
        api_key_targets: Mapping of env var names to test target configuration.
        internet_check: Callable used to test raw internet reachability.
        url_checker: Callable used to test specific service URLs.
        key_validator: Callable used to validate API keys.
        timeout: Timeout passed to checkers when supported.

    Returns:
        Dictionary containing internet status, per-service availability, and
        per-key presence/validity details.
    """

    internet_available = internet_check(timeout)

    services_report: Dict[str, bool] = {}
    if service_urls:
        for url in service_urls:
            services_report[url] = url_checker(url, timeout)

    api_keys_report: Dict[str, Dict[str, Union[bool, str]]] = {}
    if api_key_targets:
        for key_name, raw_target in api_key_targets.items():
            test_url, header_name, header_prefix, default = _normalize_api_key_target(raw_target)
            api_key = get_api_key(key_name, default)
            api_keys_report[key_name] = {
                "present": bool(api_key),
                "valid": bool(api_key)
                and key_validator(
                    key_name,
                    test_url,
                    header_name=header_name,
                    header_prefix=header_prefix,
                    default=default,
                    api_key=api_key,
                ),
                "test_url": test_url,
            }

    return {
        "internet": internet_available,
        "services": services_report,
        "api_keys": api_keys_report,
    }
