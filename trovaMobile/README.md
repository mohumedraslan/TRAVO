# TRAVO - Discover Egypt AI 👋

This is an [Expo](https://expo.dev) project for the TRAVO application.

## Get started

1. Install dependencies

   ```bash
   npm install
   ```

2. Configure your environment

   Edit the `.env` file and set your local backend URL:
   ```
   API_URL=http://192.168.X.X:8000/api
   ```
   Replace X.X with your PC's local IP address (e.g., 192.168.1.100)

3. Start the app for development

   ```bash
   npx expo start -c
   ```

## Running with Native Projects

Some features like VisionCamera cannot run in Expo Go. To use these features:

1. Create native projects

   ```bash
   npx expo prebuild
   ```

2. Run on Android

   ```bash
   npx expo run:android
   ```

3. Run on iOS

   ```bash
   npx expo run:ios
   ```

> **Note:** The app includes web fallbacks for camera functionality when running in a web browser.

You can start developing by editing the files inside the **app** directory. This project uses [file-based routing](https://docs.expo.dev/router/introduction).

## Maintaining and Updating

1. Check for outdated packages and update SDK

   ```bash
   npx expo doctor
   npx expo upgrade
   ```

2. Clean and rebuild the app

   ```bash
   npx expo start -c
   ```

## Learn more

To learn more about developing your project with Expo, look at the following resources:

- [Expo documentation](https://docs.expo.dev/): Learn fundamentals, or go into advanced topics with our [guides](https://docs.expo.dev/guides).
- [Learn Expo tutorial](https://docs.expo.dev/tutorial/introduction/): Follow a step-by-step tutorial where you'll create a project that runs on Android, iOS, and the web.

## Join the community

Join our community of developers creating universal apps.

- [Expo on GitHub](https://github.com/expo/expo): View our open source platform and contribute.
- [Discord community](https://chat.expo.dev): Chat with Expo users and ask questions.
