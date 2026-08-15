import { useMemo, useState } from "react";
import type { ReviewItem, Verdict } from "../types";
import { highlightEvidence } from "../lib/evidenceHighlight";
import { TonalChip } from "./TonalChip";
import { TrustArc } from "./TrustArc";
import { SegmentedButtons } from "./SegmentedButtons";

export function QueueCard({
  item,
  exiting,
  busy,
  onAgree,
  onCorrect,
  onExplain,
}: {
  item: ReviewItem;
  exiting: boolean;
  busy?: boolean;
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

  const tier = item.signals?.tier_resolved;

  return (
    <article
      className={`m3-surface p-6 md:p-8 ${exiting ? "m3-card-exit" : "m3-card-enter"}`}
      aria-label={`Review ${item.student_id} ${item.concept_id}`}
    >
      <header className="flex flex-wrap items-start justify-between gap-5 mb-6">
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2 mb-2">
            <span
              className="m3-label-small px-3 py-1"
              style={{
                background: "var(--md-sys-color-tertiary-container)",
                color: "var(--md-sys-color-on-tertiary-container)",
                borderRadius: "var(--md-sys-shape-corner-full)",
              }}
            >
              Deferred
            </span>
            {tier != null && (
              <span
                className="m3-label-small px-3 py-1"
                style={{
                  background: "var(--md-sys-color-secondary-container)",
                  color: "var(--md-sys-color-on-secondary-container)",
                  borderRadius: "var(--md-sys-shape-corner-full)",
                }}
              >
                Tier {tier}
              </span>
            )}
          </div>
          <p className="m3-body-small m-0 mb-1">
            {item.student_id} · {item.concept_id}
          </p>
          <h2 className="m3-headline-medium m-0">{item.knowledge_point}</h2>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <p className="m3-label-small m-0 mb-1">System</p>
            <TonalChip verdict={item.system_verdict} />
            <p className="m3-body-small m-0 mt-1">
              {item.system_marks}/{item.max_marks}
            </p>
          </div>
          <TrustArc score={item.trust_score} size={72} />
        </div>
      </header>

      <p
        className="m3-body-large mb-5 px-4 py-3"
        style={{
          background: "var(--md-sys-color-surface-container-low)",
          borderRadius: "var(--md-sys-shape-corner-large)",
          borderLeft: "4px solid var(--md-sys-color-tertiary)",
        }}
      >
        {item.defer_reason || "Deferred for human review"}
      </p>

      <section
        className="p-5 mb-5"
        style={{
          background: "var(--md-sys-color-surface-container-low)",
          borderRadius: "var(--md-sys-shape-corner-extra-large)",
        }}
      >
        <p className="m3-label-small m-0 mb-3">Student answer</p>
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
          <p className="m3-body-small mt-3 mb-0">
            Quoted evidence (not located inline): “{item.evidence_span}”
          </p>
        )}
      </section>

      <details className="mb-6">
        <summary
          className="cursor-pointer m3-body-small"
          style={{ fontWeight: 600 }}
        >
          System reasoning
        </summary>
        <p className="m3-body-small mt-2 whitespace-pre-wrap mb-0">
          {item.reasoning}
        </p>
      </details>

      {!editing ? (
        <div className="flex flex-wrap gap-3 items-center">
          <button
            type="button"
            className="m3-fab"
            disabled={busy}
            onClick={onAgree}
          >
            Agree
          </button>
          <button
            type="button"
            className="m3-btn-tonal"
            disabled={busy}
            onClick={() => setEditing(true)}
          >
            Correct
          </button>
          <button
            type="button"
            className="m3-btn-text ml-auto"
            onClick={onExplain}
          >
            Why deferred?
          </button>
        </div>
      ) : (
        <div
          className="p-5 flex flex-col gap-4"
          style={{
            background: "var(--md-sys-color-surface-container)",
            borderRadius: "var(--md-sys-shape-corner-extra-large)",
          }}
        >
          <div>
            <p className="m3-label-small m-0 mb-2">Your verdict</p>
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
          </div>
          <div>
            <p className="m3-label-small m-0 mb-2">Marks</p>
            <SegmentedButtons
              ariaLabel="Marks"
              options={markOptions}
              value={marks}
              onChange={setMarks}
            />
          </div>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Optional comment for the research trail"
            rows={2}
            className="w-full p-3 border-0 m3-body-large"
            style={{
              borderRadius: "var(--md-sys-shape-corner-medium)",
              background: "var(--md-sys-color-surface-container-lowest)",
              resize: "vertical",
            }}
          />
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              className="m3-fab"
              disabled={busy}
              onClick={() => onCorrect(verdict, marks, comment)}
            >
              Submit correction
            </button>
            <button
              type="button"
              className="m3-btn-tonal"
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
