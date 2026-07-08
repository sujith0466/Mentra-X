/**
 * Mentra X — Weakness Intelligence Frontend API Client
 * 
 * Communicates with backend REST endpoints for weakness diagnostics, pre-test vulnerability
 * scans, misconception taxonomy reports, multi-step remediation plans, and verification mutations.
 */

export interface WeaknessItem {
  concept_id: string;
  concept_name?: string;
  mastery_score: number;
  severity: "Critical" | "At Risk" | "Needs Practice" | "Learning" | "Mastery";
  mistake_count: number;
  why_detected?: string;
  last_assessed?: string;
}

export interface WeaknessProfileResponse {
  status: string;
  profile: {
    user_id: number;
    weaknesses: WeaknessItem[];
    strengths: WeaknessItem[];
    overall_confidence: number;
    timeline_state: string;
    last_updated: string;
  };
}

export interface RemediationStep {
  step_number: number;
  step_type: "Review Prerequisite" | "Targeted Study" | "Misconception Drill" | "Mastery Verification";
  title: string;
  description: string;
  status: "pending" | "active" | "completed";
  action_url?: string;
}

export interface RemediationPlan {
  plan_id: string;
  user_id: number;
  concept_id: string;
  created_at: string;
  status: string;
  step_by_step_path: RemediationStep[];
  avoidance_constraints: {
    levels_to_avoid: number[];
    analogies_to_avoid: string[];
    analogies_that_worked: string[];
  };
}

export interface CustomQuizQuestion {
  question_id: string;
  question_text: string;
  options: string[];
  correct_option_index: number;
  explanation: string;
  taxonomy_category: string;
}

export const weaknessApi = {
  async getProfile(userId: number): Promise<WeaknessProfileResponse> {
    const res = await fetch(`/api/weakness/profile/${userId}`);
    if (!res.ok) throw new Error("Failed to fetch weakness profile");
    return res.json();
  },

  async getVulnerabilities(userId: number, quizId: number): Promise<any> {
    const res = await fetch(`/api/weakness/vulnerabilities/${userId}/${quizId}`);
    if (!res.ok) throw new Error("Failed to scan quiz vulnerabilities");
    return res.json();
  },

  async getMisconceptions(userId: number): Promise<any> {
    const res = await fetch(`/api/weakness/misconceptions/${userId}`);
    if (!res.ok) throw new Error("Failed to fetch misconception reports");
    return res.json();
  },

  async getRemediationPlan(userId: number, conceptId: string): Promise<{ status: string; remediation_plan: RemediationPlan }> {
    const res = await fetch(`/api/weakness/remediation/${userId}/${conceptId}`);
    if (!res.ok) throw new Error("Failed to get remediation plan");
    return res.json();
  },

  async generateQuiz(userId: number, conceptId: string): Promise<{ status: string; custom_quiz: { questions: CustomQuizQuestion[] } }> {
    const res = await fetch(`/api/weakness/remediation/quiz/${userId}/${conceptId}`, { method: "POST" });
    if (!res.ok) throw new Error("Failed to generate remediation drill");
    return res.json();
  },

  async verifyRemediation(payload: { user_id: number; concept_id: string; passed: boolean; new_score?: number }): Promise<any> {
    const res = await fetch("/api/weakness/remediation/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to verify remediation completion");
    return res.json();
  },
};
