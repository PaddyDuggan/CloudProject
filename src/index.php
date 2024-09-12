<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json");
require('functions.inc.php');

$output = array(
	"error" => false,
    "items" => "",
	"total_ips" => 0,
    "message" => ""
);

if (!isset($_REQUEST['items']) || empty(trim($_REQUEST['items']))) {
    $output['error'] = true;
    $output['message'] = 'No IP addresses provided';
} else {
    $items = $_REQUEST['items'];
    $ip_list = explode(",", $items);
    
    // Validate IP addresses (optional)
    foreach ($ip_list as $ip) {
        if (empty(trim($ip))) {
            $output['error'] = true;
            $output['message'] = 'One or more IP addresses are empty';
            echo json_encode($output);
            exit();
        }
    }

    $total_ips = getTotalIPs($items);
    $output['items'] = $items;
    $output['total_ips'] = $total_ips;
}

echo json_encode($output);
exit();

