import React from 'react';
import { LogOut, User } from 'lucide-react';

export const Header = ({ user, onAuthClick, onLogout }) => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div>
            <h1 className="text-2xl font-bold text-green-600">SoilSense</h1>
          </div>

          <div className="flex items-center space-x-3">
            {user ? (
              <>
                <div className="flex items-center space-x-1">
                  <User className="w-5 h-5 text-gray-600" />
                  <span className="text-gray-700">{user.name}</span>
                </div>
                <button
                  onClick={onLogout}
                  className="flex items-center space-x-1 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <button
                onClick={onAuthClick}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};