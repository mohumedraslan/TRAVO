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
- Node.js 16 or higher
- npm or yarn
- Git
- Expo CLI (for mobile app)
- Android Studio / Xcode (for mobile app development)

## Setup and Running

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/TRAVO.git
   cd TRAVO
   ```

2. **Set up a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   cd travo/backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the `travo/backend` directory with:
   ```env
   # Required
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///./travo.db
   JWT_SECRET_KEY=your-jwt-secret-key
   
   # Optional (for production)
   VISION_API_KEY=your-google-vision-api-key
   WEATHER_API_KEY=your-weather-api-key
   
   # JWT Settings
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
   ```

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start the backend server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at `http://localhost:8000`
   - API Docs (Swagger UI): `http://localhost:8000/docs`
   - Alternative Docs (ReDoc): `http://localhost:8000/redoc`

### Web Frontend Setup

1. **Install dependencies**:
   ```bash
   cd trovaweb
   npm install  # or yarn install
   ```

2. **Set up environment variables**:
   Create a `.env.local` file in the `trovaweb` directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
   ```

3. **Start the development server**:
   ```bash
   npm run dev  # or yarn dev
   ```
   The web app will be available at `http://localhost:3000`

### Mobile App Setup

1. **Install Expo CLI** (if not already installed):
   ```bash
   npm install -g expo-cli
   ```

2. **Navigate to the mobile app directory**:
   ```bash
   cd travo/frontend/mobile
   ```

3. **Install dependencies**:
   ```bash
   npm install  # or yarn install
   ```

4. **Start the development server**:
   ```bash
   npx expo start
   ```
   This will open the Expo DevTools in your browser. From here you can:
   - Press `a` to open the app on an Android emulator
   - Press `i` to open the app on an iOS simulator
   - Scan the QR code with your phone's camera (requires Expo Go app)

## Example API Calls

### Authentication

**Register a new user**:
```http
POST /users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Login**:
```http
POST /users/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Monument Identification

**Identify a monument from image** (requires authentication):
```http
POST /vision/identify
Authorization: Bearer your-jwt-token
Content-Type: multipart/form-data

# Form data: file=@path/to/your/image.jpg
```

### Get Crowd Prediction

```http
GET /crowds/predict?monument_id=1&datetime=2025-12-25T14:30:00
Authorization: Bearer your-jwt-token
```

## Demo Credentials

For testing purposes, you can use the following demo account:

- **Email**: demo@travo.app
- **Password**: Demo@123

Or register a new account using the registration endpoint above.

## Environment Variables Reference

### Backend (`.env`)
- `DATABASE_URL`: Database connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `VISION_API_KEY`: Google Cloud Vision API key
- `WEATHER_API_KEY`: OpenWeatherMap API key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time

### Frontend (`.env.local`)
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`: Google Maps JavaScript API key

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