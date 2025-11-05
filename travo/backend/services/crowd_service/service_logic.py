import numpy as np
import pandas as pd
from datetime import datetime, time
import pickle
import os
import random
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from .schemas import CrowdLevel, CrowdPredictionRequest, CrowdPredictionResponse

# Constants
MODEL_PATH = os.path.join(os.path.dirname(__file__), "crowd_model.pkl")
MONUMENT_PEAK_HOURS = {
    "pyr_giza": [(10, 14), (15, 17)],  # 10AM-2PM and 3PM-5PM are peak hours
    "sphinx": [(9, 12), (14, 16)],
    "luxor": [(11, 15)],
    "karnak": [(10, 13), (16, 18)],
    "abu_simbel": [(8, 11), (14, 16)],
    "valley_kings": [(9, 14)],
    "philae": [(10, 15)],
    "hatshepsut": [(9, 12), (15, 17)],
}

# Seasonal factors (higher values = more crowded)
MONTH_FACTORS = {
    1: 0.6,   # January
    2: 0.7,   # February
    3: 0.8,   # March
    4: 0.9,   # April
    5: 0.7,   # May
    6: 0.6,   # June
    7: 0.8,   # July
    8: 0.9,   # August
    9: 0.8,   # September
    10: 1.0,  # October - peak season
    11: 0.9,  # November
    12: 0.8,  # December
}

# Day factors (weekends are more crowded)
DAY_FACTORS = {
    0: 0.9,  # Monday
    1: 0.8,  # Tuesday
    2: 0.8,  # Wednesday
    3: 0.9,  # Thursday
    4: 1.0,  # Friday
    5: 1.0,  # Saturday
    6: 1.0,  # Sunday
}


def generate_synthetic_data(n_samples: int = 1000) -> pd.DataFrame:
    """Generate synthetic data for training the crowd prediction model.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        DataFrame with synthetic training data
    """
    data = []
    monument_ids = list(MONUMENT_PEAK_HOURS.keys())
    
    for _ in range(n_samples):
        monument_id = random.choice(monument_ids)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Simplified to avoid month length issues
        hour = random.randint(8, 19)  # Opening hours 8AM to 7PM
        minute = random.choice([0, 15, 30, 45])
        
        # Calculate base crowd factor
        crowd_factor = 0.0
        
        # Add time-based factor
        time_factor = 0.0
        for peak_start, peak_end in MONUMENT_PEAK_HOURS.get(monument_id, [(10, 15)]):
            if peak_start <= hour < peak_end:
                time_factor = 0.7
                break
        
        # Add seasonal factor
        season_factor = MONTH_FACTORS.get(month, 0.7)
        
        # Add day of week factor (simplified)
        day_of_week = (day % 7)  # Simplified calculation
        day_factor = DAY_FACTORS.get(day_of_week, 0.8)
        
        # Combine factors with some randomness
        crowd_factor = (0.3 * time_factor + 0.4 * season_factor + 0.3 * day_factor) 
        crowd_factor += random.uniform(-0.2, 0.2)  # Add noise
        
        # Determine crowd level
        if crowd_factor < 0.4:
            crowd_level = CrowdLevel.LOW
        elif crowd_factor < 0.7:
            crowd_level = CrowdLevel.MEDIUM
        else:
            crowd_level = CrowdLevel.HIGH
        
        # Create data point
        data.append({
            "monument_id": monument_id,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "crowd_level": crowd_level
        })
    
    return pd.DataFrame(data)


def train_model() -> Tuple[RandomForestClassifier, OneHotEncoder]:
    """Train a machine learning model for crowd prediction.
    
    Returns:
        Tuple of (trained model, encoder)
    """
    # Generate synthetic data
    df = generate_synthetic_data(2000)
    
    # Prepare features and target
    X = df[['monument_id', 'month', 'day', 'hour', 'minute']]
    y = df['crowd_level']
    
    # Encode categorical features
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X[['monument_id']])
    
    # Combine with numerical features
    X_numeric = X[['month', 'day', 'hour', 'minute']].values
    X_combined = np.hstack([X_encoded, X_numeric])
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_combined, y)
    
    return model, encoder


def save_model(model: RandomForestClassifier, encoder: OneHotEncoder) -> None:
    """Save the trained model and encoder to disk.
    
    Args:
        model: Trained RandomForestClassifier
        encoder: Fitted OneHotEncoder
    """
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump((model, encoder), f)


def load_model() -> Tuple[RandomForestClassifier, OneHotEncoder]:
    """Load the trained model and encoder from disk.
    
    Returns:
        Tuple of (trained model, encoder)
    """
    try:
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        # Train a new model if not found
        model, encoder = train_model()
        save_model(model, encoder)
        return model, encoder


def predict_crowd_level(request: CrowdPredictionRequest) -> CrowdPredictionResponse:
    """Predict crowd level for a monument at a specific time.
    
    Args:
        request: CrowdPredictionRequest with monument_id, month, day, and time
        
    Returns:
        CrowdPredictionResponse with the prediction
    """
    # Parse time string
    hour, minute = map(int, request.time.split(':'))
    
    # Load or train model
    model, encoder = load_model()
    
    # Prepare input features
    input_data = pd.DataFrame([
        {
            'monument_id': request.monument_id,
            'month': request.month,
            'day': request.day,
            'hour': hour,
            'minute': minute
        }
    ])
    
    # Encode categorical features
    X_encoded = encoder.transform(input_data[['monument_id']])
    
    # Combine with numerical features
    X_numeric = input_data[['month', 'day', 'hour', 'minute']].values
    X_combined = np.hstack([X_encoded, X_numeric])
    
    # Make prediction
    prediction = model.predict(X_combined)[0]
    confidence = max(model.predict_proba(X_combined)[0])
    
    # Calculate wait time based on crowd level
    wait_time = None
    if prediction == CrowdLevel.LOW:
        wait_time = random.randint(5, 15)
    elif prediction == CrowdLevel.MEDIUM:
        wait_time = random.randint(15, 30)
    elif prediction == CrowdLevel.HIGH:
        wait_time = random.randint(30, 60)
    
    # Create response
    prediction_time = datetime.now()
    response = CrowdPredictionResponse(
        monument_id=request.monument_id,
        prediction_time=prediction_time,
        crowd_level=prediction,
        confidence=float(confidence),
        wait_time_minutes=wait_time
    )
    
    return response


# Initialize model on module load
def initialize_model():
    """Initialize the model when the module is loaded."""
    try:
        load_model()
    except Exception as e:
        print(f"Error initializing crowd prediction model: {e}")
        # Train a new model
        model, encoder = train_model()
        save_model(model, encoder)


# Call initialization function
initialize_model()
