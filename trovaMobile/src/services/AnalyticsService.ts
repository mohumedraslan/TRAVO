import * as Sentry from 'sentry-expo';
import PostHog from 'posthog-react-native';
import Constants from 'expo-constants';

// Initialize Sentry
try {
    const dsn = 'YOUR_SENTRY_DSN'; // Replace with actual DSN or env var
    if (dsn && dsn !== 'YOUR_SENTRY_DSN') {
        Sentry.init({
            dsn: dsn,
            enableInExpoDevelopment: true,
            debug: __DEV__,
        });
    } else {
        console.log('Sentry DSN not set, skipping initialization');
    }
} catch (e) {
    console.warn('Sentry initialization failed:', e);
}

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
            if (Sentry.Native) {
                Sentry.Native.setUser({ id: userId, ...traits });
            }
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
            if (Sentry.Native) {
                Sentry.Native.setUser(null);
            }
        } catch (e) {
            console.warn('Analytics reset error:', e);
        }
    }
}

export default AnalyticsService;
