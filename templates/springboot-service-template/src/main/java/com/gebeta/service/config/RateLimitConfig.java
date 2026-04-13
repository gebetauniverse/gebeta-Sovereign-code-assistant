package com.gebeta.service.config;

import io.github.bucket4j.Bandwidth;
import io.github.bucket4j.Bucket;
import io.github.bucket4j.Refill;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class RateLimitConfig {

    private final Map<String, Bucket> loginBuckets = new ConcurrentHashMap<>();
    private final Map<String, Bucket> registerBuckets = new ConcurrentHashMap<>();

    public Bucket getLoginBucket(String clientIp) {
        return loginBuckets.computeIfAbsent(clientIp, ip -> {
            Bandwidth limit = Bandwidth.classic(10, Refill.greedy(10, Duration.ofMinutes(1)));
            return Bucket.builder().addLimit(limit).build();
        });
    }

    public Bucket getRegisterBucket(String clientIp) {
        return registerBuckets.computeIfAbsent(clientIp, ip -> {
            Bandwidth limit = Bandwidth.classic(5, Refill.greedy(5, Duration.ofMinutes(5)));
            return Bucket.builder().addLimit(limit).build();
        });
    }
}