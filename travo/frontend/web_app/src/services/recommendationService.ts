import api from './api';

export interface RecommendationFilter {
  categories?: string[];
  budgetLevel?: string;
  season?: string;
  interests?: string[];
  city?: string;
}

export interface Recommendation {
  id: string;
  name: string;
  description: string;
  location: {
    city: string;
    country: string;
    coordinates: {
      latitude: number;
      longitude: number;
    };
  };
  rating: number;
  imageUrl?: string;
  category: string;
}

export const getRecommendations = async (filters: RecommendationFilter = {}) => {
  try {
    const response = await api.get('/recommendations/destinations', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
};

export const getTrendingDestinations = async (limit: number = 5) => {
  try {
    const response = await api.get('/recommendations/destinations/trending', { 
      params: { limit } 
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching trending destinations:', error);
    throw error;
  }
};