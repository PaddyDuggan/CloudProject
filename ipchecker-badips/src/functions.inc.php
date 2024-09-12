<?php
// List of bad IPs
$bad_ips = [
    "100.200.300.400",
    "101.201.301.401",
    "102.202.302.402",
    "103.203.303.403"
];

// Function to check IPs against the bad IPs list
function check_ips($ip_list) {
    global $bad_ips; // Use the global bad IPs array
    $results = [];

    foreach ($ip_list as $ip) {
        $trimmed_ip = trim($ip);  // Trim any whitespace or newline characters
        if (in_array($trimmed_ip, $bad_ips)) {
            $results[] = "$trimmed_ip -> Bad IP";
        } else {
            $results[] = "$trimmed_ip -> Good IP";
        }
    }

    return $results;
}
