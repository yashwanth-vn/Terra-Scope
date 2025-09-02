// Authentication service for Flask backend
class AuthService {
  constructor() {
    this.baseURL = 'http://localhost:5000/api/auth';
    this.token = localStorage.getItem('access_token');
  }

  async login(email, password) {
    try {
      const response = await fetch(`${this.baseURL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Login failed');
      }

      const data = await response.json();
      this.token = data.access_token;
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      return data.user;
    } catch (error) {
      throw new Error(error.message || 'Network error');
    }
  }

  async register(email, password, name) {
    try {
      const response = await fetch(`${this.baseURL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Registration failed');
      }

      const data = await response.json();
      this.token = data.access_token;
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      return data.user;
    } catch (error) {
      throw new Error(error.message || 'Network error');
    }
  }

  async logout() {
    try {
      if (this.token) {
        await fetch(`${this.baseURL}/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.token}`,
          },
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    }
    
    this.token = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  }

  getCurrentUser() {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  }

  getToken() {
    return this.token || localStorage.getItem('access_token');
  }
}

export const authService = new AuthService();