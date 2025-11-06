# 🚀 TRAVO - Setup Guide

This guide will help you set up the TRAVO development environment for Android, iOS, and Web platforms.

## Prerequisites

- Node.js (v16 or later)
- npm (comes with Node.js)
- Python 3.8+
- Git
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/TRAVO.git
cd TRAVO
```

### 2. Run the Setup Script (Windows)

Open PowerShell as Administrator and run:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
.\setup_travo.ps1
```

### 3. Manual Setup (Alternative)

If the script doesn't work, follow these steps:

#### Install Expo CLI globally:
```bash
npm install -g expo-cli
```

#### Install dependencies:
```bash
cd trovaMobile
npm install --legacy-peer-deps
npm install onnxruntime-react-native --legacy-peer-deps
```

#### Start the backend:
```bash
cd ../travo/backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### In a new terminal, start Expo:
```bash
cd ../../trovaMobile
npx expo start
```

## 🌐 Environment Variables

Create a `.env` file in the `trovaMobile` directory with:

```env
EXPO_PUBLIC_API_URL=http://10.0.2.2:8000  # For Android emulator
# EXPO_PUBLIC_API_URL=http://localhost:8000  # For iOS/Web
```

## 📱 Running on Different Platforms

### Android
1. Make sure you have an Android emulator running or a device connected
2. Run: `npx expo run:android`

### iOS (macOS only)
1. Install CocoaPods: `sudo gem install cocoapods`
2. Install pods: `cd ios && pod install && cd ..`
3. Run: `npx expo run:ios`

### Web
```bash
npx expo start --web
```

## 🐛 Troubleshooting

### Expo Command Not Found
- Make sure Node.js and npm are installed correctly
- Try installing Expo CLI globally: `npm install -g expo-cli`
- Add npm global packages to your PATH if needed

### Network Errors on Android
- Use `http://10.0.2.2:8000` for Android emulator
- Make sure the backend is running
- Check if ports are not blocked by firewall

### Dependency Issues
- Delete `node_modules` and `package-lock.json`
- Run `npm cache clean --force`
- Reinstall with `npm install --legacy-peer-deps`

## 🤖 AI Model Setup

The app uses ONNX Runtime for AI inference. The model should be placed in `travo/ml_models/`.

## 📝 Notes

- For iOS development, you need a Mac with Xcode
- The backend runs on port 8000 by default
- Make sure your device/emulator is on the same network as your development machine

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
