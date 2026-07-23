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
    <div className="max-w-5xl mx-auto px-4 py-8">
      <Link to="/" className="m3-body-small" style={{ color: "var(--md-sys-color-primary)" }}>
        ← Exams
      </Link>
      <h1 className="m3-headline-medium m-0 mt-2">Results</h1>
      <p className="m3-body-small">{examId}</p>

      {error && (
        <p className="m3-body-large" style={{ color: "var(--md-sys-color-error)" }}>
          {error}
        </p>
      )}

      {!error && results.length === 0 && (
        <p className="m3-body-large mt-4">
          No finals yet. Complete the review queue and finalize first.
        </p>
      )}

      {results.length > 0 && (
        <div className="grid gap-6 mt-6" style={{ gridTemplateColumns: "1fr 1.2fr" }}>
          <section className="m3-card p-4">
            <div className="flex gap-2 mb-3">
              <button
                type="button"
                className="border-0 cursor-pointer px-3 py-1"
                style={{
                  borderRadius: "var(--md-sys-shape-corner-full)",
                  background:
                    sortKey === "score"
                      ? "var(--md-sys-color-secondary-container)"
                      : "var(--md-sys-color-surface-container-high)",
                }}
                onClick={() => setSortKey("score")}
              >
                Sort by score
              </button>
              <button
                type="button"
                className="border-0 cursor-pointer px-3 py-1"
                style={{
                  borderRadius: "var(--md-sys-shape-corner-full)",
                  background:
                    sortKey === "deferred"
                      ? "var(--md-sys-color-secondary-container)"
                      : "var(--md-sys-color-surface-container-high)",
                }}
                onClick={() => setSortKey("deferred")}
              >
                Sort by deferred
              </button>
            </div>
            <table className="w-full" style={{ borderCollapse: "collapse" }}>
              <thead>
                <tr className="m3-label-small text-left">
                  <th className="py-2">Student</th>
                  <th>Score</th>
                  <th>Trust</th>
                  <th>Deferred?</th>
                </tr>
              </thead>
              <tbody>
                {sorted.map((r) => (
                  <tr
                    key={r.student_id}
                    className="cursor-pointer"
                    style={{
                      background:
                        selected === r.student_id
                          ? "var(--md-sys-color-primary-container)"
                          : "transparent",
                    }}
                    onClick={() => setSelected(r.student_id)}
                  >
                    <td className="py-2 m3-body-large">{r.student_id}</td>
                    <td className="m3-body-large">
                      {r.final_score}/{r.total_marks}
                    </td>
                    <td className="m3-body-small">{r.overall_trust.toFixed(2)}</td>
                    <td className="m3-body-small">
                      {r.has_deferred_concepts ? "yes" : "no"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          {detail && (
            <section className="m3-card p-5">
              <p className="m3-label-small m-0">{detail.student_id}</p>
              <p className="m3-display-large m-0" style={{ fontSize: "3rem" }}>
                {detail.final_score}
                <span className="m3-title-large"> / {detail.total_marks}</span>
              </p>
              <p className="m3-body-small">
                Overall trust {detail.overall_trust.toFixed(2)} ·{" "}
                {detail.all_concepts_resolved ? "All resolved" : "Unresolved remain"}
              </p>
              <ul className="list-none p-0 m-0 mt-4 flex flex-col gap-3">
                {detail.concept_results.map((c) => (
                  <li
                    key={c.concept_id}
                    className="p-3"
                    style={{
                      background: "var(--md-sys-color-surface-container-low)",
                      borderRadius: "var(--md-sys-shape-corner-small)",
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
                          }}
                          title={
                            c.reviewed_by === "teacher"
                              ? "Teacher corrected"
                              : "Auto-accepted"
                          }
                        >
                          {c.reviewed_by === "teacher" ? "👤 teacher" : "⚡ auto"}
                        </span>
                      </div>
                    </div>
                    <p className="m3-body-small m-0 mt-1">{c.knowledge_point}</p>
                    <p className="m3-body-small m-0">
                      {c.marks_awarded}/{c.max_marks} · trust {c.trust_score.toFixed(2)}
                    </p>
                    {c.teacher_comment && (
                      <p className="m3-body-small m-0 mt-1">Comment: {c.teacher_comment}</p>
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
