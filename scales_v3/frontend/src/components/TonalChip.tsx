import type { Verdict } from "../types";

const VERDICT_META: Record<
  Verdict,
  { label: string; icon: string; bg: string; fg: string }
> = {
  FULL: {
    label: "Full",
    icon: "✓",
    bg: "var(--md-sys-color-tertiary-container)",
    fg: "var(--md-sys-color-on-tertiary-container)",
  },
  PARTIAL: {
    label: "Partial",
    icon: "½",
    bg: "var(--md-sys-color-secondary-container)",
    fg: "var(--md-sys-color-on-secondary-container)",
  },
  ABSENT: {
    label: "Absent",
    icon: "○",
    bg: "var(--md-sys-color-surface-container-highest)",
    fg: "var(--md-sys-color-on-surface)",
  },
  INCORRECT: {
    label: "Incorrect",
    icon: "!",
    bg: "var(--md-sys-color-error-container)",
    fg: "var(--md-sys-color-on-error-container)",
  },
};

export function TonalChip({ verdict }: { verdict: Verdict }) {
  const m = VERDICT_META[verdict];
  return (
    <span
      className="inline-flex items-center gap-1.5 px-3 py-1 m3-label-small"
      style={{
        background: m.bg,
        color: m.fg,
        borderRadius: "var(--md-sys-shape-corner-full)",
      }}
      aria-label={`Verdict: ${m.label}`}
    >
      <span aria-hidden="true">{m.icon}</span>
      {m.label}
    </span>
  );
}
