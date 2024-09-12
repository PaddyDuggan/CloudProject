<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json");
require('functions.inc.php');

$output = array(
    "error" => false,
    "items" => "",
    "results" => []
);

if (isset($_REQUEST['items'])) {
    $items = $_REQUEST['items'];
    $ip_list = preg_split('/\s*,\s*/', $items); // Split input IPs into an array, trimming whitespace
    $results = check_ips($ip_list); // Call the function to check IPs

    $output['items'] = $items;
    $output['results'] = $results;
} else {
    $output['error'] = true;
    $output['message'] = "No IP addresses provided.";
}

echo json_encode($output);
exit();

