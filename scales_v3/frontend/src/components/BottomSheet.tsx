import { useEffect } from "react";

export function BottomSheet({
  open,
  title,
  onClose,
  children,
}: {
  open: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center"
      style={{ background: "color-mix(in srgb, black 40%, transparent)" }}
      onClick={onClose}
      role="presentation"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="w-full max-w-2xl m3-card p-6 mb-0"
        style={{
          borderBottomLeftRadius: 0,
          borderBottomRightRadius: 0,
          borderTopLeftRadius: "var(--md-sys-shape-corner-extra-large)",
          borderTopRightRadius: "var(--md-sys-shape-corner-extra-large)",
          maxHeight: "80vh",
          overflow: "auto",
          animation: "card-enter var(--md-sys-motion-duration-medium) var(--md-sys-motion-easing-expressive)",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="m3-title-large m-0">{title}</h2>
          <button
            type="button"
            onClick={onClose}
            className="border-0 cursor-pointer px-3 py-2"
            style={{
              borderRadius: "var(--md-sys-shape-corner-full)",
              background: "var(--md-sys-color-surface-container-high)",
            }}
          >
            Close
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}
