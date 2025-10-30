export interface Recommendation {
  id: string;
  destinationName: string;
  destinationId: string;
  description: string;
  imageUrl: string;
  rating: number;
  priceEstimate: {
    min: number;
    max: number;
    currency: string;
  };
  tags: string[];
  bestTimeToVisit: string[];
  crowdLevel?: CrowdLevel;
  userId: string;
  createdAt: string;
}

export enum CrowdLevel {
  LOW = 'low',
  MODERATE = 'moderate',
  HIGH = 'high',
  VERY_HIGH = 'very_high'
}
