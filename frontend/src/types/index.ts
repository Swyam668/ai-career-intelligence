export interface Profile {
  job_title: string;
  education_level: number;
  industry: string;
  company_size: string;
  location: string;
  remote_work: string;
  experience_years: number;
  skills: string[];
  certifications: number;
}

export interface Recommendation {
  job_title: string;
  role: string;
  qualifications: string;
  experience: string;
  similarity_score: number;
  match_percentage: number;
  matched_skills: string[];
  missing_skills: string[];
}

export type SalaryExplanationItem = {
  feature: string;
  title: string;
  message: string;
  impact: number;
  effect: "positive" | "negative";
};

export type SalaryResult = {
  predicted_salary: number;
  base_salary: number;
  explanation: SalaryExplanationItem[];
};

export interface AnalysisResponse {
  profile: Profile;
  recommendations: Recommendation[];
  salary: SalaryResult;
}