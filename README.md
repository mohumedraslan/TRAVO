# TRAVO - Travel Assistant Application

## Overview

TRAVO is an intelligent travel assistant application that helps users identify monuments, get personalized travel recommendations, and plan their trips efficiently. The application uses computer vision for monument identification and a rule-based recommendation engine to suggest personalized itineraries.

## Features

- **Monument Identification**: Upload images to identify famous monuments and landmarks
- **Personalized Recommendations**: Get travel recommendations based on interests and preferences
- **Rule-based Itineraries**: Generate day-by-day itineraries for destinations
- **AI Assistant**: Get information about monuments, history, and visiting tips through text or voice
- **Voice Interaction**: Convert voice to text and text to voice for hands-free experience
- **Crowd Prediction**: Get real-time crowd level predictions for monuments
- **User Management**: Register, login, and manage user preferences
- **API Documentation**: Comprehensive API documentation with OpenAPI specification

## Project Structure

```
TRAVO/
├── travo/
│   ├── backend/
│   │   ├── docs/
│   │   │   └── api_spec.yaml
│   │   ├── services/
│   │   │   ├── vision_service/
│   │   │   ├── recommendation_service/
│   │   │   ├── assistant_service/
│   │   │   ├── crowd_service/
│   │   │   └── user_service/
│   │   ├── utils/
│   │   │   └── auth.py
│   │   ├── tests/
│   │   ├── config.py
│   │   ├── main.py
│   │   └── run_tests.py
│   └── docs/
│       └── version_roadmap.md
└── trovaweb/
    ├── src/
    │   ├── app/
    │   └── components/
    ├── public/
    └── package.json
```

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- Git

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TRAVO.git
   cd TRAVO
   ```

2. Create and activate a virtual environment:
   ```bash
   # For Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # For macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   cd travo/backend
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///./travo.db
   VISION_API_KEY=your_vision_api_key
   WEATHER_API_KEY=your_weather_api_key
   JWT_SECRET_KEY=your_jwt_secret_key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd trovaweb
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Testing

### Running Backend Tests

Use the provided test script to run the backend tests:

```bash
cd travo/backend
python run_tests.py
```

Options:
- `--service [all|vision|recommendation|assistant|crowd|user|auth]`: Specify which service tests to run
- `--verbose` or `-v`: Enable verbose output
- `--coverage`: Generate coverage report

Example:
```bash
python run_tests.py --service crowd --coverage
```

### Running Frontend Tests

```bash
cd trovaweb
npm test
# or
yarn test
```

## API Documentation

The API documentation is available in OpenAPI format at `travo/backend/docs/api_spec.yaml`. When the backend server is running, you can access the interactive API documentation at `http://localhost:8000/docs`.

### Assistant Service Endpoints

- **POST /assistant/ask**: Send a text query to get information about monuments, history, or visiting tips
- **POST /assistant/voice_to_text**: Convert voice audio (base64 encoded) to text
- **POST /assistant/text_to_voice**: Convert text to voice audio (base64 encoded)
- **POST /assistant/upload_audio**: Upload an audio file for transcription

### Crowd Service Endpoints

- **POST /crowds/predict**: Get crowd level prediction for a monument at a specific time
- **GET /crowds/monuments**: Get a list of supported monuments for crowd prediction
- **GET /crowds/historical**: Get historical crowd data for a monument

### User Service Endpoints

- **POST /users/register**: Register a new user
- **POST /users/login**: Authenticate a user and get JWT token
- **GET /users/me**: Get current user information
- **GET /users/preferences**: Get user preferences
- **PUT /users/preferences**: Update user preferences

## Version Roadmap

See the [Version Roadmap](travo/docs/version_roadmap.md) for information about planned features and release stages.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.