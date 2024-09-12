package com.example.ipchecker;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import org.springframework.http.MediaType;

@WebMvcTest(IPCheckerController.class)
public class IPCheckerControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testFindCountry() throws Exception {
        String jsonRequest = "{\"ips\": [\"100.1.1.1\", \"101.1.1.1\", \"102.1.1.1\", \"103.1.1.1\"]}";

        mockMvc.perform(post("/api/findCountry")
                .contentType(MediaType.APPLICATION_JSON)
                .content(jsonRequest))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.['100.1.1.1']").value("US"))
                .andExpect(jsonPath("$.['101.1.1.1']").value("UK"))
                .andExpect(jsonPath("$.['102.1.1.1']").value("China"))
                .andExpect(jsonPath("$.['103.1.1.1']").value("Unknown"));
    }
}

