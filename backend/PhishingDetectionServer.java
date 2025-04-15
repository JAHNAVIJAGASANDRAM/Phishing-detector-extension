package com.yourcompany;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashSet;
import java.util.Set;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@SpringBootApplication
@RestController
@RequestMapping("/api")
public class PhishingDetectionServer {

    private static final Logger LOGGER = LoggerFactory.getLogger(PhishingDetectionServer.class);
    private static final Set<String> phishingDomains = new HashSet<>();

    static {
        phishingDomains.add("phishing-site.com");
        phishingDomains.add("malicious-link.com");
    }

    public static void main(String[] args) {
        SpringApplication.run(PhishingDetectionServer.class, args);
    }

    @GetMapping("/check")
    public PhishingResponse checkUrl(@RequestParam String url) {
        String domain = extractDomain(url);
        boolean isPhishing = domain != null && phishingDomains.contains(domain);

        LOGGER.info("Checked URL: {} | Domain: {} | Phishing: {}", url, domain, isPhishing);

        return new PhishingResponse(url, isPhishing);
    }

    private String extractDomain(String url) {
        try {
            @SuppressWarnings("deprecation")
            URL parsedUrl = new URL(url);
            String host = parsedUrl.getHost();
            if (host.startsWith("www.")) {
                host = host.substring(4);
            }
            return host;
        } catch (MalformedURLException e) {
            LOGGER.warn("Invalid URL format: {}", url);
            return null;
        }
    }

    private static class PhishingResponse {
        private String url;
        private boolean phishing;

        public PhishingResponse(String url, boolean phishing) {
            this.url = url;
            this.phishing = phishing;
        }

        public String getUrl() {
            return url;
        }

        public boolean isPhishing() {
            return phishing;
        }
    }
    
}
