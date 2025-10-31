# TRAVO Web App - Discover Egypt Dashboard

## Overview

The TRAVO Web App is a Next.js application that provides an interactive dashboard for exploring Egypt's tourist destinations. The "Discover Egypt" dashboard offers personalized recommendations, crowd prediction heatmaps, and search/filter functionality to help travelers plan their trips effectively.

## Features

- **Recommended Itineraries**: Browse personalized travel recommendations based on interests and location preferences
- **Interactive Map**: Visualize destinations and points of interest on an interactive map
- **Crowd Prediction Heatmap**: View real-time crowd levels at popular destinations to plan visits during less crowded times
- **Search & Filter**: Find destinations by name, category, or city

## Project Structure

```
travo/frontend/web_app/
├── package.json        # Project dependencies and scripts
├── src/                # Source code
│   ├── pages/          # Next.js pages
│   │   ├── _app.tsx    # App configuration and global providers
│   │   ├── index.tsx   # Home page (redirects to discover-egypt)
│   │   └── discover-egypt.tsx  # Main dashboard page
│   ├── components/     # Reusable React components
│   │   ├── SearchFilterBar.tsx # Search and filtering component
│   │   ├── ItineraryCard.tsx   # Card for displaying recommendations
│   │   └── CrowdHeatmap.tsx    # Map with crowd heatmap visualization
│   ├── services/       # API service modules
│   │   ├── api.ts      # Base API configuration
│   │   ├── recommendationService.ts # Recommendation API functions
│   │   └── crowdService.ts     # Crowd prediction API functions
│   └── styles/         # Global styles
│       └── globals.css # Global CSS styles
```

## Getting Started

### Prerequisites

- Node.js 14.x or higher
- npm or yarn

### Installation

```bash
# Navigate to the web app directory
cd travo/frontend/web_app

# Install dependencies
npm install
# or
yarn install
```

### Development

```bash
# Start the development server
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

### Building for Production

```bash
# Build the application
npm run build
# or
yarn build

# Start the production server
npm start
# or
yarn start
```

## API Integration

The web app connects to the TRAVO backend API for data. The main endpoints used are:

- `/api/recommendations` - Get personalized travel recommendations
- `/api/crowd-predictions` - Get crowd predictions for specific locations
- `/api/crowd-heatmap` - Get crowd heatmap data for multiple locations

API services are implemented in the `src/services` directory.

## Technologies

- **Next.js** - React framework for server-rendered applications
- **Material-UI** - React component library for consistent UI design
- **Mapbox GL JS** - Interactive mapping library for the crowd heatmap
- **Axios** - HTTP client for API requests
- **SWR** - React Hooks for data fetching

## Contributing

Please follow the existing code style and component structure when contributing to this project. Make sure to test your changes thoroughly before submitting a pull request.