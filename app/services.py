import requests
import re
import logging

def extract_ips(data):
    """REGEX to extract IPV4 and IPV6 of the pages"""
    ip_pattern = r"""
    \b
    (
        (?:[0-9]{1,3}\.){3}[0-9]{1,3}                 # IPv4
        |
        (?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}      # IPv6 completo
        |
        (?:[a-fA-F0-9]{1,4}:){1,7}:                   # IPv6 com "::" no final
        |
        (?:[a-fA-F0-9]{1,4}:){1,6}:[a-fA-F0-9]{1,4}   # IPv6 com "::" no meio
    )
    \b
    """

    ips = re.findall(ip_pattern, data, re.VERBOSE)
    return ips

def fetch_tor_ips():
    """Fetch TOR ips of external sources. I used the three provided websites to do so"""
    sources = [
        "https://www.dan.me.uk/tornodes",
        "https://www.bigdatacloud.com/insights/tor-exit-nodes",
        "https://check.torproject.org/torbulkexitlist"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    ips = []

    for source in sources:
        try:
            response = requests.get(source, timeout=10, headers=headers)
            response.raise_for_status()

            ips = extract_ips(response.text)
        except Exception as e:
            logging.error(f"Error to get IP from {source}: {e}")

    return ips
