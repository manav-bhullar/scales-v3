import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import type { ExamSummary, PaperSummary } from "../types";
import { PhaseStepper } from "../components/PhaseStepper";
import { DeferRateRing } from "../components/DeferRateRing";

export function DashboardPage() {
  const [papers, setPapers] = useState<PaperSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .listPapers()
      .then(setPapers)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const allQuestions = papers.flatMap((p) => p.questions);
  const awaiting = allQuestions.filter((e) => e.phase === "awaiting_review");
  const totalDeferred = papers.reduce((n, p) => n + p.deferred_count, 0);

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
          Question papers
        </p>
        <p className="m3-body-large mt-3 max-w-xl" style={{ opacity: 0.85 }}>
          Papers group their questions. Calibrate marking policy per question,
          then review deferred judgments.
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

      {loading && <p className="m3-body-large">Loading papers…</p>}
      {error && (
        <p className="m3-body-large" style={{ color: "var(--md-sys-color-error)" }}>
          {error}
          <span className="m3-body-small block mt-1">
            Is the API running on port 8000?
          </span>
        </p>
      )}

      {!loading && !error && papers.length === 0 && (
        <div className="m3-surface p-8">
          <h2 className="m3-headline-medium m-0">No question papers yet</h2>
          <p className="m3-body-large mt-2 mb-0">
            Grade an exam from the CLI first, then refresh this page.
          </p>
        </div>
      )}

      <div className="grid gap-8">
        {papers.map((paper, pi) => (
          <section key={paper.paper_id}>
            <div className="flex flex-wrap items-end justify-between gap-3 mb-4">
              <div>
                <p className="m3-label-small m-0">Question paper</p>
                <h2 className="m3-headline-medium m-0">{paper.paper_title}</h2>
                <p className="m3-body-small mt-1 mb-0">
                  {paper.question_count} questions
                  {" · "}
                  {paper.calibrated_count}/{paper.question_count} calibrated
                  {paper.deferred_count > 0
                    ? ` · ${paper.deferred_count} deferred`
                    : ""}
                </p>
              </div>
              {paper.questions[0] && (
                <Link
                  to={`/exams/${encodeURIComponent(paper.questions[0].exam_id)}/calibrate`}
                  className="m3-fab no-underline text-center"
                >
                  Calibrate paper
                </Link>
              )}
            </div>

            <div className="grid gap-4">
              {paper.questions.map((exam, i) => (
                <QuestionCard
                  key={exam.exam_id}
                  exam={exam}
                  delayMs={(pi * 40) + i * 50}
                />
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}

function QuestionCard({
  exam,
  delayMs,
}: {
  exam: ExamSummary;
  delayMs: number;
}) {
  const needsReview = exam.phase === "awaiting_review";
  return (
    <article
      className="m3-surface p-5 md:p-6 flex flex-wrap gap-5 items-center"
      style={{
        animation: `card-enter var(--md-sys-motion-duration-long) var(--md-sys-motion-easing-spring) ${delayMs}ms both`,
        outline: needsReview
          ? "2px solid color-mix(in srgb, var(--md-sys-color-tertiary) 35%, transparent)"
          : undefined,
      }}
    >
      <div className="flex-1 min-w-[220px]">
        <p className="m3-label-small m-0 mb-1">
          {exam.question_key}
          {exam.calibrated ? " · calibrated" : " · not calibrated"}
          {" · "}
          {exam.phase.replaceAll("_", " ")}
        </p>
        <h3 className="m3-title-large m-0">
          {exam.question_preview || exam.question_label}
          {exam.total_marks ? (
            <span className="m3-body-large" style={{ opacity: 0.7 }}>
              {" "}
              ({exam.total_marks} marks)
            </span>
          ) : null}
        </h3>
        <p
          className="m3-body-small mt-2 mb-0"
          style={{ opacity: 0.65, wordBreak: "break-all" }}
        >
          {exam.exam_id}
        </p>
        <div className="mt-3">
          <PhaseStepper phase={exam.phase} />
        </div>
        <p className="m3-body-small mt-3 mb-0">
          Graded {exam.graded_count}/{exam.total_students}
          {" · "}Deferred {exam.deferred_count}
          {" · "}Corrections {exam.corrections_count}
        </p>
      </div>

      <div className="flex flex-col items-center gap-1">
        <DeferRateRing rate={exam.defer_rate} />
        <span className="m3-label-small">Defer rate</span>
      </div>

      <div className="flex flex-col gap-2 min-w-[150px]">
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
          to={`/exams/${encodeURIComponent(exam.exam_id)}/calibrate`}
          className="m3-btn-tonal text-center"
        >
          Calibrate
        </Link>
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
}
