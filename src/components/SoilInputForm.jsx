import React, { useState } from 'react';
import { Loader2 } from 'lucide-react';

export const SoilInputForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    nitrogen: 25,
    phosphorus: 20,
    potassium: 150,
    ph: 6.5,
    organicMatter: 3,
    moisture: 45,
    temperature: 22,
    location: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'location' ? value : parseFloat(value) || 0
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-2">Enter Soil Data</h2>
        <p className="text-gray-600">Fill in your soil test results below</p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nitrogen (ppm)
            </label>
            <input
              type="number"
              name="nitrogen"
              value={formData.nitrogen}
              onChange={handleInputChange}
              min="0"
              max="100"
              step="0.1"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
              placeholder="Enter nitrogen content"
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Phosphorus (ppm)
            </label>
            <input
              type="number"
              name="phosphorus"
              value={formData.phosphorus}
              onChange={handleInputChange}
              min="0"
              max="100"
              step="0.1"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
              placeholder="Enter phosphorus content"
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Potassium (ppm)
            </label>
            <input
              type="number"
              name="potassium"
              value={formData.potassium}
              onChange={handleInputChange}
              min="0"
              max="500"
              step="1"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
              placeholder="Enter potassium content"
            />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">
            </label>
            <input
              type="number"
              name="ph"
              value={formData.ph}
              onChange={handleInputChange}
              min="0"
              max="14"
              step="0.1"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
              placeholder="Enter pH level"
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Organic Matter (%)
            </label>
            <input
              type="number"
              name="organicMatter"
              value={formData.organicMatter}
              onChange={handleInputChange}
              min="0"
              max="10"
              step="0.1"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
            />
          </div>

            <label className="block text-sm font-medium text-gray-700 mb-1">
              Moisture (%)
            </label>
            <input
              type="number"
              name="moisture"
              value={formData.moisture}
              onChange={handleInputChange}
              min="0"
              max="100"
              step="0.1"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
            />
          </div>

            <label className="block text-sm font-medium text-gray-700 mb-1">
              Temperature (°C)
            </label>
            <input
              type="number"
              name="temperature"
              value={formData.temperature}
              onChange={handleInputChange}
              min="-10"
              max="50"
              step="0.1"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
              placeholder="Enter soil temperature"
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
            </label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleInputChange}
              placeholder="e.g., Farm Field A, North Plot"
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
            />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-green-600 text-white py-3 rounded hover:bg-green-700 disabled:opacity-50 flex items-center justify-center"
          className="w-full bg-green-600 text-white py-3 rounded hover:bg-green-700 disabled:opacity-50 flex items-center justify-center"
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin mr-2" />
              Analyzing...
            </>
          ) : (
            'Analyze Soil'
          )}
        </button>
      </form>
    </div>
  );
};