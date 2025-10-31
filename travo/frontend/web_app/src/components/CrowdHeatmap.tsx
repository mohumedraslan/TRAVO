import React, { useEffect, useRef } from 'react';
import { Box, Typography, CircularProgress, Paper } from '@mui/material';
import { HeatmapDataPoint } from '../services/crowdService';

interface CrowdHeatmapProps {
  data: HeatmapDataPoint[];
  isLoading: boolean;
  error: any;
  date: string;
  time: string;
}

declare global {
  interface Window {
    mapboxgl: any;
    MapboxGeocoder: any;
  }
}

const CrowdHeatmap: React.FC<CrowdHeatmapProps> = ({ data, isLoading, error, date, time }) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<any>(null);
  
  useEffect(() => {
    // Initialize map when component mounts
    if (!map.current && mapContainer.current && window.mapboxgl) {
      window.mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || '';
      
      map.current = new window.mapboxgl.Map({
        container: mapContainer.current,
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [31.2357, 30.0444], // Cairo, Egypt coordinates
        zoom: 9
      });
      
      // Add navigation controls
      map.current.addControl(new window.mapboxgl.NavigationControl());
      
      // Add geocoder for search
      if (window.MapboxGeocoder) {
        map.current.addControl(
          new window.MapboxGeocoder({
            accessToken: window.mapboxgl.accessToken,
            mapboxgl: window.mapboxgl,
            countries: 'eg', // Limit to Egypt
            placeholder: 'Search for a place in Egypt'
          })
        );
      }
    }
    
    return () => {
      // Clean up map when component unmounts
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, []);
  
  useEffect(() => {
    // Update heatmap data when it changes
    if (map.current && data && data.length > 0) {
      // Wait for map to be loaded
      if (!map.current.loaded()) {
        map.current.on('load', () => updateHeatmap());
      } else {
        updateHeatmap();
      }
    }
  }, [data]);
  
  const updateHeatmap = () => {
    const mapInstance = map.current;
    
    // Remove existing heatmap layer if it exists
    if (mapInstance.getSource('crowd-data')) {
      mapInstance.removeLayer('crowd-heat');
      mapInstance.removeSource('crowd-data');
    }
    
    // Add new heatmap layer
    mapInstance.addSource('crowd-data', {
      'type': 'geojson',
      'data': {
        'type': 'FeatureCollection',
        'features': data.map(point => ({
          'type': 'Feature',
          'properties': {
            'intensity': point.intensity,
            'locationId': point.locationId,
            'locationName': point.locationName
          },
          'geometry': {
            'type': 'Point',
            'coordinates': [point.longitude, point.latitude]
          }
        }))
      }
    });
    
    mapInstance.addLayer({
      'id': 'crowd-heat',
      'type': 'heatmap',
      'source': 'crowd-data',
      'paint': {
        'heatmap-weight': ['get', 'intensity'],
        'heatmap-intensity': 0.8,
        'heatmap-color': [
          'interpolate',
          ['linear'],
          ['heatmap-density'],
          0, 'rgba(0, 255, 0, 0)',
          0.2, 'rgba(0, 255, 0, 0.5)',
          0.4, 'rgba(255, 255, 0, 0.5)',
          0.6, 'rgba(255, 128, 0, 0.7)',
          0.8, 'rgba(255, 0, 0, 0.8)',
          1, 'rgba(255, 0, 0, 1)'
        ],
        'heatmap-radius': 20,
        'heatmap-opacity': 0.8
      }
    });
    
    // Add markers for each location
    data.forEach(point => {
      const popup = new window.mapboxgl.Popup({ offset: 25 })
        .setHTML(
          `<strong>${point.locationName}</strong><br>
           Crowd Level: ${getCrowdLevelText(point.intensity)}<br>
           <div style="width: 100px; height: 10px; background: linear-gradient(to right, green, yellow, orange, red);"></div>`
        );
      
      new window.mapboxgl.Marker({
        color: getCrowdLevelColor(point.intensity)
      })
        .setLngLat([point.longitude, point.latitude])
        .setPopup(popup)
        .addTo(mapInstance);
    });
  };
  
  const getCrowdLevelText = (intensity: number): string => {
    if (intensity < 0.25) return 'Low';
    if (intensity < 0.5) return 'Moderate';
    if (intensity < 0.75) return 'High';
    return 'Very High';
  };
  
  const getCrowdLevelColor = (intensity: number): string => {
    if (intensity < 0.25) return 'green';
    if (intensity < 0.5) return 'yellow';
    if (intensity < 0.75) return 'orange';
    return 'red';
  };
  
  return (
    <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
      <Typography variant="h6" gutterBottom>
        Crowd Prediction Heatmap
      </Typography>
      <Typography variant="subtitle2" gutterBottom>
        {date} at {time}
      </Typography>
      
      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
          <Typography color="error">
            Error loading crowd data. Please try again.
          </Typography>
        </Box>
      ) : (
        <Box
          ref={mapContainer}
          sx={{
            height: 400,
            borderRadius: 1,
            overflow: 'hidden',
            '& .mapboxgl-canvas': {
              borderRadius: 1
            }
          }}
        />
      )}
      
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: 'green', mr: 1 }} />
          <Typography variant="caption">Low</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: 'yellow', mr: 1 }} />
          <Typography variant="caption">Moderate</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: 'orange', mr: 1 }} />
          <Typography variant="caption">High</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: 'red', mr: 1 }} />
          <Typography variant="caption">Very High</Typography>
        </Box>
      </Box>
    </Paper>
  );
};

export default CrowdHeatmap;