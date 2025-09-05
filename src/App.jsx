import React, { useState } from 'react';
import { Header } from './components/Header';
import { AuthModal } from './components/AuthModal';
import { Dashboard } from './components/Dashboard';
import { useAuth } from './hooks/useAuth';

function App() {
  const { user, isLoading, error, login, register, logout } = useAuth();
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  const handleAuthSuccess = () => {
    setIsAuthModalOpen(false);
  };

  const handleLogin = async (email, password) => {
    await login(email, password);
    handleAuthSuccess();
  };

  const handleRegister = async (email, password, name) => {
    await register(email, password, name);
    handleAuthSuccess();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading SoilSense...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header
        user={user}
        onAuthClick={() => setIsAuthModalOpen(true)}
        onLogout={logout}
      />

      {user ? (
        <Dashboard />
      ) : (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="max-w-md mx-auto px-4 text-center">
            
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              SoilSense
            </h1>
            
            <p className="text-gray-600 mb-8">
              Analyze your soil fertility and get recommendations for better farming
            </p>
            
            <button
              onClick={() => setIsAuthModalOpen(true)}
              className="bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700"
            >
              Get Started
            </button>
            
            <p className="text-gray-500 mt-4 text-sm">
              Sign in to start analyzing your soil
            </p>
          </div>
        </div>
      )}

      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onLogin={handleLogin}
        onRegister={handleRegister}
        isLoading={isLoading}
        error={error}
      />
    </div>
  );
}

export default App;