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
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = prev;
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center"
      style={{
        background:
          "color-mix(in srgb, var(--md-sys-color-inverse-surface) 45%, transparent)",
      }}
      onClick={onClose}
      role="presentation"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="w-full max-w-2xl p-6 md:p-8"
        style={{
          background: "var(--md-sys-color-surface-container-lowest)",
          borderTopLeftRadius: "var(--md-sys-shape-corner-extra-large)",
          borderTopRightRadius: "var(--md-sys-shape-corner-extra-large)",
          maxHeight: "85vh",
          overflow: "auto",
          animation:
            "sheet-up var(--md-sys-motion-duration-medium) var(--md-sys-motion-easing-spring)",
          boxShadow:
            "0 -8px 40px color-mix(in srgb, var(--md-sys-color-on-surface) 18%, transparent)",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div
          className="mx-auto mb-4"
          style={{
            width: 40,
            height: 4,
            borderRadius: 999,
            background: "var(--md-sys-color-outline-variant)",
          }}
          aria-hidden
        />
        <div className="flex items-center justify-between mb-5 gap-3">
          <h2 className="m3-headline-medium m-0">{title}</h2>
          <button type="button" className="m3-btn-tonal" onClick={onClose}>
            Close
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}
