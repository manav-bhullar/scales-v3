import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import type { FinalResult } from "../types";
import { TonalChip } from "../components/TonalChip";

type SortKey = "score" | "deferred";

export function ResultsPage() {
  const { examId = "" } = useParams();
  const [results, setResults] = useState<FinalResult[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [sortKey, setSortKey] = useState<SortKey>("score");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getResults(examId)
      .then((rows) => {
        setResults(rows);
        if (rows.length) setSelected(rows[0].student_id);
      })
      .catch((e: Error) => setError(e.message));
  }, [examId]);

  const sorted = useMemo(() => {
    const copy = [...results];
    if (sortKey === "score") {
      copy.sort((a, b) => b.final_score - a.final_score);
    } else {
      copy.sort(
        (a, b) =>
          Number(b.has_deferred_concepts) - Number(a.has_deferred_concepts),
      );
    }
    return copy;
  }, [results, sortKey]);

  const detail = results.find((r) => r.student_id === selected) ?? null;

  return (
    <div className="shell">
      <Link to="/" className="m3-btn-text" style={{ paddingLeft: 0 }}>
        ← Exams
      </Link>
      <h1 className="m3-headline-large m-0 mt-2">Results</h1>
      <p className="m3-body-small" style={{ wordBreak: "break-all" }}>
        {examId}
      </p>

      {error && (
        <p className="m3-body-large" style={{ color: "var(--md-sys-color-error)" }}>
          {error}
        </p>
      )}

      {!error && results.length === 0 && (
        <div className="m3-surface p-8 mt-6">
          <h2 className="m3-headline-medium m-0">No finals yet</h2>
          <p className="m3-body-large mt-2 mb-0">
            Resolve the DEFER queue and finalize first.
          </p>
          <div className="flex gap-3 mt-5 flex-wrap">
            <Link
              to={`/exams/${encodeURIComponent(examId)}/review`}
              className="m3-fab no-underline inline-flex"
            >
              Open review
            </Link>
            <Link
              to={`/exams/${encodeURIComponent(examId)}/explain`}
              className="m3-btn-tonal no-underline inline-flex"
            >
              See why these marks
            </Link>
          </div>
        </div>
      )}

      {results.length > 0 && (
        <div className="results-grid mt-8">
          <section className="m3-surface p-5">
            <div className="flex gap-2 mb-4 flex-wrap">
              {(
                [
                  ["score", "By score"],
                  ["deferred", "By deferred"],
                ] as const
              ).map(([key, label]) => (
                <button
                  key={key}
                  type="button"
                  className="border-0 cursor-pointer px-4 py-2"
                  style={{
                    borderRadius: "var(--md-sys-shape-corner-full)",
                    fontWeight: 600,
                    background:
                      sortKey === key
                        ? "var(--md-sys-color-secondary-container)"
                        : "var(--md-sys-color-surface-container-high)",
                    color:
                      sortKey === key
                        ? "var(--md-sys-color-on-secondary-container)"
                        : "var(--md-sys-color-on-surface)",
                  }}
                  onClick={() => setSortKey(key)}
                >
                  {label}
                </button>
              ))}
            </div>
            <ul className="list-none m-0 p-0 flex flex-col gap-2">
              {sorted.map((r) => {
                const active = selected === r.student_id;
                return (
                  <li key={r.student_id}>
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
                      onClick={() => setSelected(r.student_id)}
                    >
                      <span className="m3-title-large block">{r.student_id}</span>
                      <span className="m3-body-small">
                        {r.final_score}/{r.total_marks}
                        {" · trust "}
                        {r.overall_trust.toFixed(2)}
                        {r.has_deferred_concepts ? " · had DEFER" : ""}
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
                {detail.final_score}
                <span className="m3-title-large"> / {detail.total_marks}</span>
              </p>
              <p className="m3-body-small mt-2">
                Overall trust {detail.overall_trust.toFixed(2)} ·{" "}
                {detail.all_concepts_resolved ? "All concepts resolved" : "Unresolved remain"}
              </p>
              <ul className="list-none p-0 m-0 mt-6 flex flex-col gap-3">
                {detail.concept_results.map((c) => (
                  <li
                    key={c.concept_id}
                    className="p-4"
                    style={{
                      background: "var(--md-sys-color-surface-container-low)",
                      borderRadius: "var(--md-sys-shape-corner-large)",
                    }}
                  >
                    <div className="flex items-center justify-between gap-2 flex-wrap">
                      <strong className="m3-body-large">{c.concept_id}</strong>
                      <div className="flex items-center gap-2">
                        <TonalChip verdict={c.verdict} />
                        <span
                          className="m3-label-small px-2 py-1"
                          style={{
                            borderRadius: "var(--md-sys-shape-corner-full)",
                            background:
                              c.reviewed_by === "teacher"
                                ? "var(--md-sys-color-tertiary-container)"
                                : "var(--md-sys-color-surface-container-highest)",
                            color:
                              c.reviewed_by === "teacher"
                                ? "var(--md-sys-color-on-tertiary-container)"
                                : undefined,
                          }}
                        >
                          {c.reviewed_by === "teacher" ? "Teacher" : "Auto"}
                        </span>
                      </div>
                    </div>
                    <p className="m3-body-small m-0 mt-2">{c.knowledge_point}</p>
                    <p className="m3-body-small m-0">
                      {c.marks_awarded}/{c.max_marks} · trust {c.trust_score.toFixed(2)}
                    </p>
                    {c.teacher_comment && (
                      <p className="m3-body-small m-0 mt-2">
                        Comment: {c.teacher_comment}
                      </p>
                    )}
                  </li>
                ))}
              </ul>
            </section>
          )}
        </div>
      )}
    </div>
  );
}
