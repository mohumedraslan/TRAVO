import { CrowdLevel } from './Recommendation';

export interface CrowdPrediction {
  id: string;
  destinationId: string;
  destinationName: string;
  currentCrowdLevel: CrowdLevel;
  predictedCrowdLevels: HourlyPrediction[];
  lastUpdated: string;
  confidence: number;
  factors: PredictionFactor[];
}

export interface HourlyPrediction {
  hour: number;
  crowdLevel: CrowdLevel;
  confidence: number;
}

export interface PredictionFactor {
  name: string;
  impact: number; // -1 to 1 scale where negative reduces crowds, positive increases
  description: string;
}
