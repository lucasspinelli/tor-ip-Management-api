import ipaddress

def validate_ip(ip):
    """Validate if the input string is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
