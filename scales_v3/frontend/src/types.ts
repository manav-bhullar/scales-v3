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

export type TrustDecision = "ACCEPT" | "DEFER";
export type JudgmentSource = "auto" | "teacher";

/** One concept judgment with the full "why these marks" trail. */
export interface ConceptExplain {
  concept_id: string;
  knowledge_point: string;
  target_criteria: string;
  max_marks: number;
  verdict: Verdict;
  marks_awarded: number;
  evidence_span: string;
  reasoning: string;
  counter_arguments: string;
  decision: TrustDecision;
  trust_score: number;
  tier_resolved: number;
  trust_reason: string;
  signal_1_evidence_verified: boolean;
  signal_2_nli_score: number | null;
  signal_3_stability: number | null;
  signal_4_keyword_score: number;
  expected_keywords: string[];
  keywords_found: string[];
  keywords_missing: string[];
  source: JudgmentSource;
  teacher_verdict: Verdict | null;
  teacher_marks: number | null;
  teacher_comment: string | null;
  correction_type: string | null;
}

export interface StudentExplain {
  student_id: string;
  answer_text: string;
  auto_score: number;
  current_score: number;
  total_marks: number;
  deferred_count: number;
  corrected_count: number;
  concepts: ConceptExplain[];
}

export interface RubricConcept {
  concept_id: string;
  knowledge_point: string;
  target_criteria: string;
  marks: number;
  expected_keywords: string[];
  acceptable_variants: string[];
}

export interface BreakdownPayload {
  exam_id: string;
  question: {
    question_id: string;
    question_text: string;
    reference_answer: string;
    rubric: string;
    total_marks: number;
  };
  concepts: RubricConcept[];
  students: StudentExplain[];
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
