export interface BobResponse {
  agent: string;
  mode: string;
  message?: string;
  summary?: string;
  diagnosis?: string;
  next_steps?: string[];
  recommended_cases?: string[];
  milestones?: Array<{ name: string; goal: string }>;
  suggestions?: string[];
  risks?: string[];
}
