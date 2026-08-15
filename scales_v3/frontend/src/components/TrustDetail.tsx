import type { CbteSignals } from "../types";
import { TrustArc } from "./TrustArc";

export function TrustDetail({
  signals,
  deferReason,
  trustScore,
}: {
  signals: CbteSignals | null;
  deferReason: string;
  trustScore?: number;
}) {
  if (!signals) {
    return (
      <p className="m3-body-large">No CBTE signals available for this item.</p>
    );
  }

  const tiers = [
    { n: 1, label: "Evidence + keywords", hint: "Fast deterministic checks" },
    { n: 2, label: "NLI entailment", hint: "DeBERTa on evidence ↔ claim" },
    { n: 3, label: "Weighted trust", hint: "NLI + keywords + stability" },
  ];

  const rows: { label: string; value: string; warn?: boolean }[] = [
    {
      label: "Evidence verified",
      value: signals.signal_1_evidence_verified ? "Yes" : "No — quote mismatch",
      warn: !signals.signal_1_evidence_verified,
    },
    {
      label: "NLI score",
      value:
        signals.signal_2_nli_score == null
          ? "—"
          : signals.signal_2_nli_score.toFixed(3),
      warn:
        signals.signal_2_nli_score != null && signals.signal_2_nli_score < 0.7,
    },
    {
      label: "Keyword score",
      value: signals.signal_4_keyword_score.toFixed(2),
      warn: signals.signal_4_keyword_score < 0.3,
    },
    {
      label: "Stability",
      value:
        signals.signal_3_stability == null
          ? "—"
          : signals.signal_3_stability.toFixed(2),
    },
  ];

  return (
    <div className="flex flex-col gap-5">
      {trustScore != null && (
        <div className="flex items-center gap-4">
          <TrustArc score={trustScore} size={88} />
          <div>
            <p className="m3-label-small m-0">Trust score</p>
            <p className="m3-headline-medium m-0">{trustScore.toFixed(2)}</p>
            <p className="m3-body-small m-0">Below τ → human review</p>
          </div>
        </div>
      )}

      <p className="m3-body-large m-0">{deferReason || signals.reason}</p>

      <div className="flex gap-2 flex-wrap" aria-label="Tier resolution">
        {tiers.map((t) => {
          const active = signals.tier_resolved === t.n;
          return (
            <div
              key={t.n}
              className="flex-1 min-w-[140px] p-4"
              style={{
                borderRadius: "var(--md-sys-shape-corner-large)",
                background: active
                  ? "var(--md-sys-color-primary-container)"
                  : "var(--md-sys-color-surface-container-high)",
                color: active
                  ? "var(--md-sys-color-on-primary-container)"
                  : undefined,
                outline: active
                  ? "2px solid var(--md-sys-color-primary)"
                  : "none",
                transform: active ? "scale(1.02)" : undefined,
                transition:
                  "transform var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-spring)",
              }}
            >
              <p className="m3-label-small m-0">Tier {t.n}</p>
              <p className="m3-body-large m-0 mt-1" style={{ fontWeight: 600 }}>
                {t.label}
              </p>
              <p className="m3-body-small m-0 mt-1">{t.hint}</p>
              {active && (
                <p
                  className="m3-label-small m-0 mt-3"
                  style={{ color: "var(--md-sys-color-primary)" }}
                >
                  Resolved here
                </p>
              )}
            </div>
          );
        })}
      </div>

      <dl className="grid gap-3 m-0" style={{ gridTemplateColumns: "1fr 1fr" }}>
        {rows.map((row) => (
          <div
            key={row.label}
            className="p-3"
            style={{
              borderRadius: "var(--md-sys-shape-corner-medium)",
              background: row.warn
                ? "var(--md-sys-color-tertiary-container)"
                : "var(--md-sys-color-surface-container-low)",
              color: row.warn
                ? "var(--md-sys-color-on-tertiary-container)"
                : undefined,
            }}
          >
            <dt className="m3-label-small">{row.label}</dt>
            <dd className="m3-title-large m-0 mt-1">{row.value}</dd>
          </div>
        ))}
      </dl>

      {signals.keywords_found.length > 0 && (
        <div>
          <p className="m3-label-small m-0 mb-2">Keywords found</p>
          <div className="flex flex-wrap gap-2">
            {signals.keywords_found.map((kw) => (
              <span
                key={kw}
                className="px-3 py-1 m3-body-small"
                style={{
                  background: "var(--md-sys-color-secondary-container)",
                  color: "var(--md-sys-color-on-secondary-container)",
                  borderRadius: "var(--md-sys-shape-corner-full)",
                  fontWeight: 600,
                }}
              >
                {kw}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
