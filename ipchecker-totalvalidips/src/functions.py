import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This will allow CORS for all routes

# Check if IP addresses are valid or not

# Check if IPv4 address is valid
def is_valid_ipv4(ip):
    # Should be 4 groups of values separated by full stops
    parts = ip.split('.')
    return len(parts) == 4

# Check if IPv6 address is valid
def is_valid_ipv6(ip):
    # Should be between 2 and 8 groups of values separated by colons
    parts = ip.split(':')
    return 2 <= len(parts) <= 8

# Create an array to store the IPs post-processing
def validate_ips(ip_list):
    valid_count = 0
    results = []

    for ip in ip_list:
        if is_valid_ipv4(ip) or is_valid_ipv6(ip):
            results.append(f"{ip} -> valid")
            valid_count += 1
        else:
            results.append(f"{ip} -> invalid")

    return valid_count, results

# Create a route to handle the validation request
@app.route('/validate_ips', methods=['GET'])
def validate_ips_route():
    items = request.args.get('items')
    if not items:
        return jsonify({'error': 'No items provided'}), 400
    ip_list = items.split(',')
    total_valid_ips, results = validate_ips([ip.strip() for ip in ip_list])
    return jsonify({'total_valid_ips': total_valid_ips, 'results': results})

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)