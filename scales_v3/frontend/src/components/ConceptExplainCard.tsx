import type { ConceptExplain, Verdict } from "../types";
import { TonalChip } from "./TonalChip";
import { highlightEvidence } from "../lib/evidenceHighlight";

/** Plain-language headline: what the teacher reads first. */
function headline(c: ConceptExplain): string {
  const awarded = c.marks_awarded;
  const max = c.max_marks;
  const verdict: Verdict = c.teacher_verdict ?? c.verdict;
  const marks = c.teacher_marks ?? awarded;
  switch (verdict) {
    case "FULL":
      return `Full marks (${marks}/${max}) — the concept is fully present in the answer.`;
    case "PARTIAL":
      return `Partial marks (${marks}/${max}) — the concept is only partly present.`;
    case "ABSENT":
      return `No marks (${marks}/${max}) — the concept was not found in the answer.`;
    case "INCORRECT":
      return `No marks (${marks}/${max}) — the answer addresses this concept but states it wrongly.`;
  }
}

function accent(c: ConceptExplain): string {
  const verdict: Verdict = c.teacher_verdict ?? c.verdict;
  if (verdict === "FULL") return "var(--md-sys-color-tertiary)";
  if (verdict === "PARTIAL") return "var(--md-sys-color-secondary)";
  if (verdict === "INCORRECT") return "var(--md-sys-color-error)";
  return "var(--md-sys-color-outline)";
}

function Pill({
  children,
  bg,
  fg,
  title,
}: {
  children: React.ReactNode;
  bg: string;
  fg?: string;
  title?: string;
}) {
  return (
    <span
      className="m3-label-small px-2.5 py-1 inline-flex items-center gap-1"
      title={title}
      style={{
        background: bg,
        color: fg,
        borderRadius: "var(--md-sys-shape-corner-full)",
        textTransform: "none",
        letterSpacing: 0,
      }}
    >
      {children}
    </span>
  );
}

