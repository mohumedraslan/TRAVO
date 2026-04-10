import React, { useState } from 'react';
import { TextField, Select, MenuItem, FormControl, InputLabel, Chip, Box, Button } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

interface SearchFilterBarProps {
  onSearch: (filters: {
    query: string;
    interests: string[];
    city: string;
  }) => void;
}

const interests = [
  'Pyramids', 'Museums', 'Temples', 'Beaches', 'Food', 'Shopping',
  'History', 'Architecture', 'Nature', 'Adventure'
];

const cities = [
  'Cairo', 'Alexandria', 'Luxor', 'Aswan', 'Hurghada', 'Sharm El Sheikh',
  'Giza', 'Dahab', 'Marsa Alam', 'Siwa'
];

const SearchFilterBar: React.FC<SearchFilterBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [selectedCity, setSelectedCity] = useState('');

  const handleInterestChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedInterests(event.target.value as string[]);
  };

  const handleCityChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedCity(event.target.value as string);
  };

  const handleSearch = () => {
    onSearch({
      query,
      interests: selectedInterests,
      city: selectedCity,
    });
  };

  return (
    <Box sx={{ p: 2, backgroundColor: 'white', borderRadius: 1, boxShadow: 1, mb: 3 }}>
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 2 }}>
        <TextField
          fullWidth
          label="Search"
          variant="outlined"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          InputProps={{
            endAdornment: <SearchIcon />,
          }}
        />
        
        <FormControl fullWidth>
          <InputLabel>City</InputLabel>
          <Select
            value={selectedCity}
            label="City"
            onChange={handleCityChange}
          >
            <MenuItem value="">All Cities</MenuItem>
            {cities.map((city) => (
              <MenuItem key={city} value={city}>{city}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
      
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>Interests</InputLabel>
        <Select
          multiple
          value={selectedInterests}
          label="Interests"
          onChange={handleInterestChange}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {(selected as string[]).map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
        >
          {interests.map((interest) => (
            <MenuItem key={interest} value={interest}>{interest}</MenuItem>
          ))}
        </Select>
      </FormControl>
      
      <Button 
        variant="contained" 
        color="primary" 
        onClick={handleSearch}
        startIcon={<SearchIcon />}
      >
        Search
      </Button>
    </Box>
  );
};

export default SearchFilterBar;