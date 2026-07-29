import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import { SegmentedButtons } from "../components/SegmentedButtons";
import type { CalibrateConcept, CalibratePayload, CalibrateRubric } from "../types";

type ReqOpt = "required" | "optional";

function toReqOpt(required: boolean): ReqOpt {
  return required ? "required" : "optional";
}

function cloneRubrics(rubrics: CalibrateRubric[]): CalibrateRubric[] {
  return rubrics.map((r) => ({
    ...r,
    concepts: r.concepts.map((c) => ({ ...c })),
  }));
}

function toBody(rubrics: CalibrateRubric[]) {
  return {
    rubrics: rubrics.map((r) => ({
      rubric_item_id: r.rubric_item_id,
      required_for_full_marks: r.required_for_full_marks,
      concepts: r.concepts.map((c) => ({
        concept_id: c.concept_id,
        needed_for_rubric: c.needed_for_rubric,
        partial_credit_note: c.partial_credit_note,
        matching_note: c.matching_note,
      })),
    })),
  };
}

export function CalibratePage() {
  const { examId = "" } = useParams();
  const [data, setData] = useState<CalibratePayload | null>(null);
  const [rubrics, setRubrics] = useState<CalibrateRubric[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState<string | null>(null);
  const [openRubrics, setOpenRubrics] = useState<Set<string>>(new Set());

  useEffect(() => {
    setLoading(true);
    setError(null);
    api
      .getCalibrate(examId)
      .then((d) => {
        setData(d);
        setRubrics(cloneRubrics(d.rubrics));
        setOpenRubrics(new Set(d.rubrics.map((r) => r.rubric_item_id)));
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [examId]);

  const requiredMarks = useMemo(
    () =>
      rubrics
        .filter((r) => r.required_for_full_marks)
        .reduce((s, r) => s + r.marks, 0),
    [rubrics],
  );

  const totalMarks = data?.question.total_marks ?? 0;

  function toggleOpen(id: string) {
    setOpenRubrics((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function setRubricRequired(rid: string, value: ReqOpt) {
    setRubrics((prev) =>
      prev.map((r) =>
        r.rubric_item_id === rid
          ? { ...r, required_for_full_marks: value === "required" }
          : r,
      ),
    );
    setSaveMsg(null);
  }

  function patchConcept(
    rid: string,
    cid: string,
    patch: Partial<CalibrateConcept>,
  ) {
    setRubrics((prev) =>
      prev.map((r) =>
        r.rubric_item_id !== rid
          ? r
          : {
              ...r,
              concepts: r.concepts.map((c) =>
                c.concept_id === cid ? { ...c, ...patch } : c,
              ),
            },
      ),
    );
    setSaveMsg(null);
  }

  async function onSave() {
    setSaving(true);
    setError(null);
    setSaveMsg(null);
    try {
      const next = await api.putCalibrate(examId, toBody(rubrics));
      setData(next);
      setRubrics(cloneRubrics(next.rubrics));
      setSaveMsg(
        next.updated_at
          ? `Saved · ${new Date(next.updated_at).toLocaleString()}`
          : "Saved",
      );
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="shell">
      <Link to="/" className="m3-btn-text" style={{ paddingLeft: 0 }}>
        ← Question papers
      </Link>
      <h1 className="m3-headline-large m-0 mt-2">Calibrate marking policy</h1>
      {data?.paper_title && (
        <p className="m3-title-medium m-0 mt-1">{data.paper_title}</p>
      )}
      <p className="m3-body-small" style={{ wordBreak: "break-all" }}>
        {data?.question_key ? `${data.question_key} · ` : ""}
        {examId}
      </p>
      <p className="m3-body-large mt-2 max-w-2xl" style={{ opacity: 0.85 }}>
        Rubric lines are the teacher mark buckets. Concepts under each line are
        what CERA extracted — often several per line. Mark a{" "}
        <strong>rubric line</strong> required/optional for full marks on the
        question; when a line has multiple concepts, say which ones are needed
        to earn that line.
      </p>

      {data?.siblings && data.siblings.length > 1 && (
        <div className="mt-5 flex flex-wrap gap-2" role="navigation" aria-label="Questions on this paper">
          {data.siblings.map((s) => {
            const active = s.exam_id === examId;
            return (
              <Link
                key={s.exam_id}
                to={`/exams/${encodeURIComponent(s.exam_id)}/calibrate`}
                className={active ? "m3-fab no-underline" : "m3-btn-tonal no-underline"}
                style={{
                  opacity: active ? 1 : 0.9,
                }}
              >
                {s.question_label}
                {s.calibrated ? " ✓" : ""}
              </Link>
            );
          })}
        </div>
      )}

      {loading && <p className="m3-body-large">Loading calibrate…</p>}
      {error && (
        <p className="m3-body-large" style={{ color: "var(--md-sys-color-error)" }}>
          {error}
        </p>
      )}

      {data && (
        <>
          <section className="m3-surface p-6 md:p-7 mt-6">
            <p className="m3-label-small m-0">
              {data.question.question_id} · {data.question.total_marks} marks
            </p>
            <p className="m3-title-large m-0 mt-1">
              {data.question.question_text}
            </p>
          </section>

          <section className="m3-surface p-6 md:p-7 mt-4">
            <p className="m3-label-small m-0 mb-2">Reference answer</p>
            <p
              className="m3-body-large m-0 whitespace-pre-wrap"
              style={{ lineHeight: 1.55 }}
            >
              {data.question.reference_answer}
            </p>
          </section>

          <p className="m3-label-small m-0 mt-8 mb-3">
            Rubric items → concepts · required lines sum to {requiredMarks} /{" "}
            {totalMarks} marks
          </p>

          <div className="flex flex-col gap-4">
            {rubrics.map((r) => {
              const open = openRubrics.has(r.rubric_item_id);
              return (
                <article key={r.rubric_item_id} className="m3-surface p-5 md:p-6">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <button
                      type="button"
                      className="m3-btn-text text-left"
                      style={{ paddingLeft: 0 }}
                      onClick={() => toggleOpen(r.rubric_item_id)}
                      aria-expanded={open}
                    >
                      <span className="m3-label-small block">
                        {r.rubric_item_id}
                        {r.synthetic ? " · synthetic" : ""}
                        {r.atomic
                          ? " · atomic (1 concept)"
                          : ` · ${r.concepts.length} concepts`}
                      </span>
                      <span className="m3-title-large block mt-1">
                        {open ? "▾ " : "▸ "}
                        {r.label}{" "}
                        <span className="m3-body-large" style={{ opacity: 0.7 }}>
                          ({r.marks} marks)
                        </span>
                      </span>
                    </button>
                    <div>
                      <p className="m3-label-small m-0 mb-2">
                        For full marks on this question
                      </p>
                      <SegmentedButtons
                        ariaLabel={`${r.label} required for full marks`}
                        value={toReqOpt(r.required_for_full_marks)}
                        onChange={(v) => setRubricRequired(r.rubric_item_id, v)}
                        options={[
                          { value: "required", label: "Required" },
                          { value: "optional", label: "Optional" },
                        ]}
                      />
                    </div>
                  </div>

                  {open && (
                    <ul className="list-none p-0 m-0 mt-5 flex flex-col gap-4">
                      {r.concepts.length === 0 && (
                        <li className="m3-body-large" style={{ opacity: 0.7 }}>
                          No concepts under this rubric yet.
                        </li>
                      )}
                      {r.concepts.length > 1 && (
                        <li className="m3-body-small m-0" style={{ opacity: 0.75 }}>
                          {r.concepts.length} concepts under this rubric line
                          (sum {r.concepts.reduce((s, c) => s + c.marks, 0)} marks)
                        </li>
                      )}
                      {r.concepts.map((c) => {
                        const multi = r.concepts.length > 1;
                        return (
                        <li
                          key={c.concept_id}
                          className="p-4"
                          style={{
                            background:
                              "var(--md-sys-color-surface-container-high)",
                            borderRadius: "var(--md-sys-shape-corner-large)",
                          }}
                        >
                          <p className="m3-label-small m-0">
                            Concept · {c.concept_id}
                          </p>
                          <p className="m3-title-medium m-0 mt-1">
                            {c.knowledge_point}{" "}
                            <span style={{ opacity: 0.7 }}>
                              ({c.marks} marks)
                            </span>
                          </p>
                          {c.target_criteria && (
                            <p className="m3-body-small mt-2 mb-0">
                              Criteria: {c.target_criteria}
                            </p>
                          )}
                          {c.evidence_facets.length > 0 && (
                            <p className="m3-body-small mt-1 mb-0">
                              Facets ({c.evidence_role || c.evidence_mode}
                              {c.min_count != null ? ` · n≥${c.min_count}` : ""}):{" "}
                              {c.evidence_facets.join(" · ")}
                            </p>
                          )}

                          {multi && (
                            <div className="mt-4">
                              <p className="m3-label-small m-0 mb-2">
                                Needed to earn this rubric line&apos;s marks?
                              </p>
                              <SegmentedButtons
                                ariaLabel={`${c.concept_id} needed for rubric`}
                                value={toReqOpt(c.needed_for_rubric)}
                                onChange={(v) =>
                                  patchConcept(r.rubric_item_id, c.concept_id, {
                                    needed_for_rubric: v === "required",
                                  })
                                }
                                options={[
                                  { value: "required", label: "Needed" },
                                  { value: "optional", label: "Optional" },
                                ]}
                              />
                            </div>
                          )}

                          <label className="block mt-4">
                            <span className="m3-label-small">
                              Partial credit note
                            </span>
                            <textarea
                              className="block w-full mt-1 p-3 m3-body-medium border-0"
                              style={{
                                background:
                                  "var(--md-sys-color-surface-container-lowest)",
                                borderRadius:
                                  "var(--md-sys-shape-corner-medium)",
                                minHeight: 64,
                                resize: "vertical",
                              }}
                              value={c.partial_credit_note}
                              onChange={(e) =>
                                patchConcept(r.rubric_item_id, c.concept_id, {
                                  partial_credit_note: e.target.value,
                                })
                              }
                              placeholder="What should count as partial for this concept?"
                            />
                          </label>

                          <label className="block mt-3">
                            <span className="m3-label-small">
                              Matching note (for later CGR fix — not scoring)
                            </span>
                            <textarea
                              className="block w-full mt-1 p-3 m3-body-medium border-0"
                              style={{
                                background:
                                  "var(--md-sys-color-surface-container-lowest)",
                                borderRadius:
                                  "var(--md-sys-shape-corner-medium)",
                                minHeight: 56,
                                resize: "vertical",
                              }}
                              value={c.matching_note}
                              onChange={(e) =>
                                patchConcept(r.rubric_item_id, c.concept_id, {
                                  matching_note: e.target.value,
                                })
                              }
                              placeholder="e.g. students say 'slower throughput' for 'low transmission rate'"
                            />
                          </label>
                        </li>
                        );
                      })}
                    </ul>
                  )}
                </article>
              );
            })}
          </div>

          <footer className="mt-8 flex flex-wrap items-center gap-4">
            <button
              type="button"
              className="m3-fab"
              disabled={saving}
              onClick={() => void onSave()}
            >
              {saving ? "Saving…" : "Save policy"}
            </button>
            {saveMsg && <span className="m3-body-medium">{saveMsg}</span>}
            {!saveMsg && data.saved && data.updated_at && (
              <span className="m3-body-small" style={{ opacity: 0.75 }}>
                Last saved {new Date(data.updated_at).toLocaleString()}
              </span>
            )}
            <Link
              to={`/exams/${encodeURIComponent(examId)}/explain`}
              className="m3-btn-text"
            >
              Why these marks
            </Link>
          </footer>
        </>
      )}
    </div>
  );
}
