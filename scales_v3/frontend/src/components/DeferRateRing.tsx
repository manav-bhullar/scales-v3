export function DeferRateRing({ rate, size = 72 }: { rate: number; size?: number }) {
  const clamped = Math.max(0, Math.min(1, rate));
  const r = (size - 10) / 2;
  const c = 2 * Math.PI * r;
  const dash = clamped * c;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} role="img" aria-label={`Defer rate ${(clamped * 100).toFixed(0)} percent`}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--md-sys-color-surface-container-highest)" strokeWidth={8} />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke="var(--md-sys-color-secondary)"
        strokeWidth={8}
        strokeLinecap="round"
        strokeDasharray={`${dash} ${c - dash}`}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x="50%" y="50%" dominantBaseline="central" textAnchor="middle" fontSize={14} fontWeight={700} fill="var(--md-sys-color-on-surface)">
        {(clamped * 100).toFixed(0)}%
      </text>
    </svg>
  );
}
