import type {
  BreakdownPayload,
  ExamSummary,
  FinalResult,
  ReviewPayload,
  Verdict,
} from "./types";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    ...init,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? JSON.stringify(body);
    } catch {
      /* ignore */
    }
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  listExams: () => request<ExamSummary[]>("/api/exams"),
  getReview: (examId: string) =>
    request<ReviewPayload>(`/api/exams/${encodeURIComponent(examId)}/review`),
  submitCorrection: (
    examId: string,
    body: {
      student_id: string;
      concept_id: string;
      verdict: Verdict;
      marks: number;
      comment?: string;
    },
  ) =>
    request<{ progress: ReviewPayload["progress"] }>(
      `/api/exams/${encodeURIComponent(examId)}/review`,
      { method: "POST", body: JSON.stringify(body) },
    ),
  finalize: (examId: string) =>
    request<{ final_results: FinalResult[] }>(
      `/api/exams/${encodeURIComponent(examId)}/finalize`,
      { method: "POST" },
    ),
  getResults: (examId: string) =>
    request<FinalResult[]>(`/api/exams/${encodeURIComponent(examId)}/results`),
  getBreakdown: (examId: string) =>
    request<BreakdownPayload>(
      `/api/exams/${encodeURIComponent(examId)}/breakdown`,
    ),
};
