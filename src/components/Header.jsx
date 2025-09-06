import React from 'react';
import { Leaf, LogOut, User } from 'lucide-react';

export const Header = ({ user, onAuthClick, onLogout }) => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <div className="bg-green-600 w-8 h-8 rounded flex items-center justify-center mr-3">
              <Leaf className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold text-gray-900">SoilSense</h1>
          </div>

          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <div className="flex items-center space-x-2">
                  <User className="w-4 h-4 text-gray-600" />
                  <span className="text-sm text-gray-700">{user.name}</span>
                </div>
                <button
                  onClick={onLogout}
                  className="flex items-center space-x-1 text-gray-600 hover:text-gray-900"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="text-sm">Logout</span>
                </button>
              </>
            ) : (
              <button
                onClick={onAuthClick}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                Login
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};