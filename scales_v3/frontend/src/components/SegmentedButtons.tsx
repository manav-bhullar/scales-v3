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
      className="inline-flex overflow-hidden"
      style={{
        borderRadius: "var(--md-sys-shape-corner-full)",
        background: "var(--md-sys-color-surface-container-high)",
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
            className="px-3 py-2 m3-body-small border-0 cursor-pointer transition-colors"
            style={{
              background: selected
                ? "var(--md-sys-color-secondary-container)"
                : "transparent",
              color: selected
                ? "var(--md-sys-color-on-secondary-container)"
                : "var(--md-sys-color-on-surface)",
              fontWeight: selected ? 600 : 400,
            }}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
