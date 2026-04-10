import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LoginScreen from '../screens/LoginScreen';
import SignupScreen from '../screens/SignupScreen';
import ExploreScreen from '../screens/ExploreScreen';
import CameraScreen from '../screens/CameraScreen';
import ItineraryScreen from '../screens/ItineraryScreen';
import SettingsScreen from '../screens/SettingsScreen';
import NotificationsScreen from '../screens/NotificationsScreen';
import PrivacyScreen from '../screens/PrivacyScreen';
import FavoritesScreen from '../screens/FavoritesScreen';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();
const SettingsStack = createNativeStackNavigator();
const RootStack = createNativeStackNavigator();

// Settings nested stack
const SettingsStackScreen = () => (
  <SettingsStack.Navigator>
    <SettingsStack.Screen name="SettingsHome" component={SettingsScreen} options={{ title: 'Settings' }} />
    <SettingsStack.Screen name="Notifications" component={NotificationsScreen} />
    <SettingsStack.Screen name="Privacy" component={PrivacyScreen} />
    <SettingsStack.Screen name="Favorites" component={FavoritesScreen} />
  </SettingsStack.Navigator>
);

// Main app tabs
const MainTabs = () => (
  <Tab.Navigator>
    <Tab.Screen name="Explore" component={ExploreScreen} />
    <Tab.Screen name="Camera" component={CameraScreen} />
    <Tab.Screen name="Itinerary" component={ItineraryScreen} />
    <Tab.Screen name="Settings" component={SettingsStackScreen} options={{ headerShown: false }} />
  </Tab.Navigator>
);

// Auth stack (login/signup)
const AuthStack = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="Login" component={LoginScreen} />
    <Stack.Screen name="Signup" component={SignupScreen} />
  </Stack.Navigator>
);

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <RootStack.Navigator screenOptions={{ headerShown: false }}>
        <RootStack.Screen name="Auth" component={AuthStack} />
        <RootStack.Screen name="Main" component={MainTabs} />
      </RootStack.Navigator>
    </NavigationContainer>
  );
}
