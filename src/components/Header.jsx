import React, { useState } from 'react';
import { BarChart3, Leaf, MessageCircle } from 'lucide-react';
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
        <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50 flex items-center justify-center">
          <div className="max-w-5xl mx-auto px-4 text-center">
            <div className="bg-green-600 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-8 shadow-lg">
              <Leaf className="w-10 h-10 text-white" />
            </div>
            
            <h1 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
              Welcome to SoilSense
            </h1>
            
            <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              Transform your farming with AI-powered soil analysis. Get instant fertility predictions, 
              personalized fertilizer recommendations, and expert crop suggestions to maximize your harvest.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
              <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                <div className="bg-blue-100 w-14 h-14 rounded-lg flex items-center justify-center mx-auto mb-6">
                  <BarChart3 className="w-7 h-7 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-gray-900">Smart Analysis</h3>
                <p className="text-gray-600 leading-relaxed">
                  Advanced machine learning algorithms analyze your soil composition and provide detailed insights
                </p>
              </div>
              
              <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                <div className="bg-green-100 w-14 h-14 rounded-lg flex items-center justify-center mx-auto mb-6">
                  <Leaf className="w-7 h-7 text-green-600" />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-gray-900">Crop Recommendations</h3>
                <p className="text-gray-600 leading-relaxed">
                  Get personalized suggestions for optimal crop selection based on your soil conditions
                </p>
              </div>
              
              <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                <div className="bg-orange-100 w-14 h-14 rounded-lg flex items-center justify-center mx-auto mb-6">
                  <MessageCircle className="w-7 h-7 text-orange-600" />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-gray-900">AI Assistant</h3>
                <p className="text-gray-600 leading-relaxed">
                  Chat with our AI assistant for instant farming advice and expert guidance
                </p>
              </div>
            </div>
            
            <button
              onClick={() => setIsAuthModalOpen(true)}
              className="bg-green-600 text-white px-10 py-4 rounded-lg hover:bg-green-700 transition-all font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              Get Started Today
            </button>
            
            <p className="text-gray-500 mt-6">
              Join thousands of farmers improving their soil health with AI
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