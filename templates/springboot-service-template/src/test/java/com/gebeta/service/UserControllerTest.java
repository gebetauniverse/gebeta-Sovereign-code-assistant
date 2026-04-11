package com.gebeta.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.gebeta.service.dto.UserUpdateRequest;
import com.gebeta.service.model.User;
import com.gebeta.service.repository.UserRepository;
import com.gebeta.service.security.JwtUtil;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.http.MediaType;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.time.LocalDateTime;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Tests for User Controller.
 * Follows Gebeta Sovereign Coding Rules for security and quality.
 */
@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
class UserControllerTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("testuser")
            .withPassword("testpass");

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JwtUtil jwtUtil;

    @Autowired
    private ObjectMapper objectMapper;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    private String authToken;
    private Long userId;
    private String userEmail;

    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
        
        // Create test user
        User user = new User();
        userEmail = "user@example.com";
        user.setEmail(userEmail);
        user.setPassword(passwordEncoder.encode("StrongPass123!"));
        user.setFullName("Test User");
        user.setCreatedAt(LocalDateTime.now());
        User saved = userRepository.save(user);
        userId = saved.getId();
        
        authToken = jwtUtil.generateToken(user.getEmail());
    }

    // ========== Get Current User Tests ==========

    @Test
    void getCurrentUser_Success() throws Exception {
        mockMvc.perform(get("/api/v1/users/me")
                .header("Authorization", "Bearer " + authToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value(userEmail))
                .andExpect(jsonPath("$.fullName").value("Test User"))
                .andExpect(jsonPath("$.password").doesNotExist())
                .andExpect(jsonPath("$.hashed_password").doesNotExist());
    }

    @Test
    void getCurrentUser_Unauthorized_Returns401() throws Exception {
        mockMvc.perform(get("/api/v1/users/me"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void getCurrentUser_InvalidToken_Returns401() throws Exception {
        mockMvc.perform(get("/api/v1/users/me")
                .header("Authorization", "Bearer invalid.token.here"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void getCurrentUser_ExpiredToken_Returns401() throws Exception {
        // Generate an expired token (set expiration to past)
        String expiredToken = jwtUtil.generateTokenWithExpiration(userEmail, -1000);
        
        mockMvc.perform(get("/api/v1/users/me")
                .header("Authorization", "Bearer " + expiredToken))
                .andExpect(status().isUnauthorized());
    }

    // ========== Update Current User Tests ==========

    @Test
    void updateCurrentUser_FullUpdate_Success() throws Exception {
        UserUpdateRequest updateRequest = new UserUpdateRequest("updated@example.com", "NewStrongPass123!", "Updated Name");

        mockMvc.perform(put("/api/v1/users/me")
                .header("Authorization", "Bearer " + authToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value("updated@example.com"))
                .andExpect(jsonPath("$.fullName").value("Updated Name"))
                .andExpect(jsonPath("$.password").doesNotExist());
    }

    @Test
    void updateCurrentUser_PartialUpdate_EmailOnly_Success() throws Exception {
        UserUpdateRequest updateRequest = new UserUpdateRequest();
        updateRequest.setEmail("partial@example.com");

        mockMvc.perform(put("/api/v1/users/me")
                .header("Authorization", "Bearer " + authToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value("partial@example.com"))
                .andExpect(jsonPath("$.fullName").value("Test User")); // Unchanged
    }

    @Test
    void updateCurrentUser_PartialUpdate_FullNameOnly_Success() throws Exception {
        UserUpdateRequest updateRequest = new UserUpdateRequest();
        updateRequest.setFullName("Partial Name Only");

        mockMvc.perform(put("/api/v1/users/me")
                .header("Authorization", "Bearer " + authToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value(userEmail)) // Unchanged
                .andExpect(jsonPath("$.fullName").value("Partial Name Only"));
    }

    @Test
    void updateCurrentUser_DuplicateEmail_Returns400() throws Exception {
        // Create another user
        User other = new User();
        other.setEmail("existing@example.com");
        other.setPassword(passwordEncoder.encode("StrongPass123!"));
        other.setCreatedAt(LocalDateTime.now());
        userRepository.save(other);

        UserUpdateRequest updateRequest = new UserUpdateRequest();
        updateRequest.setEmail("existing@example.com");

        mockMvc.perform(put("/api/v1/users/me")
                .header("Authorization", "Bearer " + authToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void updateCurrentUser_InvalidEmail_Returns400() throws Exception {
        UserUpdateRequest updateRequest = new UserUpdateRequest();
        updateRequest.setEmail("not-an-email");

        mockMvc.perform(put("/api/v1/users/me")
                .header("Authorization", "Bearer " + authToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void updateCurrentUser_WeakPassword_Returns400() throws Exception {
        UserUpdateRequest updateRequest = new UserUpdateRequest();
        updateRequest.setPassword("123");

        mockMvc.perform(put("/api/v1/users/me")
                .header("Authorization", "Bearer " + authToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void updateCurrentUser_Unauthorized_Returns401() throws Exception {
        UserUpdateRequest updateRequest = new UserUpdateRequest();
        updateRequest.setEmail("hacker@example.com");

        mockMvc.perform(put("/api/v1/users/me")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest)))
                .andExpect(status().isUnauthorized());
    }
}
