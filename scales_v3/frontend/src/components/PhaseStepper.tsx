import type { PipelinePhase } from "../types";

const STEPS: { id: PipelinePhase; label: string }[] = [
  { id: "idle", label: "Idle" },
  { id: "grading", label: "Grading" },
  { id: "awaiting_review", label: "Review" },
  { id: "complete", label: "Complete" },
];

const ORDER: PipelinePhase[] = [
  "idle",
  "grading",
  "awaiting_review",
  "complete",
];

export function PhaseStepper({ phase }: { phase: PipelinePhase }) {
  const current = ORDER.indexOf(phase);
  return (
    <ol
      className="flex gap-2 items-center flex-wrap m-0 p-0 list-none"
      aria-label="Pipeline phase"
    >
      {STEPS.map((step, i) => {
        const done = i < current;
        const active = i === current;
        return (
          <li key={step.id} className="flex items-center gap-2">
            <span
              className="inline-flex items-center justify-center"
              style={{
                width: 32,
                height: 32,
                fontSize: "0.75rem",
                fontWeight: 700,
                borderRadius: "var(--md-sys-shape-corner-full)",
                background: active
                  ? "var(--md-sys-color-primary)"
                  : done
                    ? "var(--md-sys-color-primary-container)"
                    : "var(--md-sys-color-surface-container-highest)",
                color: active
                  ? "var(--md-sys-color-on-primary)"
                  : done
                    ? "var(--md-sys-color-on-primary-container)"
                    : "var(--md-sys-color-on-surface)",
                transition:
                  "transform var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-spring)",
                transform: active ? "scale(1.08)" : undefined,
              }}
              aria-current={active ? "step" : undefined}
            >
              {done ? "✓" : i + 1}
            </span>
            <span
              className="m3-body-small"
              style={{
                fontWeight: active ? 700 : 500,
                color: active ? "var(--md-sys-color-primary)" : undefined,
              }}
            >
              {step.label}
            </span>
            {i < STEPS.length - 1 && (
              <span
                aria-hidden
                style={{
                  width: 18,
                  height: 3,
                  borderRadius: 999,
                  background: done
                    ? "var(--md-sys-color-primary)"
                    : "var(--md-sys-color-outline-variant)",
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
