import { useMemo, useState } from "react";
import type { ReviewItem, Verdict } from "../types";
import { highlightEvidence } from "../lib/evidenceHighlight";
import { TonalChip } from "./TonalChip";
import { TrustArc } from "./TrustArc";
import { SegmentedButtons } from "./SegmentedButtons";

export function QueueCard({
  item,
  exiting,
  onAgree,
  onCorrect,
  onExplain,
}: {
  item: ReviewItem;
  exiting: boolean;
  onAgree: () => void;
  onCorrect: (verdict: Verdict, marks: number, comment: string) => void;
  onExplain: () => void;
}) {
  const [editing, setEditing] = useState(false);
  const [verdict, setVerdict] = useState<Verdict>(item.system_verdict);
  const [marks, setMarks] = useState(item.system_marks);
  const [comment, setComment] = useState("");

  const highlighted = useMemo(
    () => highlightEvidence(item.student_answer, item.evidence_span),
    [item.student_answer, item.evidence_span],
  );

  const markOptions = useMemo(() => {
    const full = item.max_marks;
    const half = full * 0.5;
    return [
      { value: 0, label: "0" },
      { value: half, label: String(half) },
      { value: full, label: String(full) },
    ];
  }, [item.max_marks]);

  const onVerdictChange = (v: Verdict) => {
    setVerdict(v);
    if (v === "FULL") setMarks(item.max_marks);
    else if (v === "PARTIAL") setMarks(item.max_marks * 0.5);
    else setMarks(0);
  };

  return (
    <article
      className={`m3-card p-6 ${exiting ? "m3-card-exit" : "m3-card-enter"}`}
      aria-label={`Review ${item.student_id} ${item.concept_id}`}
    >
      <header className="flex flex-wrap items-start justify-between gap-4 mb-4">
        <div>
          <p className="m3-label-small m-0 mb-1">
            {item.student_id} · {item.concept_id}
          </p>
          <h2 className="m3-headline-medium m-0">{item.knowledge_point}</h2>
        </div>
        <div className="flex items-center gap-3">
          <TonalChip verdict={item.system_verdict} />
          <TrustArc score={item.trust_score} />
        </div>
      </header>

      <p className="m3-body-small mb-2">
        System: {item.system_marks}/{item.max_marks} · {item.defer_reason || "Deferred for review"}
      </p>

      <section
        className="p-4 mb-4"
        style={{
          background: "var(--md-sys-color-surface-container-low)",
          borderRadius: "var(--md-sys-shape-corner-medium)",
        }}
      >
        <p className="m3-label-small m-0 mb-2">Student answer</p>
        <p className="m3-body-large m-0 whitespace-pre-wrap">
          {highlighted ? (
            <>
              {highlighted.before}
              <mark className="evidence-mark">{highlighted.match}</mark>
              {highlighted.after}
            </>
          ) : (
            item.student_answer || "(empty)"
          )}
        </p>
        {item.evidence_span && !highlighted && (
          <p className="m3-body-small mt-2">
            Quoted evidence (not located inline): “{item.evidence_span}”
          </p>
        )}
      </section>

      <details className="mb-4">
        <summary className="cursor-pointer m3-body-small">Reasoning</summary>
        <p className="m3-body-small mt-2 whitespace-pre-wrap">{item.reasoning}</p>
      </details>

      {!editing ? (
        <div className="flex flex-wrap gap-3 items-center">
          <button
            type="button"
            className="border-0 cursor-pointer px-6 py-3 m3-title-large"
            style={{
              background: "var(--md-sys-color-primary)",
              color: "var(--md-sys-color-on-primary)",
              borderRadius: "var(--md-sys-shape-corner-full)",
            }}
            onClick={onAgree}
          >
            Agree
          </button>
          <button
            type="button"
            className="border-0 cursor-pointer px-5 py-3"
            style={{
              background: "var(--md-sys-color-secondary-container)",
              color: "var(--md-sys-color-on-secondary-container)",
              borderRadius: "var(--md-sys-shape-corner-full)",
            }}
            onClick={() => setEditing(true)}
          >
            Correct
          </button>
          <button
            type="button"
            className="border-0 cursor-pointer px-4 py-2 ml-auto"
            style={{
              background: "transparent",
              color: "var(--md-sys-color-primary)",
              borderRadius: "var(--md-sys-shape-corner-full)",
            }}
            onClick={onExplain}
          >
            Explain
          </button>
        </div>
      ) : (
        <div
          className="p-4 flex flex-col gap-3"
          style={{
            background: "var(--md-sys-color-surface-container)",
            borderRadius: "var(--md-sys-shape-corner-medium)",
          }}
        >
          <SegmentedButtons
            ariaLabel="Teacher verdict"
            options={[
              { value: "FULL" as Verdict, label: "Full" },
              { value: "PARTIAL" as Verdict, label: "Partial" },
              { value: "ABSENT" as Verdict, label: "Absent" },
              { value: "INCORRECT" as Verdict, label: "Incorrect" },
            ]}
            value={verdict}
            onChange={onVerdictChange}
          />
          <SegmentedButtons
            ariaLabel="Marks"
            options={markOptions}
            value={marks}
            onChange={setMarks}
          />
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Optional comment"
            rows={2}
            className="w-full p-3 border-0 m3-body-large"
            style={{
              borderRadius: "var(--md-sys-shape-corner-small)",
              background: "var(--md-sys-color-surface-container-lowest)",
            }}
          />
          <div className="flex gap-2">
            <button
              type="button"
              className="border-0 cursor-pointer px-5 py-2"
              style={{
                background: "var(--md-sys-color-primary)",
                color: "var(--md-sys-color-on-primary)",
                borderRadius: "var(--md-sys-shape-corner-full)",
              }}
              onClick={() => onCorrect(verdict, marks, comment)}
            >
              Submit correction
            </button>
            <button
              type="button"
              className="border-0 cursor-pointer px-4 py-2"
              style={{
                background: "var(--md-sys-color-surface-container-high)",
                borderRadius: "var(--md-sys-shape-corner-full)",
              }}
              onClick={() => setEditing(false)}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </article>
  );
}
