import React, { useState } from 'react';
import { MessageCircle } from 'lucide-react';
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
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Soil Fertility Analysis
          </h1>
          <p className="text-gray-600">
            Enter your soil test results to get fertility predictions and recommendations
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <SoilInputForm onSubmit={handleSoilAnalysis} isLoading={isAnalyzing} />
          
          {prediction ? (
            <FertilityResults prediction={prediction} />
          ) : (
            <div className="bg-white rounded-lg shadow p-8 flex items-center justify-center">
              <div className="text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Analyze</h3>
                <p className="text-gray-600">
                  Fill out the form to get your soil analysis results
                </p>
              </div>
            </div>
          )}
        </div>

        <button
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-6 right-6 bg-green-600 text-white p-4 rounded-full shadow-lg hover:bg-green-700 z-30"
        >
          <MessageCircle className="w-6 h-6" />
        </button>

        <ChatBot isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
      </div>
    </div>
  );
};