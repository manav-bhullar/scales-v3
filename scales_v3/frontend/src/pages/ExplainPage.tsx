import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import type { BreakdownPayload, StudentExplain } from "../types";
import { ConceptExplainCard } from "../components/ConceptExplainCard";

type Filter = "all" | "deferred" | "silent_zero" | "low";

const FILTERS: [Filter, string][] = [
  ["all", "All students"],
  ["deferred", "Waiting on me"],
  ["silent_zero", "Zeros never checked"],
  ["low", "Lowest scores"],
];

function silentZeros(s: StudentExplain): number {
  return s.concepts.filter(
    (c) =>
      (c.teacher_marks ?? c.marks_awarded) === 0 &&
      c.decision === "ACCEPT" &&
      c.source === "auto",
  ).length;
}

export function ExplainPage() {
  const { examId = "" } = useParams();
  const [data, setData] = useState<BreakdownPayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<string | null>(null);
  const [filter, setFilter] = useState<Filter>("all");
  const [openConcepts, setOpenConcepts] = useState<Set<string>>(new Set());

  useEffect(() => {
    api
      .getBreakdown(examId)
      .then((d) => {
        setData(d);
        if (d.students.length) setSelected(d.students[0].student_id);
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [examId]);

  const students = data?.students ?? [];

  /** Cohort-level rubric health: a concept nobody earns is usually mis-specified,
   *  not universally missed. Surfacing it here is how you tell a strictness
   *  problem from a student-knowledge problem. */
  const rubricHealth = useMemo(() => {
    if (!data) return [];
    const n = students.length || 1;
    return data.concepts.map((rc) => {
      const zero = students.filter((s) => {
        const c = s.concepts.find((x) => x.concept_id === rc.concept_id);
        return c ? (c.teacher_marks ?? c.marks_awarded) === 0 : false;
      }).length;
      return {
        ...rc,
        zeroCount: zero,
        zeroRate: zero / n,
        earnRate: 1 - zero / n,
      };
    });
  }, [data, students]);

  const visible = useMemo(() => {
    const copy = [...students];
    if (filter === "deferred")
      return copy.filter((s) => s.deferred_count > 0);
    if (filter === "silent_zero")
      return copy
        .filter((s) => silentZeros(s) > 0)
        .sort((a, b) => silentZeros(b) - silentZeros(a));
    if (filter === "low")
      return copy.sort((a, b) => a.current_score - b.current_score);
    return copy;
  }, [students, filter]);

  const detail = students.find((s) => s.student_id === selected) ?? null;

  function toggleConcept(id: string) {
    setOpenConcepts((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  return (
    <div className="shell">
      <Link to="/" className="m3-btn-text" style={{ paddingLeft: 0 }}>
        ← Exams
      </Link>
      <h1 className="m3-headline-large m-0 mt-2">Why these marks</h1>
      <p className="m3-body-small" style={{ wordBreak: "break-all" }}>
        {examId}
      </p>

      {loading && <p className="m3-body-large">Loading breakdown…</p>}
      {error && (
        <p className="m3-body-large" style={{ color: "var(--md-sys-color-error)" }}>
          {error}
          <span className="m3-body-small block mt-1">
            Is the API running on port 8000, and has this exam been graded?
          </span>
        </p>
      )}

      {data && (
        <>
          <section className="m3-surface p-6 md:p-7 mt-6">
            <p className="m3-label-small m-0">
              {data.question.question_id} · {data.question.total_marks} marks ·{" "}
              {students.length} students
            </p>
            <p className="m3-title-large m-0 mt-1">
              {data.question.question_text}
            </p>

            <p className="m3-label-small m-0 mt-6 mb-3">
              Rubric health — how many students earned each concept
            </p>
            <ul className="list-none p-0 m-0 flex flex-col gap-3">
              {rubricHealth.map((rc) => {
                const dead = rc.zeroRate >= 0.8;
                return (
                  <li key={rc.concept_id} className="flex items-center gap-3 flex-wrap">
                    <span
                      className="m3-body-small"
                      style={{ minWidth: 70, color: "var(--md-sys-color-on-surface)" }}
                    >
                      {rc.concept_id}
                    </span>
                    <div
                      className="flex-1 min-w-[140px] h-2.5 overflow-hidden"
                      style={{
                        background: "var(--md-sys-color-surface-container-highest)",
                        borderRadius: "var(--md-sys-shape-corner-full)",
                      }}
                    >
                      <div
                        className="h-full"
                        style={{
                          width: `${rc.earnRate * 100}%`,
                          background: dead
                            ? "var(--md-sys-color-error)"
                            : "var(--md-sys-color-primary)",
                          borderRadius: "var(--md-sys-shape-corner-full)",
                        }}
                      />
                    </div>
                    <span className="m3-body-small" style={{ minWidth: 150 }}>
                      {students.length - rc.zeroCount}/{students.length} earned ·{" "}
                      {rc.marks} mark{rc.marks === 1 ? "" : "s"}
                    </span>
                    {dead && (
                      <span
                        className="m3-label-small px-2.5 py-1"
                        style={{
                          background: "var(--md-sys-color-error-container)",
                          color: "var(--md-sys-color-on-error-container)",
                          borderRadius: "var(--md-sys-shape-corner-full)",
                          textTransform: "none",
                          letterSpacing: 0,
                        }}
                        title="Almost nobody earns this concept. Either the class genuinely missed it, or the rubric asks for something the question never prompted."
                      >
                        Check this concept
                      </span>
                    )}
                    <span className="m3-body-small w-full" style={{ paddingLeft: 82 }}>
                      {rc.knowledge_point}
                    </span>
                  </li>
                );
              })}
            </ul>
          </section>

          <div className="results-grid mt-6">
            <section className="m3-surface p-5">
              <div className="flex gap-2 mb-4 flex-wrap">
                {FILTERS.map(([key, label]) => (
                  <button
                    key={key}
                    type="button"
                    className="border-0 cursor-pointer px-4 py-2"
                    style={{
                      borderRadius: "var(--md-sys-shape-corner-full)",
                      fontWeight: 600,
                      fontSize: "0.8125rem",
                      background:
                        filter === key
                          ? "var(--md-sys-color-secondary-container)"
                          : "var(--md-sys-color-surface-container-high)",
                      color:
                        filter === key
                          ? "var(--md-sys-color-on-secondary-container)"
                          : "var(--md-sys-color-on-surface)",
                    }}
                    onClick={() => setFilter(key)}
                  >
                    {label}
                  </button>
                ))}
              </div>

              {visible.length === 0 && (
                <p className="m3-body-small m-0">Nothing matches this filter.</p>
              )}

              <ul className="list-none m-0 p-0 flex flex-col gap-2">
                {visible.map((s) => {
                  const active = selected === s.student_id;
                  const sz = silentZeros(s);
                  return (
                    <li key={s.student_id}>
                      <button
                        type="button"
                        className="w-full text-left border-0 cursor-pointer px-4 py-3"
                        style={{
                          borderRadius: "var(--md-sys-shape-corner-large)",
                          background: active
                            ? "var(--md-sys-color-primary-container)"
                            : "var(--md-sys-color-surface-container-low)",
                          color: active
                            ? "var(--md-sys-color-on-primary-container)"
                            : "var(--md-sys-color-on-surface)",
                        }}
                        onClick={() => setSelected(s.student_id)}
                      >
                        <span className="m3-title-large block">
                          {s.student_id}
                        </span>
                        <span className="m3-body-small">
                          {s.current_score}/{s.total_marks}
                          {s.deferred_count > 0 && ` · ${s.deferred_count} waiting`}
                          {sz > 0 && ` · ${sz} unchecked zero${sz === 1 ? "" : "s"}`}
                        </span>
                      </button>
                    </li>
                  );
                })}
              </ul>
            </section>

            {detail && (
              <section className="m3-surface p-6 md:p-8">
                <p className="m3-label-small m-0">{detail.student_id}</p>
                <p className="m3-display-large m-0 mt-1">
                  {detail.current_score}
                  <span className="m3-title-large"> / {detail.total_marks}</span>
                </p>
                <p className="m3-body-small mt-1">
                  {detail.corrected_count > 0
                    ? `${detail.corrected_count} concept(s) set by teacher · machine alone gave ${detail.auto_score}`
                    : "All concepts decided by the machine so far"}
                </p>

                <div
                  className="mt-6 p-5"
                  style={{
                    background: "var(--md-sys-color-surface-container-low)",
                    borderRadius: "var(--md-sys-shape-corner-large)",
                  }}
                >
                  <p className="m3-label-small m-0 mb-2">Student&apos;s answer</p>
                  <p
                    className="m3-body-large m-0"
                    style={{ whiteSpace: "pre-wrap" }}
                  >
                    {detail.answer_text || "(blank)"}
                  </p>
                </div>

                <p className="m3-label-small m-0 mt-7 mb-3">
                  Mark-by-mark breakdown — tap a concept for the reasoning
                </p>
                <ul className="list-none p-0 m-0 flex flex-col gap-3">
                  {detail.concepts.map((c) => (
                    <ConceptExplainCard
                      key={c.concept_id}
                      concept={c}
                      answerText={detail.answer_text}
                      expanded={openConcepts.has(
                        `${detail.student_id}:${c.concept_id}`,
                      )}
                      onToggle={() =>
                        toggleConcept(`${detail.student_id}:${c.concept_id}`)
                      }
                    />
                  ))}
                </ul>

                {detail.deferred_count > 0 && (
                  <Link
                    to={`/exams/${encodeURIComponent(examId)}/review`}
                    className="m3-fab no-underline mt-6 inline-flex"
                  >
                    Resolve {detail.deferred_count} deferred
                  </Link>
                )}
              </section>
            )}
          </div>
        </>
      )}
    </div>
  );
}
