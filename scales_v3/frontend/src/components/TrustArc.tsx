export function TrustArc({
  score,
  size = 48,
}: {
  score: number;
  size?: number;
}) {
  const clamped = Math.max(0, Math.min(1, score));
  const r = (size - 8) / 2;
  const c = 2 * Math.PI * r;
  const dash = clamped * c;
  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      role="img"
      aria-label={`Trust score ${clamped.toFixed(2)}`}
    >
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke="var(--md-sys-color-surface-container-highest)"
        strokeWidth={6}
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke="var(--md-sys-color-primary)"
        strokeWidth={6}
        strokeLinecap="round"
        strokeDasharray={`${dash} ${c - dash}`}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text
        x="50%"
        y="50%"
        dominantBaseline="central"
        textAnchor="middle"
        fontSize={11}
        fontWeight={600}
        fill="var(--md-sys-color-on-surface)"
      >
        {clamped.toFixed(2)}
      </text>
    </svg>
  );
}
