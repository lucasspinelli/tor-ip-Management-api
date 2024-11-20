import logging
from flask import Blueprint, request, jsonify
from app.auth_utils import require_jwt, require_role
from app.database import get_db, insert_excluded_ip, get_excluded_ips, delete_excluded_ip
from app.services import fetch_tor_ips
from app.utils import validate_ip

bp = Blueprint('api', __name__)

@bp.route('/tor-ips', methods=['GET'])
@require_jwt
def get_tor_ips():
    """Endpoint to fetch TOR IPs from external sources."""
    try:
        tor_ips = fetch_tor_ips()
        logging.info(f"{len(tor_ips)} IPs TOR recuperados das fontes externas.")
        return jsonify({"tor_ips": list(tor_ips)})
    except Exception as e:
        logging.error(f"Erro ao buscar IPs TOR: {e}")
        return jsonify({"error": "Erro ao buscar IPs TOR."}), 500

@bp.route('/excluded-ips', methods=['POST'])
@require_role("admin")
def exclude_ip():
    """
    Endpoint to add IPs to exclusion list.
    These formats are allowed:
    {
        "ip": "192.168.0.1"
    }
    or
    {
        "ips": ["192.168.0.1", "10.0.0.1"]
    }
    """
    data = request.json

    ip = data.get('ip')
    ips = data.get('ips')

    results = []

    if ip:
        if validate_ip(ip):
            try:
                insert_excluded_ip(ip)
                logging.info(f"IP {ip} added with success.")
                results.append({"ip": ip, "status": "success"})
            except Exception as e:
                logging.error(f"Error to add the IP {ip} to exclusion list: {e}")
                results.append({"ip": ip, "status": "error", "error": str(e)})
        else:
            logging.warning(f"Invalid Format: {ip}")
            return jsonify({"error": f"Invalid IP address: {ip}"}), 400

    elif ips:
        for ip in ips:
            if validate_ip(ip):
                try:
                    insert_excluded_ip(ip)
                    logging.info(f"IP {ip} added with success.")
                    results.append({"ip": ip, "status": "success"})
                except Exception as e:
                    logging.error(f"Error to add the IP {ip} to exclusion list: {e}")
                    results.append({"ip": ip, "status": "error", "error": str(e)})
            else:
                logging.warning(f"Invalid Format: {ip}")
                results.append({"ip": ip, "status": "error", "error": "Invalid IP address format"})
    else:
        logging.warning("Theres no valid data provided.")
        return jsonify({"error": "No valid data provided. Provide 'ip' or 'ips'."}), 400

    return jsonify({"results": results}), 201

@bp.route('/filtered-tor-ips', methods=['GET'])
@require_jwt
def get_filtered_tor_ips():
    """Endpoint to fetch filtered TOR IPs."""
    try:
        tor_ips = fetch_tor_ips()
        excluded_ips = get_excluded_ips()
        filtered_ips = tor_ips - excluded_ips
        return jsonify({"filtered_tor_ips": list(filtered_ips)})
    except Exception as e:
        logging.error(f"Error on search filtered TOR IPs: {e}")
        return jsonify({"error": "Error on search filtered TOR IPs."}), 500

@bp.route('/excluded-ips', methods=['DELETE'])
@require_role("admin")
def delete_excluded_ip_endpoint():
    """
    Endpoint to remove an IP of the exclusion list.
    (JSON):
    {
        "ip": "192.168.0.1"
    }
    """
    data = request.json
    ip = data.get('ip')

    if not ip:
        logging.warning("Attempt of exclusion without provide an IP.")
        return jsonify({"error": "IP address is required"}), 400

    try:
        delete_excluded_ip(ip)
        logging.info(f"IP {ip} was removed successfully.")
        return jsonify({"message": f"IP {ip} successfully removed from exclusion list."}), 200
    except ValueError as e:
        logging.warning(f"Attempt of exclusion of non existent IP: {ip}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Error to remove IP {ip}: {e}")
        return jsonify({"error": str(e)}), 500
