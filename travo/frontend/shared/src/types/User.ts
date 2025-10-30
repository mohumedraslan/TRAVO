export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  profilePicture?: string;
  preferences?: UserPreferences;
  createdAt: string;
  updatedAt: string;
}

export interface UserPreferences {
  favoriteDestinations?: string[];
  travelInterests?: string[];
  accommodationPreferences?: string[];
  budgetRange?: {
    min: number;
    max: number;
    currency: string;
  };
  notificationSettings?: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
}
