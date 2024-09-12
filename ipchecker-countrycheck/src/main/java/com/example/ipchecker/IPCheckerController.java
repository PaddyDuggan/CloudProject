package com.example.ipchecker;

import org.springframework.web.bind.annotation.*;

import java.util.LinkedHashMap;
import java.util.Map;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api")
public class IPCheckerController {

    @PostMapping("/findCountry")
    public Map<String, String> findCountry(@RequestBody Map<String, String[]> ipRequest) {
        String[] ips = ipRequest.get("ips");

        // Use LinkedHashMap to maintain insertion order
        Map<String, String> results = new LinkedHashMap<>();

        for (String ip : ips) {
            String country = identifyCountry(ip);
            results.put(ip, country);
        }

        return results;
    }

    private String identifyCountry(String ip) {
        if (ip.startsWith("100.")) {
            return "US";
        } else if (ip.startsWith("101.")) {
            return "UK";
        } else if (ip.startsWith("102.")) {
            return "China";
        } else {
            return "Unknown";
        }
    }
}

