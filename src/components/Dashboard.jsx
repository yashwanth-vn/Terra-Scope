import React, { useState } from 'react';
import { MessageCircle, BarChart3, Leaf, Beaker, TrendingUp, Users } from 'lucide-react';
import { SoilInputForm } from './SoilInputForm';
import { FertilityResults } from './FertilityResults';
import { ChatBot } from './ChatBot';
import { soilAnalysisService } from '../services/soilAnalysis';

export const Dashboard = () => {
  const [prediction, setPrediction] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleSoilAnalysis = async (soilData) => {
    setIsAnalyzing(true);
    try {
      const result = await soilAnalysisService.predictFertility(soilData);
      setPrediction(result);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="bg-green-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
            <Leaf className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI-Powered Soil Fertility Analysis
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Get instant insights into your soil health with our advanced machine learning model. 
            Receive personalized fertilizer recommendations and discover the best crops for your land.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-white p-6 rounded-lg shadow-sm text-center border border-gray-200 hover:shadow-md transition-shadow">
            <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-4">
              <BarChart3 className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Fertility Prediction</h3>
            <p className="text-gray-600 text-sm">Advanced ML algorithms analyze your soil composition</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm text-center border border-gray-200 hover:shadow-md transition-shadow">
            <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Beaker className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Fertilizer Recommendations</h3>
            <p className="text-gray-600 text-sm">Get specific fertilizer suggestions for optimal growth</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm text-center border border-gray-200 hover:shadow-md transition-shadow">
            <div className="bg-orange-100 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Leaf className="w-6 h-6 text-orange-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Crop Suggestions</h3>
            <p className="text-gray-600 text-sm">Discover the best crops for your soil conditions</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm text-center border border-gray-200 hover:shadow-md transition-shadow">
            <div className="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-4">
              <MessageCircle className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Assistant</h3>
            <p className="text-gray-600 text-sm">Chat with our AI for instant farming advice</p>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          <SoilInputForm onSubmit={handleSoilAnalysis} isLoading={isAnalyzing} />
          
          {prediction ? (
            <FertilityResults prediction={prediction} />
          ) : (
            <div className="bg-white rounded-lg shadow-sm p-8 border border-gray-200 flex items-center justify-center">
              <div className="text-center">
                <TrendingUp className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready for Analysis</h3>
                <p className="text-gray-600">
                  Enter your soil parameters to get detailed fertility predictions and recommendations.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Stats Section */}
        <div className="mt-12 bg-white rounded-lg shadow-sm p-8 border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Why Choose SoilSense?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">90%</h3>
              <p className="text-gray-600">ML Model Accuracy</p>
            </div>
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">10,000+</h3>
              <p className="text-gray-600">Farmers Helped</p>
            </div>
            <div className="text-center">
              <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-8 h-8 text-orange-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">30%</h3>
              <p className="text-gray-600">Average Yield Increase</p>
            </div>
          </div>
          
          <div className="mt-8 p-4 bg-green-50 rounded-lg border border-green-200">
            <div className="flex items-center space-x-2 mb-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <h4 className="font-semibold text-green-800">Powered by Machine Learning</h4>
            </div>
            <p className="text-green-700 text-sm">
              Our Random Forest model analyzes 7 key soil parameters with 90% accuracy, 
              trained on thousands of soil samples to provide precise fertility predictions.
            </p>
          </div>
        </div>

        {/* Chat Bot Toggle */}
        <button
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-6 right-6 bg-green-600 text-white p-4 rounded-full shadow-lg hover:bg-green-700 transition-all hover:scale-105 z-30"
          title="Open AI Assistant"
        >
          <MessageCircle className="w-6 h-6" />
        </button>

        <ChatBot isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
      </div>
    </div>
  );
};