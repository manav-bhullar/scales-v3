import type { CbteSignals } from "../types";

export function TrustDetail({
  signals,
  deferReason,
}: {
  signals: CbteSignals | null;
  deferReason: string;
}) {
  if (!signals) {
    return <p className="m3-body-large">No CBTE signals available for this item.</p>;
  }

  const tiers = [
    { n: 1, label: "Evidence + keywords" },
    { n: 2, label: "NLI entailment" },
    { n: 3, label: "Weighted trust" },
  ];

  return (
    <div className="flex flex-col gap-4">
      <p className="m3-body-large m-0">{deferReason || signals.reason}</p>

      <div className="flex gap-2 flex-wrap" aria-label="Tier resolution">
        {tiers.map((t) => {
          const active = signals.tier_resolved === t.n;
          return (
            <div
              key={t.n}
              className="flex-1 min-w-[120px] p-3"
              style={{
                borderRadius: "var(--md-sys-shape-corner-medium)",
                background: active
                  ? "var(--md-sys-color-primary-container)"
                  : "var(--md-sys-color-surface-container-high)",
                outline: active
                  ? "2px solid var(--md-sys-color-primary)"
                  : "none",
              }}
            >
              <p className="m3-label-small m-0">Tier {t.n}</p>
              <p className="m3-body-small m-0 mt-1">{t.label}</p>
              {active && (
                <p className="m3-label-small m-0 mt-2" style={{ color: "var(--md-sys-color-primary)" }}>
                  Resolved here
                </p>
              )}
            </div>
          );
        })}
      </div>

      <dl className="grid gap-2 m-0" style={{ gridTemplateColumns: "1fr 1fr" }}>
        <div>
          <dt className="m3-label-small">Evidence verified</dt>
          <dd className="m3-body-large m-0">
            {signals.signal_1_evidence_verified ? "Yes" : "No"}
          </dd>
        </div>
        <div>
          <dt className="m3-label-small">NLI score</dt>
          <dd className="m3-body-large m-0">
            {signals.signal_2_nli_score == null
              ? "—"
              : signals.signal_2_nli_score.toFixed(3)}
          </dd>
        </div>
        <div>
          <dt className="m3-label-small">Keyword score</dt>
          <dd className="m3-body-large m-0">
            {signals.signal_4_keyword_score.toFixed(2)}
          </dd>
        </div>
        <div>
          <dt className="m3-label-small">Stability</dt>
          <dd className="m3-body-large m-0">
            {signals.signal_3_stability == null
              ? "—"
              : signals.signal_3_stability.toFixed(2)}
          </dd>
        </div>
      </dl>

      {signals.keywords_found.length > 0 && (
        <div>
          <p className="m3-label-small m-0 mb-2">Keywords found</p>
          <div className="flex flex-wrap gap-2">
            {signals.keywords_found.map((kw) => (
              <span
                key={kw}
                className="px-2 py-1 m3-body-small"
                style={{
                  background: "var(--md-sys-color-secondary-container)",
                  borderRadius: "var(--md-sys-shape-corner-full)",
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
