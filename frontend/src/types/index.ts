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


type RoadmapPhase = {
  phase: string;
  duration: string;
  focus: string;
  skills: string[];
  action_items: string[];
};

type CareerRoadmap = {
  target_role: string;
  readiness_score: number;
  current_strengths: string[];
  priority_skills: string[];
  estimated_timeline: string;
  roadmap: RoadmapPhase[];
  project_suggestions: string[];
};


export interface AnalysisResponse {
  profile: Profile;
  recommendations: Recommendation[];
  salary: SalaryResult;
  career_roadmap: CareerRoadmap;
}