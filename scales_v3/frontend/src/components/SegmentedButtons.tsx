type Option<T extends string | number> = { value: T; label: string };

export function SegmentedButtons<T extends string | number>({
  options,
  value,
  onChange,
  ariaLabel,
}: {
  options: Option<T>[];
  value: T;
  onChange: (v: T) => void;
  ariaLabel: string;
}) {
  return (
    <div
      role="radiogroup"
      aria-label={ariaLabel}
      className="inline-flex flex-wrap overflow-hidden"
      style={{
        borderRadius: "var(--md-sys-shape-corner-full)",
        background: "var(--md-sys-color-surface-container-highest)",
        padding: 4,
        gap: 2,
      }}
    >
      {options.map((opt) => {
        const selected = opt.value === value;
        return (
          <button
            key={String(opt.value)}
            type="button"
            role="radio"
            aria-checked={selected}
            onClick={() => onChange(opt.value)}
            className="px-4 py-2.5 border-0 cursor-pointer"
            style={{
              borderRadius: "var(--md-sys-shape-corner-full)",
              background: selected
                ? "var(--md-sys-color-secondary-container)"
                : "transparent",
              color: selected
                ? "var(--md-sys-color-on-secondary-container)"
                : "var(--md-sys-color-on-surface)",
              fontWeight: selected ? 700 : 500,
              transition:
                "background var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-expressive), transform var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-spring)",
              transform: selected ? "scale(1.02)" : undefined,
            }}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
