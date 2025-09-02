import { useState, useEffect } from 'react';
import { authService } from '../services/auth';

export const useAuth = () => {
  const [authState, setAuthState] = useState({
    user: null,
    isLoading: true,
    error: null
  });

  useEffect(() => {
    const user = authService.getCurrentUser();
    setAuthState({
      user,
      isLoading: false,
      error: null
    });
  }, []);

  const login = async (email, password) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const user = await authService.login(email, password);
      setAuthState({ user, isLoading: false, error: null });
    } catch (error) {
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: error.message || 'Login failed'
      }));
    }
  };

  const register = async (email, password, name) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const user = await authService.register(email, password, name);
      setAuthState({ user, isLoading: false, error: null });
    } catch (error) {
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: error.message || 'Registration failed'
      }));
    }
  };

  const logout = async () => {
    await authService.logout();
    setAuthState({ user: null, isLoading: false, error: null });
  };

  return {
    ...authState,
    login,
    register,
    logout
  };
};