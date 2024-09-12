<?php
use PHPUnit\Framework\TestCase;

// Include the functions file
require 'functions.inc.php';

class BadIPsTest extends TestCase
{
    private $bad_ips;

    protected function setUp(): void
    {
        // Initialize the bad IPs array here
        $GLOBALS['bad_ips'] = [
            "100.200.300.400",
            "101.201.301.401",
            "102.202.302.402",
            "103.203.303.403"
        ];
    }

    public function testCheckIpsIdentifiesBadIp()
    {
        $ip_list = ["100.200.300.400"];
        $expected = ["100.200.300.400 -> Bad IP"];
        $results = check_ips($ip_list);
        $this->assertEquals($expected, $results);
    }

    public function testCheckIpsIdentifiesGoodIp()
    {
        $ip_list = ["192.168.0.1"];
        $expected = ["192.168.0.1 -> Good IP"];
        $results = check_ips($ip_list);
        $this->assertEquals($expected, $results);
    }

    public function testCheckIpsWithMultipleIps()
    {
        $ip_list = ["100.200.300.400", "192.168.0.1", "101.201.301.401"];
        $expected = [
            "100.200.300.400 -> Bad IP",
            "192.168.0.1 -> Good IP",
            "101.201.301.401 -> Bad IP"
        ];
        $results = check_ips($ip_list);
        $this->assertEquals($expected, $results);
    }
}




