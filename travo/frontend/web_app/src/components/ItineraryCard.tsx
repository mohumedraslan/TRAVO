import React from 'react';
import { Card, CardContent, CardMedia, Typography, Box, Chip, Rating } from '@mui/material';
import { Recommendation } from '../services/recommendationService';

interface ItineraryCardProps {
  recommendation: Recommendation;
  onClick?: () => void;
}

const ItineraryCard: React.FC<ItineraryCardProps> = ({ recommendation, onClick }) => {
  const { name, description, location, rating, imageUrl, category } = recommendation;
  
  return (
    <Card 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        cursor: onClick ? 'pointer' : 'default',
        '&:hover': {
          boxShadow: onClick ? 6 : 1,
          transform: onClick ? 'scale(1.02)' : 'none',
          transition: 'all 0.2s ease-in-out'
        }
      }}
      onClick={onClick}
    >
      <CardMedia
        component="img"
        height="160"
        image={imageUrl || 'https://source.unsplash.com/random?egypt'}
        alt={name}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
          <Typography gutterBottom variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
            {name}
          </Typography>
          <Chip 
            label={category} 
            size="small" 
            color="primary" 
            sx={{ ml: 1 }}
          />
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Rating value={rating} precision={0.5} readOnly size="small" />
          <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
            {rating.toFixed(1)}
          </Typography>
        </Box>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {location.city}, {location.country}
        </Typography>
        
        <Typography variant="body2" color="text.secondary">
          {description.length > 120 ? `${description.substring(0, 120)}...` : description}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default ItineraryCard;