import React, { useState, useEffect } from 'react';
import { Container, Grid, Typography, Box, Paper, CircularProgress, Divider } from '@mui/material';
import SearchFilterBar from '../components/SearchFilterBar';
import ItineraryCard from '../components/ItineraryCard';
import CrowdHeatmap from '../components/CrowdHeatmap';
import { getRecommendations, Recommendation } from '../services/recommendationService';
import { getCrowdHeatmap, HeatmapDataPoint } from '../services/crowdService';

const DiscoverEgypt: React.FC = () => {
  // State for recommendations
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [isLoadingRecommendations, setIsLoadingRecommendations] = useState(true);
  const [recommendationsError, setRecommendationsError] = useState<any>(null);
  
  // State for crowd heatmap
  const [heatmapData, setHeatmapData] = useState<HeatmapDataPoint[]>([]);
  const [isLoadingHeatmap, setIsLoadingHeatmap] = useState(true);
  const [heatmapError, setHeatmapError] = useState<any>(null);
  
  // State for filters
  const [filters, setFilters] = useState({
    query: '',
    interests: [] as string[],
    city: '',
  });
  
  // Current date and time for crowd predictions
  const [currentDate, setCurrentDate] = useState('');
  const [currentTime, setCurrentTime] = useState('');
  
  useEffect(() => {
    // Set current date and time
    const now = new Date();
    setCurrentDate(now.toISOString().split('T')[0]);
    setCurrentTime(`${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`);
    
    // Load initial data
    fetchRecommendations();
    fetchHeatmapData();
  }, []);
  
  const fetchRecommendations = async () => {
    setIsLoadingRecommendations(true);
    setRecommendationsError(null);
    
    try {
      // Convert filters to API format
      const apiFilters = {
        categories: filters.interests,
        city: filters.city || undefined,
      };
      
      const data = await getRecommendations(apiFilters);
      setRecommendations(data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setRecommendationsError(error);
    } finally {
      setIsLoadingRecommendations(false);
    }
  };
  
  const fetchHeatmapData = async () => {
    setIsLoadingHeatmap(true);
    setHeatmapError(null);
    
    try {
      const data = await getCrowdHeatmap(currentDate, currentTime);
      setHeatmapData(data);
    } catch (error) {
      console.error('Error fetching heatmap data:', error);
      setHeatmapError(error);
    } finally {
      setIsLoadingHeatmap(false);
    }
  };
  
  const handleSearch = (newFilters: typeof filters) => {
    setFilters(newFilters);
    fetchRecommendations();
  };
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: '#1976d2' }}>
        Discover Egypt
      </Typography>
      <Typography variant="h6" gutterBottom sx={{ color: 'text.secondary', mb: 4 }}>
        Explore the wonders of Egypt with personalized recommendations and real-time crowd information
      </Typography>
      
      <SearchFilterBar onSearch={handleSearch} />
      
      <Grid container spacing={4}>
        {/* Recommendations Section */}
        <Grid item xs={12} md={7}>
          <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Recommended Itineraries
            </Typography>
            
            {isLoadingRecommendations ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
              </Box>
            ) : recommendationsError ? (
              <Box sx={{ p: 2 }}>
                <Typography color="error">
                  Error loading recommendations. Please try again.
                </Typography>
              </Box>
            ) : recommendations.length === 0 ? (
              <Box sx={{ p: 2 }}>
                <Typography>
                  No recommendations found. Try adjusting your filters.
                </Typography>
              </Box>
            ) : (
              <Grid container spacing={2}>
                {recommendations.map((recommendation) => (
                  <Grid item xs={12} sm={6} key={recommendation.id}>
                    <ItineraryCard 
                      recommendation={recommendation} 
                      onClick={() => console.log('View details for', recommendation.name)}
                    />
                  </Grid>
                ))}
              </Grid>
            )}
          </Paper>
        </Grid>
        
        {/* Crowd Heatmap Section */}
        <Grid item xs={12} md={5}>
          <CrowdHeatmap
            data={heatmapData}
            isLoading={isLoadingHeatmap}
            error={heatmapError}
            date={currentDate}
            time={currentTime}
          />
        </Grid>
      </Grid>
      
      <Box sx={{ mt: 4 }}>
        <Divider sx={{ mb: 2 }} />
        <Typography variant="body2" color="text.secondary" align="center">
          © {new Date().getFullYear()} TRAVO - AI-Powered Travel Companion
        </Typography>
      </Box>
    </Container>
  );
};

export default DiscoverEgypt;