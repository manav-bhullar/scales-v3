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

  const awaiting = exams.filter((e) => e.phase === "awaiting_review");
  const totalDeferred = awaiting.reduce((n, e) => n + e.deferred_count, 0);

  return (
    <div className="shell">
      <header className="mb-10">
        <p
          className="m3-display-large m-0"
          style={{ color: "var(--md-sys-color-primary)" }}
        >
          SCALES
        </p>
        <p className="m3-headline-medium m-0 mt-2" style={{ fontWeight: 500 }}>
          Teacher review
        </p>
        <p className="m3-body-large mt-3 max-w-xl" style={{ opacity: 0.85 }}>
          Clear deferred concepts the system couldn&apos;t trust — one judgment at
          a time, with every CBTE signal visible.
        </p>
        {!loading && awaiting.length > 0 && (
          <p
            className="m3-title-large mt-6 mb-0 inline-flex items-center gap-2 px-4 py-2"
            style={{
              background: "var(--md-sys-color-tertiary-container)",
              color: "var(--md-sys-color-on-tertiary-container)",
              borderRadius: "var(--md-sys-shape-corner-full)",
            }}
          >
            {totalDeferred} waiting in queue
          </p>
        )}
      </header>

      {loading && <p className="m3-body-large">Loading exams…</p>}
      {error && (
        <p className="m3-body-large" style={{ color: "var(--md-sys-color-error)" }}>
          {error}
          <span className="m3-body-small block mt-1">
            Is the API running on port 8000?
          </span>
        </p>
      )}

      {!loading && !error && exams.length === 0 && (
        <div className="m3-surface p-8">
          <h2 className="m3-headline-medium m-0">No exams yet</h2>
          <p className="m3-body-large mt-2 mb-0">
            Grade an exam from the CLI first, then refresh this page to review
            deferred items.
          </p>
        </div>
      )}

      <div className="grid gap-5">
        {exams.map((exam, i) => {
          const needsReview = exam.phase === "awaiting_review";
          return (
            <article
              key={exam.exam_id}
              className="m3-surface p-6 md:p-7 flex flex-wrap gap-6 items-center"
              style={{
                animation: `card-enter var(--md-sys-motion-duration-long) var(--md-sys-motion-easing-spring) ${i * 60}ms both`,
                outline: needsReview
                  ? "2px solid color-mix(in srgb, var(--md-sys-color-tertiary) 35%, transparent)"
                  : undefined,
              }}
            >
              <div className="flex-1 min-w-[240px]">
                <p className="m3-label-small m-0 mb-1">
                  {exam.subject || "Exam"} · {exam.phase.replaceAll("_", " ")}
                </p>
                <h2 className="m3-title-large m-0" style={{ wordBreak: "break-word" }}>
                  {exam.exam_id}
                </h2>
                <div className="mt-4">
                  <PhaseStepper phase={exam.phase} />
                </div>
                <p className="m3-body-small mt-4 mb-0">
                  Graded {exam.graded_count}/{exam.total_students}
                  {" · "}Deferred {exam.deferred_count}
                  {" · "}Corrections {exam.corrections_count}
                </p>
              </div>

              <div className="flex flex-col items-center gap-1">
                <DeferRateRing rate={exam.defer_rate} />
                <span className="m3-label-small">Defer rate</span>
              </div>

              <div className="flex flex-col gap-2 min-w-[160px]">
                {needsReview ? (
                  <Link
                    to={`/exams/${encodeURIComponent(exam.exam_id)}/review`}
                    className="m3-fab no-underline text-center"
                  >
                    Resolve DEFERs
                  </Link>
                ) : (
                  <span
                    className="text-center px-4 py-3 m3-body-small"
                    style={{
                      borderRadius: "var(--md-sys-shape-corner-full)",
                      background: "var(--md-sys-color-surface-container-high)",
                    }}
                  >
                    {exam.phase === "complete" ? "Review done" : "No queue"}
                  </span>
                )}
                <Link
                  to={`/exams/${encodeURIComponent(exam.exam_id)}/explain`}
                  className="m3-btn-tonal text-center"
                >
                  Why these marks
                </Link>
                <Link
                  to={`/exams/${encodeURIComponent(exam.exam_id)}/results`}
                  className="m3-btn-text text-center"
                >
                  Results
                </Link>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
