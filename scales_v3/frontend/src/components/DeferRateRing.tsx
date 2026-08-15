export function DeferRateRing({
  rate,
  size = 80,
}: {
  rate: number;
  size?: number;
}) {
  const clamped = Math.max(0, Math.min(1, rate));
  const r = (size - 12) / 2;
  const c = 2 * Math.PI * r;
  const dash = clamped * c;
  const hot = clamped > 0.35;
  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      role="img"
      aria-label={`Defer rate ${(clamped * 100).toFixed(0)} percent`}
    >
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="var(--md-sys-color-surface-container-low)"
        stroke="var(--md-sys-color-surface-container-highest)"
        strokeWidth={10}
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke={
          hot ? "var(--md-sys-color-tertiary)" : "var(--md-sys-color-primary)"
        }
        strokeWidth={10}
        strokeLinecap="round"
        strokeDasharray={`${dash} ${c - dash}`}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text
        x="50%"
        y="50%"
        dominantBaseline="central"
        textAnchor="middle"
        fontSize={16}
        fontWeight={750}
        fill="var(--md-sys-color-on-surface)"
        fontFamily="Roboto Flex, sans-serif"
      >
        {(clamped * 100).toFixed(0)}%
      </text>
    </svg>
  );
}
