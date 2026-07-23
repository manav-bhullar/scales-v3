import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import type { ExamSummary } from "../types";
import { PhaseStepper } from "../components/PhaseStepper";
import { DeferRateRing } from "../components/DeferRateRing";

export function DashboardPage() {
  const [exams, setExams] = useState<ExamSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .listExams()
      .then(setExams)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <header className="mb-8">
        <p className="m3-label-small m-0 mb-1">SCALES v3.0</p>
        <h1 className="m3-display-large m-0" style={{ fontSize: "2.75rem" }}>
          Exams
        </h1>
        <p className="m3-body-large mt-2">
          Teacher review dashboard — skim health, then clear the defer queue.
        </p>
      </header>

      {loading && <p className="m3-body-large">Loading exams…</p>}
      {error && (
        <p className="m3-body-large" style={{ color: "var(--md-sys-color-error)" }}>
          {error}
        </p>
      )}

      <div className="grid gap-4">
        {exams.map((exam) => (
          <article key={exam.exam_id} className="m3-card p-5 flex flex-wrap gap-4 items-center">
            <div className="flex-1 min-w-[220px]">
              <h2 className="m3-title-large m-0">{exam.exam_id}</h2>
              <p className="m3-body-small m-0 mt-1">{exam.subject || "—"}</p>
              <div className="mt-3">
                <PhaseStepper phase={exam.phase} />
              </div>
              <p className="m3-body-small mt-3">
                Graded {exam.graded_count}/{exam.total_students} · Deferred{" "}
                {exam.deferred_count} · Corrections {exam.corrections_count}
              </p>
            </div>
            <DeferRateRing rate={exam.defer_rate} />
            <div className="flex flex-col gap-2">
              {exam.phase === "awaiting_review" && (
                <Link
                  to={`/exams/${encodeURIComponent(exam.exam_id)}/review`}
                  className="no-underline text-center px-5 py-3"
                  style={{
                    background: "var(--md-sys-color-primary)",
                    color: "var(--md-sys-color-on-primary)",
                    borderRadius: "var(--md-sys-shape-corner-full)",
                    fontWeight: 600,
                  }}
                >
                  Start review
                </Link>
              )}
              <Link
                to={`/exams/${encodeURIComponent(exam.exam_id)}/results`}
                className="no-underline text-center px-5 py-2"
                style={{
                  background: "var(--md-sys-color-secondary-container)",
                  color: "var(--md-sys-color-on-secondary-container)",
                  borderRadius: "var(--md-sys-shape-corner-full)",
                }}
              >
                Results
              </Link>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
