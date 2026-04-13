import React, { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';
import api from '../services/api';

interface User {
  id: number;
  email: string;
  full_name: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [tokenExpiresAt, setTokenExpiresAt] = useState<number | null>(null);

  const refreshToken = useCallback(async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) throw new Error('No token to refresh');

      const response = await api.post('/auth/refresh', { token });
      const newToken = response.data.access_token;
      const expiresAtTime = Date.now() + 30 * 60 * 1000;

      localStorage.setItem('access_token', newToken);
      localStorage.setItem('token_expires_at', expiresAtTime.toString());
      setTokenExpiresAt(expiresAtTime);
      setIsAuthenticated(true);
      setError(null);
    } catch (err) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_expires_at');
      setIsAuthenticated(false);
      setUser(null);
      setTokenExpiresAt(null);
      setError('Session expired. Please login again.');
    }
  }, []);

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('access_token');
      const expiresAt = localStorage.getItem('token_expires_at');

      if (token && expiresAt) {
        const expiresAtNum = parseInt(expiresAt, 10);
        if (expiresAtNum > Date.now()) {
          setTokenExpiresAt(expiresAtNum);
          setIsAuthenticated(true);
          try {
            const response = await api.get('/users/me');
            setUser(response.data);
          } catch {
            localStorage.removeItem('access_token');
            localStorage.removeItem('token_expires_at');
            setIsAuthenticated(false);
          }
        } else {
          await refreshToken();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, [refreshToken]);

  useEffect(() => {
    if (!tokenExpiresAt) return;
    const interval = setInterval(() => {
      const timeUntilExpiry = tokenExpiresAt - Date.now();
      if (timeUntilExpiry <= 0) {
        refreshToken();
      } else if (timeUntilExpiry < 5 * 60 * 1000) {
        refreshToken();
      }
    }, 60000);
    return () => clearInterval(interval);
  }, [tokenExpiresAt, refreshToken]);

  const login = useCallback(async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/auth/login', { username: email, password });
      const { access_token } = response.data;
      const expiresAtTime = Date.now() + 30 * 60 * 1000;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('token_expires_at', expiresAtTime.toString());
      setTokenExpiresAt(expiresAtTime);
      setIsAuthenticated(true);

      const userResponse = await api.get('/users/me');
      setUser(userResponse.data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.response?.data?.detail || 'Login failed. Please check your credentials.';
      setError(errorMessage);
      setIsAuthenticated(false);
      setUser(null);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_expires_at');
    setIsAuthenticated(false);
    setUser(null);
    setTokenExpiresAt(null);
    setError(null);
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, loading, error, login, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};