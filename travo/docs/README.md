# TRAVO

## Overview
TRAVO is a comprehensive travel platform that leverages AI and machine learning to provide personalized travel recommendations, crowd predictions, visual identification of landmarks, and an intelligent travel assistant.

## Project Structure

```
/travo
│
├── backend/
│   ├── services/
│   │   ├── user_service/
│   │   ├── recommendation_service/
│   │   ├── crowd_service/
│   │   ├── vision_service/
│   │   ├── assistant_service/
│   │   └── business_service/
│   ├── models/
│   ├── utils/
│   ├── api/
│   └── main.py
│
├── frontend/
│   ├── mobile_app/  → for React Native (iOS + Android)
│   ├── web_app/     → for Next.js frontend
│   └── shared/      → shared UI and logic components
│
├── data/
│   ├── datasets/
│   ├── pipelines/
│   └── docs/
│
├── ml_models/
│   ├── recommendation/
│   ├── crowd_prediction/
│   ├── vision_identification/
│   ├── nlp_assistant/
│
└── docs/
    ├── README.md
    ├── version_roadmap.md
    ├── architecture_diagram.png
    └── api_spec.yaml
```

## Getting Started

### Backend
The backend is built with FastAPI, SQLAlchemy, and various ML libraries.

```bash
# Navigate to the backend directory
cd travo/backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

### Frontend

#### Web App
```bash
# Navigate to the web app directory
cd travo/frontend/web_app

# Install dependencies
npm install

# Run the development server
npm run dev
```

#### Mobile App
```bash
# Navigate to the mobile app directory
cd travo/frontend/mobile_app

# Install dependencies
npm install

# Run for iOS
npm run ios

# Run for Android
npm run android
```

## Features
- Personalized travel recommendations
- Real-time crowd predictions for popular destinations
- Visual identification of landmarks and attractions
- AI-powered travel assistant
- Business integration for local services

## Technologies
- **Backend**: FastAPI, Pydantic, SQLAlchemy
- **ML/AI**: TensorFlow, PyTorch, OpenCV, scikit-learn
- **Frontend**: Next.js, React Native
- **Data**: Various datasets for training ML models

## License
This project is proprietary and confidential.
