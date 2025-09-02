// Soil analysis service for Flask backend
class SoilAnalysisService {
  constructor() {
    this.baseURL = 'http://localhost:5000/api/soil';
  }

  getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };
  }

  async predictFertility(soilData) {
    try {
      const response = await fetch(`${this.baseURL}/analyze`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          nitrogen: soilData.nitrogen,
          phosphorus: soilData.phosphorus,
          potassium: soilData.potassium,
          ph: soilData.ph,
          organic_matter: soilData.organicMatter,
          moisture: soilData.moisture,
          temperature: soilData.temperature,
          location: soilData.location || ''
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Analysis failed');
      }

      const data = await response.json();
      return {
        fertilityLevel: data.fertility_level,
        score: data.score,
        reasons: data.reasons,
        recommendations: data.recommendations
      };
    } catch (error) {
      throw new Error(error.message || 'Network error');
    }
  }

  async getAnalysisHistory() {
    try {
      const response = await fetch(`${this.baseURL}/history`, {
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to fetch history');
      }

      const data = await response.json();
      return data.history;
    } catch (error) {
      throw new Error(error.message || 'Network error');
    }
  }

  async getStatistics() {
    try {
      const response = await fetch(`${this.baseURL}/statistics`, {
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to fetch statistics');
      }

      return await response.json();
    } catch (error) {
      throw new Error(error.message || 'Network error');
    }
  }
}

export const soilAnalysisService = new SoilAnalysisService();