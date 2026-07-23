export type Verdict = "FULL" | "PARTIAL" | "ABSENT" | "INCORRECT";
export type PipelinePhase = "idle" | "grading" | "awaiting_review" | "complete";

export interface ExamSummary {
  exam_id: string;
  subject: string;
  phase: PipelinePhase;
  total_students: number;
  graded_count: number;
  deferred_count: number;
  corrections_count: number;
  review_complete: boolean;
  final_results_count: number;
  defer_rate: number;
  message: string;
}

export interface ReviewProgress {
  total: number;
  resolved: number;
  remaining: number;
  is_complete: boolean;
}

export interface CbteSignals {
  tier_resolved: number;
  signal_1_evidence_verified: boolean;
  signal_2_nli_score: number | null;
  signal_3_stability: number | null;
  signal_4_keyword_score: number;
  keywords_found: string[];
  reason: string;
}

export interface ReviewItem {
  review_item_id: string;
  cbte_result_id: string;
  cgr_result_id: string;
  student_id: string;
  concept_id: string;
  question_id: string;
  knowledge_point: string;
  max_marks: number;
  student_answer: string;
  system_verdict: Verdict;
  system_marks: number;
  evidence_span: string;
  reasoning: string;
  trust_score: number;
  defer_reason: string;
  signals: CbteSignals | null;
}

export interface ReviewPayload {
  items: ReviewItem[];
  progress: ReviewProgress;
}

export interface ConceptFeedback {
  concept_id: string;
  knowledge_point: string;
  verdict: Verdict;
  marks_awarded: number;
  max_marks: number;
  evidence_span: string;
  reasoning: string;
  trust_score: number;
  reviewed_by: "auto" | "teacher";
  teacher_comment: string | null;
}

export interface FinalResult {
  student_id: string;
  question_id: string;
  final_score: number;
  total_marks: number;
  overall_trust: number;
  has_deferred_concepts: boolean;
  all_concepts_resolved: boolean;
  concept_results: ConceptFeedback[];
}
