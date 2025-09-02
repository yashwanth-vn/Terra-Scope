import React, { useState } from 'react';
import { Loader2, MapPin, Thermometer, Droplets, Beaker } from 'lucide-react';

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
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <div className="flex items-center space-x-3 mb-6">
        <div className="bg-green-100 p-2 rounded-lg">
          <Beaker className="w-6 h-6 text-green-600" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900">Soil Analysis Input</h2>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
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
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              placeholder="Enter nitrogen content"
            />
            <p className="text-xs text-gray-500 mt-1">Essential for plant growth and leaf development</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
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
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              placeholder="Enter phosphorus content"
            />
            <p className="text-xs text-gray-500 mt-1">Important for root development and flowering</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
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
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              placeholder="Enter potassium content"
            />
            <p className="text-xs text-gray-500 mt-1">Helps with disease resistance and water regulation</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              pH Level
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
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              placeholder="Enter pH level"
            />
            <p className="text-xs text-gray-500 mt-1">Optimal range: 6.0 - 7.5 for most crops</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
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
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              placeholder="Enter organic matter percentage"
            />
            <p className="text-xs text-gray-500 mt-1">Improves soil structure and water retention</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Droplets className="w-4 h-4 inline mr-1" />
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
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              placeholder="Enter moisture percentage"
            />
            <p className="text-xs text-gray-500 mt-1">Current soil moisture content</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Thermometer className="w-4 h-4 inline mr-1" />
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
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              placeholder="Enter soil temperature"
            />
            <p className="text-xs text-gray-500 mt-1">Affects nutrient availability and microbial activity</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <MapPin className="w-4 h-4 inline mr-1" />
              Location (Optional)
            </label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleInputChange}
              placeholder="e.g., Farm Field A, North Plot"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
            />
            <p className="text-xs text-gray-500 mt-1">Help identify and track different field areas</p>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-green-600 text-white py-4 rounded-lg hover:bg-green-700 transition-colors font-medium flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin mr-2" />
              Analyzing Soil...
            </>
          ) : (
            'Analyze Soil Fertility'
          )}
        </button>
      </form>
    </div>
  );
};