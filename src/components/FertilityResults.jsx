import React from 'react';
import { CheckCircle, AlertCircle, XCircle } from 'lucide-react';

export const FertilityResults = ({ prediction }) => {
  const getFertilityIcon = () => {
    switch (prediction.fertilityLevel) {
      case 'High':
        return <CheckCircle className="w-8 h-8 text-green-600" />;
      case 'Medium':
        return <AlertCircle className="w-8 h-8 text-yellow-600" />;
      case 'Low':
        return <XCircle className="w-8 h-8 text-red-600" />;
      default:
        return <AlertCircle className="w-8 h-8 text-gray-600" />;
    }
  };

  const getFertilityColor = () => {
    switch (prediction.fertilityLevel) {
      case 'High':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'Medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'Low':
        return 'text-red-600 bg-red-50 border-red-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getScoreColor = () => {
    if (prediction.score > 80) return 'text-green-600';
    if (prediction.score > 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className={`border rounded p-4 mb-6 ${getFertilityColor()}`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            {getFertilityIcon()}
            <div>
              <h3 className="text-xl font-bold">{prediction.fertilityLevel} Fertility</h3>
              <p className="text-sm opacity-80">Soil health status</p>
            </div>
          </div>
          <div className="text-right">
            <div className={`text-2xl font-bold ${getScoreColor()}`}>
              {prediction.score}
            </div>
            <div className="text-sm opacity-60">out of 100</div>
          </div>
        </div>
                <div className="w-1 h-1 bg-gray-600 rounded-full mt-2 flex-shrink-0"></div>
                <span className="text-sm text-gray-700">{reason}</span>
          <h4 className="font-semibold mb-2">Why this rating:</h4>
            ))}
          </ul>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 rounded p-4 border border-blue-200">
          <div className="space-y-1">
            <h4 className="font-semibold text-blue-900">Fertilizers</h4>
              prediction.recommendations.fertilizers.map((fertilizer, index) => (
                <div key={index} className="text-sm text-blue-800 bg-white px-2 py-1 rounded">
                  {fertilizer}
                </div>
              ))
            ) : (
              <p className="text-sm text-blue-700">None needed</p>
            )}
          </div>
        <div className="bg-green-50 rounded p-4 border border-green-200">
          <div className="mb-3">
            <h4 className="font-semibold text-green-900">Suitable Crops</h4>
          </div>
          <div className="space-y-1">
            {prediction.recommendations.crops.map((crop, index) => (
              <div key={index} className="text-sm text-green-800 bg-white px-2 py-1 rounded">
                {crop}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-orange-50 rounded p-4 border border-orange-200">
          <div className="mb-3">
            <h4 className="font-semibold text-orange-900">Improvements</h4>
            {prediction.recommendations.improvements.length > 0 ? (
              prediction.recommendations.improvements.map((improvement, index) => (
                <div key={index} className="text-sm text-orange-800 bg-white px-2 py-1 rounded">
                  {improvement}
                </div>
              ))
            ) : (
              <p className="text-sm text-orange-700">None needed</p>
            )}
          </div>
          <div className="space-y-1">
      </div>
    </div>
  );
};