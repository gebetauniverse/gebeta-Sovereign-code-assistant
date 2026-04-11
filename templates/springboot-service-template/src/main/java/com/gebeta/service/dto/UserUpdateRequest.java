package com.gebeta.service.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

/**
 * DTO for updating user information.
 * Separate from UserResponse to avoid exposing sensitive data.
 */
public class UserUpdateRequest {
    
    @Email(message = "Invalid email format")
    private String email;
    
    @Size(min = 2, max = 100, message = "Full name must be between 2 and 100 characters")
    private String fullName;
    
    @Pattern(regexp = "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$",
             message = "Password must contain at least 8 characters, one uppercase, one lowercase, one number, and one special character")
    private String password;
    
    // Constructors
    public UserUpdateRequest() {}
    
    public UserUpdateRequest(String email, String fullName, String password) {
        this.email = email;
        this.fullName = fullName;
        this.password = password;
    }
    
    // Getters and Setters
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
}