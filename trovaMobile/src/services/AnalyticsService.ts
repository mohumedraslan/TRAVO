import PostHog from 'posthog-react-native';
import Constants from 'expo-constants';

// Initialize Sentry - DISABLED for now due to build errors
/*
import * as Sentry from 'sentry-expo';
try {
  const dsn = 'YOUR_SENTRY_DSN';
  if (dsn && dsn !== 'YOUR_SENTRY_DSN') {
    Sentry.init({
      dsn: dsn,
      enableInExpoDevelopment: true,
      debug: __DEV__,
    });
  }
} catch (e) {
  console.warn('Sentry initialization failed:', e);
}
*/

// Initialize PostHog
let posthog: PostHog | undefined;
try {
    const apiKey = 'YOUR_POSTHOG_API_KEY'; // Replace with actual API Key or env var
    if (apiKey && apiKey !== 'YOUR_POSTHOG_API_KEY') {
        // @ts-ignore
        posthog = new PostHog(apiKey, {
            host: 'https://app.posthog.com',
        });
    } else {
        console.log('PostHog API Key not set, skipping initialization');
    }
} catch (e) {
    console.warn('PostHog initialization failed:', e);
}

class AnalyticsService {
    static init() {
        // Already initialized above
    }

    static identify(userId: string, traits: Record<string, any> = {}) {
        try {
            posthog?.identify(userId, traits);
            // Sentry disabled
            /*
            if (Sentry.Native) {
              Sentry.Native.setUser({ id: userId, ...traits });
            }
            */
        } catch (e) {
            console.warn('Analytics identify error:', e);
        }
    }

    static track(eventName: string, properties: Record<string, any> = {}) {
        try {
            posthog?.capture(eventName, properties);
        } catch (e) {
            console.warn('Analytics track error:', e);
        }
    }

    static screen(screenName: string, properties: Record<string, any> = {}) {
        try {
            posthog?.screen(screenName, properties);
        } catch (e) {
            console.warn('Analytics screen error:', e);
        }
    }

    static reset() {
        try {
            posthog?.reset();
            // Sentry disabled
            /*
            if (Sentry.Native) {
              Sentry.Native.setUser(null);
            }
            */
        } catch (e) {
            console.warn('Analytics reset error:', e);
        }
    }
}

export default AnalyticsService;
