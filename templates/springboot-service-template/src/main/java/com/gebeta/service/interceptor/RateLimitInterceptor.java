package com.gebeta.service.interceptor;

import com.gebeta.service.config.RateLimitConfig;
import io.github.bucket4j.Bucket;
import io.github.bucket4j.ConsumptionProbe;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component
public class RateLimitInterceptor implements HandlerInterceptor {

    private static final Logger logger = LoggerFactory.getLogger(RateLimitInterceptor.class);

    private final RateLimitConfig rateLimitConfig;

    public RateLimitInterceptor(RateLimitConfig rateLimitConfig) {
        this.rateLimitConfig = rateLimitConfig;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String requestUri = request.getRequestURI();
        String clientIp = getClientIp(request);

        // Apply rate limiting to login endpoint
        if (requestUri.endsWith("/auth/login")) {
            Bucket bucket = rateLimitConfig.getLoginBucket(clientIp);
            ConsumptionProbe probe = bucket.tryConsumeAndReturnRemaining(1);

            if (!probe.isConsumed()) {
                long waitForRefill = probe.getRoundedSecondsToWait();
                response.setContentType("application/json");
                response.setStatus(429);
                response.setHeader("Retry-After", String.valueOf(waitForRefill));
                response.getWriter().write(String.format(
                        "{\"error_code\":\"RATE_LIMITED\",\"message\":\"Too many login attempts. Please try again in %d seconds\",\"status\":429}",
                        waitForRefill
                ));
                logger.warn("Rate limit exceeded for login from IP: {}", clientIp);
                return false;
            }
        }

        // Apply rate limiting to register endpoint
        if (requestUri.endsWith("/auth/register")) {
            Bucket bucket = rateLimitConfig.getRegisterBucket(clientIp);
            ConsumptionProbe probe = bucket.tryConsumeAndReturnRemaining(1);

            if (!probe.isConsumed()) {
                long waitForRefill = probe.getRoundedSecondsToWait();
                response.setContentType("application/json");
                response.setStatus(429);
                response.setHeader("Retry-After", String.valueOf(waitForRefill));
                response.getWriter().write(String.format(
                        "{\"error_code\":\"RATE_LIMITED\",\"message\":\"Too many registration attempts. Please try again in %d seconds\",\"status\":429}",
                        waitForRefill
                ));
                logger.warn("Rate limit exceeded for registration from IP: {}", clientIp);
                return false;
            }
        }

        return true;
    }

    private String getClientIp(HttpServletRequest request) {
        String xForwardedFor = request.getHeader("X-Forwarded-For");
        if (xForwardedFor != null && !xForwardedFor.isEmpty()) {
            return xForwardedFor.split(",")[0];
        }
        String xRealIp = request.getHeader("X-Real-IP");
        if (xRealIp != null && !xRealIp.isEmpty()) {
            return xRealIp;
        }
        return request.getRemoteAddr();
    }
}