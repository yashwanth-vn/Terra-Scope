import React from 'react';
import { CheckCircle, AlertCircle, XCircle, Beaker, Leaf, TrendingUp } from 'lucide-react';

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
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <div className="flex items-center space-x-3 mb-6">
        <div className="bg-blue-100 p-2 rounded-lg">
          <TrendingUp className="w-6 h-6 text-blue-600" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900">Fertility Analysis Results</h2>
      </div>
      
      {/* Fertility Level */}
      <div className={`border rounded-lg p-6 mb-6 ${getFertilityColor()}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            {getFertilityIcon()}
            <div>
              <h3 className="text-2xl font-bold">{prediction.fertilityLevel} Fertility</h3>
              <p className="text-lg opacity-80">Overall soil health assessment</p>
            </div>
          </div>
          <div className="text-right">
            <div className={`text-3xl font-bold ${getScoreColor()}`}>
              {prediction.score}
            </div>
            <div className="text-sm opacity-60">out of 100</div>
          </div>
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <div className="w-2 h-2 bg-green-600 rounded-full mr-2"></div>
          Analysis Summary
        </h3>
        <div className="bg-gray-50 rounded-lg p-4">
          <ul className="space-y-3">
            {prediction.reasons.map((reason, index) => (
              <li key={index} className="flex items-start space-x-3">
                <div className="w-1.5 h-1.5 bg-green-600 rounded-full mt-2 flex-shrink-0"></div>
                <span className="text-gray-700 leading-relaxed">{reason}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Recommendations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Fertilizers */}
        <div className="bg-blue-50 rounded-lg p-5 border border-blue-100">
          <div className="flex items-center space-x-2 mb-4">
            <Beaker className="w-5 h-5 text-blue-600" />
            <h4 className="font-semibold text-blue-900">Recommended Fertilizers</h4>
          </div>
          <div className="space-y-2">
            {prediction.recommendations.fertilizers.length > 0 ? (
              prediction.recommendations.fertilizers.map((fertilizer, index) => (
                <div key={index} className="text-sm text-blue-800 bg-white px-3 py-2 rounded border border-blue-200 hover:bg-blue-50 transition-colors">
                  {fertilizer}
                </div>
              ))
            ) : (
              <p className="text-sm text-blue-700 italic">No specific fertilizers needed</p>
            )}
          </div>
        </div>

        {/* Crops */}
        <div className="bg-green-50 rounded-lg p-5 border border-green-100">
          <div className="flex items-center space-x-2 mb-4">
            <Leaf className="w-5 h-5 text-green-600" />
            <h4 className="font-semibold text-green-900">Suitable Crops</h4>
          </div>
          <div className="space-y-2">
            {prediction.recommendations.crops.map((crop, index) => (
              <div key={index} className="text-sm text-green-800 bg-white px-3 py-2 rounded border border-green-200 hover:bg-green-50 transition-colors">
                {crop}
              </div>
            ))}
          </div>
        </div>

        {/* Improvements */}
        <div className="bg-orange-50 rounded-lg p-5 border border-orange-100">
          <div className="flex items-center space-x-2 mb-4">
            <TrendingUp className="w-5 h-5 text-orange-600" />
            <h4 className="font-semibold text-orange-900">Improvement Tips</h4>
          </div>
          <div className="space-y-2">
            {prediction.recommendations.improvements.length > 0 ? (
              prediction.recommendations.improvements.map((improvement, index) => (
                <div key={index} className="text-sm text-orange-800 bg-white px-3 py-2 rounded border border-orange-200 hover:bg-orange-50 transition-colors">
                  {improvement}
                </div>
              ))
            ) : (
              <p className="text-sm text-orange-700 italic">Soil is in good condition</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};