export function ConceptExplainCard({
  concept,
  answerText,
  expanded,
  onToggle,
}: {
  concept: ConceptExplain;
  answerText: string;
  expanded: boolean;
  onToggle: () => void;
}) {
  const c = concept;
  const shownMarks = c.teacher_marks ?? c.marks_awarded;
  const shownVerdict = c.teacher_verdict ?? c.verdict;
  const fillPct = c.max_marks > 0 ? (shownMarks / c.max_marks) * 100 : 0;
  const evidence = highlightEvidence(answerText, c.evidence_span);
  // Zero marks that CBTE trusted enough to auto-accept: the teacher was never
  // shown this judgment, so an over-strict rubric silently costs the student.
  const silentZero =
    shownMarks === 0 && c.decision === "ACCEPT" && c.source === "auto";

  return (
    <li
      className="overflow-hidden"
      style={{
        background: "var(--md-sys-color-surface-container-low)",
        borderRadius: "var(--md-sys-shape-corner-large)",
        borderLeft: `6px solid ${accent(c)}`,
      }}
    >
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={expanded}
        className="w-full text-left border-0 bg-transparent cursor-pointer p-4 md:p-5"
      >
        <div className="flex items-start justify-between gap-3 flex-wrap">
          <div className="flex-1 min-w-[200px]">
            <p className="m3-label-small m-0">{c.concept_id}</p>
            <p className="m3-title-large m-0 mt-0.5">{c.knowledge_point}</p>
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <TonalChip verdict={shownVerdict} />
            <span className="m3-title-large" style={{ whiteSpace: "nowrap" }}>
              {shownMarks}
              <span className="m3-body-small"> / {c.max_marks}</span>
            </span>
          </div>
        </div>

        <div
          className="mt-3 h-2 w-full overflow-hidden"
          style={{
            background: "var(--md-sys-color-surface-container-highest)",
            borderRadius: "var(--md-sys-shape-corner-full)",
          }}
          role="img"
          aria-label={`${shownMarks} of ${c.max_marks} marks`}
        >
          <div
            className="h-full"
            style={{
              width: `${fillPct}%`,
              background: accent(c),
              borderRadius: "var(--md-sys-shape-corner-full)",
              transition:
                "width var(--md-sys-motion-duration-medium) var(--md-sys-motion-easing-emphasized)",
            }}
          />
        </div>

        <p className="m3-body-large m-0 mt-3">{headline(c)}</p>

        <div className="flex gap-2 mt-3 flex-wrap">
          {c.source === "teacher" ? (
            <Pill
              bg="var(--md-sys-color-primary-container)"
              fg="var(--md-sys-color-on-primary-container)"
            >
              Teacher decided
              {c.correction_type ? ` · ${c.correction_type}` : ""}
            </Pill>
          ) : c.decision === "DEFER" ? (
            <Pill
              bg="var(--md-sys-color-tertiary-container)"
              fg="var(--md-sys-color-on-tertiary-container)"
            >
              Sent to teacher (low trust {c.trust_score.toFixed(2)})
            </Pill>
          ) : (
            <Pill bg="var(--md-sys-color-surface-container-highest)">
              Auto-accepted · trust {c.trust_score.toFixed(2)}
            </Pill>
          )}
          {silentZero && (
            <Pill
              bg="var(--md-sys-color-error-container)"
              fg="var(--md-sys-color-on-error-container)"
              title="Machine gave 0 and was confident, so no human ever checked it. If the rubric is too strict, this is where marks quietly disappear."
            >
              Zero without human check
            </Pill>
          )}
          <Pill bg="var(--md-sys-color-surface-container-highest)">
            {expanded ? "Hide detail ▴" : "Why? ▾"}
          </Pill>
        </div>
      </button>

      {expanded && (
        <div
          className="px-4 md:px-5 pb-5 flex flex-col gap-4"
          style={{
            animation:
              "card-enter var(--md-sys-motion-duration-medium) var(--md-sys-motion-easing-expressive)",
          }}
        >
          <Section label="What this concept required">
            <p className="m3-body-large m-0">
              {c.target_criteria || c.knowledge_point}
            </p>
          </Section>

          <Section label="Grader's reasoning">
            <p className="m3-body-large m-0">{c.reasoning}</p>
            {c.counter_arguments && (
              <p className="m3-body-small m-0 mt-2">
                Counter-argument considered: {c.counter_arguments}
              </p>
            )}
          </Section>

          <Section label="Evidence quoted from the answer">
            {c.evidence_span ? (
              <p className="m3-body-large m-0">
                {evidence ? (
                  <>
                    <span style={{ opacity: 0.5 }}>
                      …{evidence.before.slice(-60)}
                    </span>
                    <mark className="evidence-mark">{evidence.match}</mark>
                    <span style={{ opacity: 0.5 }}>
                      {evidence.after.slice(0, 60)}…
                    </span>
                  </>
                ) : (
                  <>
                    <q>{c.evidence_span}</q>{" "}
                    <span
                      className="m3-body-small"
                      style={{ color: "var(--md-sys-color-error)" }}
                    >
                      (not located verbatim in the answer)
                    </span>
                  </>
                )}
              </p>
            ) : (
              <p className="m3-body-small m-0">
                None — the grader found nothing in the answer to quote for this
                concept.
              </p>
            )}
          </Section>

          <Section label="Rubric keywords">
            <div className="flex gap-2 flex-wrap">
              {c.keywords_found.map((k) => (
                <Pill
                  key={`f-${k}`}
                  bg="var(--md-sys-color-tertiary-container)"
                  fg="var(--md-sys-color-on-tertiary-container)"
                >
                  ✓ {k}
                </Pill>
              ))}
              {c.keywords_missing.map((k) => (
                <Pill
                  key={`m-${k}`}
                  bg="var(--md-sys-color-surface-container-highest)"
                  title="Expected by the rubric, not matched in this answer"
                >
                  ○ {k}
                </Pill>
              ))}
              {c.expected_keywords.length === 0 && (
                <span className="m3-body-small">
                  No keywords on this concept.
                </span>
              )}
            </div>
          </Section>

          <Section
            label={`Trust signals · resolved at tier ${c.tier_resolved}`}
          >
            <div className="flex gap-2 flex-wrap">
              <Pill
                bg="var(--md-sys-color-surface-container-highest)"
                title="Was the quoted evidence actually found in the student's answer?"
              >
                Evidence{" "}
                {c.signal_1_evidence_verified ? "verified" : "unverified"}
              </Pill>
              <Pill
                bg="var(--md-sys-color-surface-container-highest)"
                title="Fraction of rubric keywords matched"
              >
                Keywords {(c.signal_4_keyword_score * 100).toFixed(0)}%
              </Pill>
              {c.signal_2_nli_score !== null && (
                <Pill
                  bg="var(--md-sys-color-surface-container-highest)"
                  title="NLI entailment between answer and concept"
                >
                  NLI {c.signal_2_nli_score.toFixed(2)}
                </Pill>
              )}
              {c.signal_3_stability !== null && (
                <Pill
                  bg="var(--md-sys-color-surface-container-highest)"
                  title="Agreement across repeated gradings"
                >
                  Stability {c.signal_3_stability.toFixed(2)}
                </Pill>
              )}
            </div>
            {c.trust_reason && (
              <p className="m3-body-small m-0 mt-2">{c.trust_reason}</p>
            )}
          </Section>

          {c.source === "teacher" && (
            <Section label="Teacher override">
              <p className="m3-body-large m-0">
                Machine said {c.verdict} ({c.marks_awarded}/{c.max_marks});
                teacher set {c.teacher_verdict} ({c.teacher_marks}/{c.max_marks}
                ).
              </p>
              {c.teacher_comment && (
                <p className="m3-body-small m-0 mt-1">“{c.teacher_comment}”</p>
              )}
            </Section>
          )}
        </div>
      )}
    </li>
  );
}

function Section({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className="p-4"
      style={{
        background: "var(--md-sys-color-surface-container-lowest)",
        borderRadius: "var(--md-sys-shape-corner-medium)",
      }}
    >
      <p className="m3-label-small m-0 mb-2">{label}</p>
      {children}
    </div>
  );
}
