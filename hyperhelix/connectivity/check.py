"""Connectivity checking utilities for network and API availability."""

from __future__ import annotations

import socket
import logging
import time
import urllib.request
from typing import Dict, List, Optional, Tuple, Union
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

def check_api_key_validity(key_name: str, test_url: str, 
                          header_name: str = "Authorization",
                          header_prefix: str = "Bearer ",
                          default: Optional[str] = None) -> bool:
    """Check if an API key is valid by making a test request.
    
    Args:
        key_name: Environment variable name containing the API key.
        test_url: URL to test the API key against.
        header_name: Name of the header to include the key in.
        header_prefix: Prefix to add before the key in the header.
        default: Default value if key is not found in environment.
        
    Returns:
        True if the API key is valid, False otherwise.
    """
    api_key = get_api_key(key_name, default)
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
