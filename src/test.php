<?php
use PHPUnit\Framework\TestCase;

require 'functions.inc.php';

class TotalIPsTest extends TestCase
{
    public function testGetTotalIPs()
    {
        // Test case with multiple IPs
        $ip_list = "192.168.0.1, 192.168.0.2, 192.168.0.3";
        $expected = 3;
        $result = getTotalIPs($ip_list);
        $this->assertEquals($expected, $result);

        // Test case with a single IP
        $ip_list = "192.168.0.1";
        $expected = 1;
        $result = getTotalIPs($ip_list);
        $this->assertEquals($expected, $result);

        // Test case with empty input
        $ip_list = "";
        $expected = 1; // Since there's still one empty string in the list
        $result = getTotalIPs($ip_list);
        $this->assertEquals($expected, $result);
    }
}
