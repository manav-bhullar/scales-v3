export function TrustArc({
  score,
  size = 48,
}: {
  score: number;
  size?: number;
}) {
  const clamped = Math.max(0, Math.min(1, score));
  const r = (size - 10) / 2;
  const c = 2 * Math.PI * r;
  const dash = clamped * c;
  const stroke =
    clamped < 0.5
      ? "var(--md-sys-color-tertiary)"
      : clamped < 0.7
        ? "var(--md-sys-color-secondary)"
        : "var(--md-sys-color-primary)";

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
        fill="var(--md-sys-color-surface-container-low)"
        stroke="var(--md-sys-color-surface-container-highest)"
        strokeWidth={8}
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke={stroke}
        strokeWidth={8}
        strokeLinecap="round"
        strokeDasharray={`${dash} ${c - dash}`}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        style={{
          transition:
            "stroke-dasharray var(--md-sys-motion-duration-long) var(--md-sys-motion-easing-expressive)",
        }}
      />
      <text
        x="50%"
        y="50%"
        dominantBaseline="central"
        textAnchor="middle"
        fontSize={size > 60 ? 16 : 11}
        fontWeight={700}
        fill="var(--md-sys-color-on-surface)"
        fontFamily="Roboto Flex, sans-serif"
      >
        {clamped.toFixed(2)}
      </text>
    </svg>
  );
}
