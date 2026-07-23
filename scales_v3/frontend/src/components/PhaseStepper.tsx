import type { PipelinePhase } from "../types";

const STEPS: { id: PipelinePhase; label: string }[] = [
  { id: "idle", label: "Idle" },
  { id: "grading", label: "Grading" },
  { id: "awaiting_review", label: "Review" },
  { id: "complete", label: "Complete" },
];

const ORDER: PipelinePhase[] = ["idle", "grading", "awaiting_review", "complete"];

export function PhaseStepper({ phase }: { phase: PipelinePhase }) {
  const current = ORDER.indexOf(phase);
  return (
    <ol className="flex gap-2 items-center flex-wrap m-0 p-0 list-none" aria-label="Pipeline phase">
      {STEPS.map((step, i) => {
        const done = i < current;
        const active = i === current;
        return (
          <li key={step.id} className="flex items-center gap-2">
            <span
              className="inline-flex items-center justify-center m3-label-small"
              style={{
                width: 28,
                height: 28,
                borderRadius: "var(--md-sys-shape-corner-full)",
                background: active
                  ? "var(--md-sys-color-primary)"
                  : done
                    ? "var(--md-sys-color-primary-container)"
                    : "var(--md-sys-color-surface-container-highest)",
                color: active
                  ? "var(--md-sys-color-on-primary)"
                  : "var(--md-sys-color-on-surface)",
              }}
              aria-current={active ? "step" : undefined}
            >
              {done ? "✓" : i + 1}
            </span>
            <span className="m3-body-small" style={{ fontWeight: active ? 600 : 400 }}>
              {step.label}
            </span>
            {i < STEPS.length - 1 && (
              <span
                aria-hidden
                style={{
                  width: 16,
                  height: 2,
                  background: "var(--md-sys-color-outline-variant)",
                  display: "inline-block",
                }}
              />
            )}
          </li>
        );
      })}
    </ol>
  );
}
