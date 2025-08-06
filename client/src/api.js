import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

export const predictSeverity = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/predict`, formData);
    return response.data;
  } catch (error) {
    console.error('Prediction API error:', error);
    throw error;
  }
};
