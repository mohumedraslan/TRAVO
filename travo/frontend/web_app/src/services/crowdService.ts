import api from './api';

export interface CrowdPredictionRequest {
  locationId: string;
  day: number;
  month: number;
  year: number;
  time: string; // Format: HH:MM
}

export interface CrowdPrediction {
  locationId: string;
  locationName: string;
  date: string;
  time: string;
  crowdLevel: 'LOW' | 'MODERATE' | 'HIGH' | 'VERY_HIGH';
  confidence: number;
  waitTime: number; // in minutes
}

export interface HeatmapDataPoint {
  latitude: number;
  longitude: number;
  intensity: number; // 0-1 value representing crowd density
  locationId: string;
  locationName: string;
}

export const predictCrowd = async (request: CrowdPredictionRequest): Promise<CrowdPrediction> => {
  try {
    const response = await api.post('/crowd/predict', request);
    return response.data;
  } catch (error) {
    console.error('Error predicting crowd:', error);
    throw error;
  }
};

export const getCrowdHeatmap = async (date: string, time: string): Promise<HeatmapDataPoint[]> => {
  try {
    const response = await api.get('/crowd/heatmap', {
      params: { date, time }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching crowd heatmap:', error);
    throw error;
  }
};