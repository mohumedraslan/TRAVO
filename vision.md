# 🚀 TRAVO: Automatic AI Travel Diary

**Current Version:** 1.0 (MVP)
**Status:** Live / Testing

TRAVO is a mobile application that automatically builds a travel diary from your photos. It uses AI to identify monuments and locations, creating a timeline of your trip without you needing to type a single word.

---

## ✅ Current Features (MVP)

The following features are fully implemented and functional:

### 1. Smart Camera & Identification
*   **Point & Shoot**: User takes a photo within the app.
*   **AI Recognition**: The backend (CLIP model) analyzes the image to identify landmarks (e.g., "Eiffel Tower", "Taj Mahal").
*   **GPS Fallback**: If AI is unsure, it falls back to GPS coordinates (currently defaults to 0,0 until `expo-location` is added).
*   **Zero Typing**: The location name is automatically logged.

### 2. Automatic Diary
*   **Timeline View**: A chronological feed of all your trips and visited places.
*   **Trip Management**: Start and end trips easily.
*   **Cloud Sync**: All data (photos, places, trips) is securely stored in Supabase.

### 3. Story Sharing
*   **Trip Summary**: Generates a shareable card with stats (Places Visited, Photos Taken).
*   **Social Sharing**: Uses native sharing to send the story to friends via Instagram, WhatsApp, etc.

---

## 🏗️ Technical Architecture

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Mobile App** | React Native (Expo) | UI, Camera, Gallery, Navigation |
| **Backend** | FastAPI (Python) | AI Logic, API Endpoints, Data Processing |
| **Database** | Supabase (PostgreSQL) | User Data, Trip Logs, Relational Data |
| **Storage** | Supabase Storage | Photo Hosting (`trip_photos` bucket) |
| **AI Model** | OpenAI CLIP | Image-to-Text / Zero-shot Classification |

---

## 🗺️ Roadmap: Version 2.0

The next phase of development focuses on precision, engagement, and polish.

### 1. 📍 Precision Location (High Priority)
*   **Real GPS Integration**: Implement `expo-location` to capture exact coordinates.
*   **Smart Fallback**: Combine AI confidence + GPS proximity for 99% accuracy.
*   **Map View**: Display the trip route on an interactive map (Google Maps / Mapbox).

### 2. 🧠 Enhanced AI
*   **Expanded Dataset**: Add more monuments and hidden gems to `monuments.json`.
*   **Fine-tuning**: Train a custom model layer for better accuracy on specific architectural styles.
*   **Offline Mode**: Basic recognition or caching for when data is unavailable.

### 3. 🎨 UI/UX Polish
*   **Rich Animations**: Smooth transitions between Diary and Details screens.
*   **Custom Themes**: Allow users to skin their diary (e.g., "Vintage", "Modern").
*   **Photo Gallery**: Better grid view for places with multiple photos.

### 4. 💰 Monetization (Future)
*   **Premium Export**: High-res PDF export of the diary.
*   **Unlimited Cloud**: Paid tier for storing unlimited full-res photos.

---

## 🧪 Development Philosophy

*   **Zero Friction**: The user should never have to type if the AI can guess it.
*   **Performance First**: The app must feel instant. Optimistic updates for UI.
*   **Privacy**: User data is theirs. Photos are private by default.
