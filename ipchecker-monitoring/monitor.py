import subprocess
import json
import time
import random
from datetime import datetime

def generate_random_ipv4():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def generate_random_ipv6():
    return ":".join("{:x}".format(random.randint(0, 65535)) for _ in range(8))

def generate_random_ip_addresses(count=5):
    ip_addresses = []
    for _ in range(count):
        if random.choice([True, False]):  # Randomly choose between IPv4 and IPv6
            ip_addresses.append(generate_random_ipv4())
        else:
            ip_addresses.append(generate_random_ipv6())
    return ip_addresses

def is_valid_ipv4(ip):
    parts = ip.split('.')
    return len(parts) == 4

def is_valid_ipv6(ip):
    parts = ip.split(':')
    return 2 <= len(parts) <= 8

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

def log_results_to_file(log_data, filename="monitoring_log.json"):
    try:
        with open(filename, "a") as file:
            json.dump(log_data, file)
            file.write("\n")
    except IOError as e:
        print(f"Failed to write to log file: {e}")

def test_function_via_proxy(function_name, proxy_url, ip_addresses, expected_response, method='POST'):
    # Prepare the data for the request
    if method == 'GET':
        # For GET request, format IP addresses as query string
        ip_string = ",".join(ip_addresses)
        url = f"{proxy_url}/{function_name}?items={ip_string}"
        data = None
    else:
        # For POST request, send data as JSON body
        data = json.dumps({"ips": ip_addresses})
        url = f"{proxy_url}/{function_name}"

    # Start the timer
    start_time = time.time()

    # Make the HTTP request using curl
    try:
        if method == 'GET':
            response = subprocess.check_output(
                ["curl", "-X", "GET", url],
                universal_newlines=True
            )
        else:
            response = subprocess.check_output(
                [
                    "curl",
                    "-X", method,
                    "-H", "Content-Type: application/json",
                    "-d", data,
                    url
                ],
                universal_newlines=True
            )
    except subprocess.CalledProcessError as e:
        print(f"Error calling {function_name}: {e.output}")
        return

    # Measure the time taken
    elapsed_time = time.time() - start_time

    # Parse the response
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON response for {function_name}")
        return

    # Check correctness based on function name
    if function_name == 'total-ips':
        correct = response_json.get('total_ips') == expected_response.get('total_ips')
    elif function_name == 'total-empty-ips':
        correct = response_json.get('total_empty_ips') == expected_response.get('total_empty_ips')
    elif function_name == 'total-valid-ips/validate_ips':
        correct = response_json.get('total_valid_ips') == expected_response.get('total_valid_ips') and response_json.get('results') == expected_response.get('results')
    elif function_name == 'find-bad-ips':
        correct = response_json.get('results') == expected_response.get('results')
    else:
        correct = response_json == expected_response

    # Prepare the log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "function_name": function_name,
        "ip_addresses": ip_addresses,
        "expected_response": expected_response,
        "actual_response": response_json,
        "correct": correct,
        "time_taken": round(elapsed_time, 2)
    }

    # Print results
    print(f"Function: {function_name}")
    print(f"Expected Response: {expected_response}")
    print(f"Response: {response_json}")
    print(f"Correct: {'Yes' if correct else 'No'}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print()

    # Log the results to file
    log_results_to_file(log_entry)

def main():
    proxy_url = "http://ipchecker-proxy-40125560.qpc.qubcloud.uk"  

    # Generate random IP addresses
    ip_addresses = generate_random_ip_addresses()

    # Expected responses
    expected_total_ips = {"total_ips": len(ip_addresses)}
    expected_total_empty_ips = {"total_empty_ips": 0}  # Since no empty IPs should be generated randomly

    # Validation logic for `total-valid-ips`
    total_valid_ips = 0
    results = []
    for ip in ip_addresses:
        if is_valid_ipv4(ip) or is_valid_ipv6(ip):
            results.append(f"{ip} -> valid")
            total_valid_ips += 1
        else:
            results.append(f"{ip} -> invalid")

    expected_total_valid_ips = {
        "total_valid_ips": total_valid_ips,
        "results": results
    }

    expected_classify = {
        "results": [f"{ip} -> IPv4" if "." in ip else f"{ip} -> IPv6" for ip in ip_addresses]
    }

    expected_find_country = {
        ip: "US" if ip.startswith("100.") else "UK" if ip.startswith("101.") else "China" if ip.startswith("102.") else "Unknown"
        for ip in ip_addresses
    }

    # Validation logic for `badips`
    bad_ips_list = [
        "100.200.300.400",
        "101.201.301.401",
        "102.202.302.402",
        "103.203.303.403"
    ]
    expected_bad_ips = {
        "results": [f"{ip} -> Bad IP" if ip in bad_ips_list else f"{ip} -> Good IP" for ip in ip_addresses]
    }

    # Test the functions
    test_function_via_proxy("total-ips", proxy_url, ip_addresses, expected_total_ips, method='GET')
    test_function_via_proxy("total-empty-ips", proxy_url, ip_addresses, expected_total_empty_ips, method='GET')
    test_function_via_proxy("total-valid-ips/validate_ips", proxy_url, ip_addresses, expected_total_valid_ips, method='GET')
    test_function_via_proxy("classify", proxy_url, ip_addresses, expected_classify)
    test_function_via_proxy("find-country", proxy_url, ip_addresses, expected_find_country)
    test_function_via_proxy("find-bad-ips", proxy_url, ip_addresses, expected_bad_ips, method='GET')
    
if __name__ == "__main__":
    main()
