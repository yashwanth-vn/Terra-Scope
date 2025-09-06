import React from 'react';
import { CheckCircle, AlertCircle, XCircle, Leaf, Droplets } from 'lucide-react';

export const FertilityResults = ({ prediction }) => {
  if (!prediction) return null;

  const getFertilityColor = (level) => {
    switch (level.toLowerCase()) {
      case 'high': return 'text-green-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getFertilityIcon = (level) => {
    switch (level.toLowerCase()) {
      case 'high': return <CheckCircle className="w-6 h-6 text-green-600" />;
      case 'medium': return <AlertCircle className="w-6 h-6 text-yellow-600" />;
      case 'low': return <XCircle className="w-6 h-6 text-red-600" />;
      default: return <AlertCircle className="w-6 h-6 text-gray-600" />;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Analysis Results</h2>
      
      <div className="mb-6">
        <div className="flex items-center mb-2">
          {getFertilityIcon(prediction.fertility_level)}
          <span className={`ml-2 text-lg font-semibold ${getFertilityColor(prediction.fertility_level)}`}>
            {prediction.fertility_level} Fertility
          </span>
        </div>
        <p className="text-2xl font-bold text-gray-900">Score: {prediction.score}/100</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="font-semibold text-gray-900 mb-3">Reasons</h3>
          <ul className="space-y-2">
            {prediction.reasons.map((reason, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-start">
                <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                {reason}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="font-semibold text-gray-900 mb-3">Recommendations</h3>
          
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Fertilizers</h4>
            <div className="flex flex-wrap gap-2">
              {prediction.recommendations.fertilizers.map((fertilizer, index) => (
                <span key={index} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                  {fertilizer}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Suitable Crops</h4>
            <div className="flex flex-wrap gap-2">
              {prediction.recommendations.crops.map((crop, index) => (
                <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                  {crop}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};