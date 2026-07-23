import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import type { ReviewItem, ReviewProgress, Verdict } from "../types";
import { QueueCard } from "../components/QueueCard";
import { BottomSheet } from "../components/BottomSheet";
import { TrustDetail } from "../components/TrustDetail";

export function ReviewPage() {
  const { examId = "" } = useParams();
  const [items, setItems] = useState<ReviewItem[]>([]);
  const [progress, setProgress] = useState<ReviewProgress | null>(null);
  const [index, setIndex] = useState(0);
  const [exiting, setExiting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [explainOpen, setExplainOpen] = useState(false);
  const [finalizing, setFinalizing] = useState(false);
  const [doneMsg, setDoneMsg] = useState<string | null>(null);

  const load = useCallback(async () => {
    const data = await api.getReview(examId);
    // Filter out already-resolved items using progress: show remaining only
    // Backend returns full deferred queue; resolved ones still listed until we
    // filter by matching corrections — progress.remaining is authoritative.
    setItems(data.items);
    setProgress(data.progress);
    setIndex(0);
  }, [examId]);

  useEffect(() => {
    load().catch((e: Error) => setError(e.message));
  }, [load]);

  // Unresolved = items whose (student,concept) not yet corrected.
  // We track locally by shrinking the working list after each submit.
  const current = items[index] ?? null;
  const remainingLocal = items.length;

  const advance = () => {
    setExiting(true);
    window.setTimeout(() => {
      setItems((prev) => prev.filter((_, i) => i !== index));
      setExiting(false);
      setIndex(0);
    }, 320);
  };

  const submit = async (verdict: Verdict, marks: number, comment = "") => {
    if (!current || busy) return;
    setBusy(true);
    setError(null);
    try {
      const res = await api.submitCorrection(examId, {
        student_id: current.student_id,
        concept_id: current.concept_id,
        verdict,
        marks,
        comment,
      });
      setProgress(res.progress);
      advance();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  const onAgree = () => {
    if (!current) return;
    void submit(current.system_verdict, current.system_marks);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (busy || explainOpen) return;
      const tag = (e.target as HTMLElement)?.tagName;
      if (tag === "TEXTAREA" || tag === "INPUT") return;
      if (e.key === "a" || e.key === "A") {
        e.preventDefault();
        onAgree();
      } else if (e.key === "c" || e.key === "C") {
        // Correct mode is opened inside QueueCard — focus hint only
      } else if (e.key === "ArrowRight") {
        setIndex((i) => Math.min(i + 1, Math.max(items.length - 1, 0)));
      } else if (e.key === "ArrowLeft") {
        setIndex((i) => Math.max(i - 1, 0));
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [busy, explainOpen, current, items.length]);

  const finalize = async () => {
    setFinalizing(true);
    setError(null);
    try {
      await api.finalize(examId);
      setDoneMsg("Review complete — finals written.");
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setFinalizing(false);
    }
  };

  const resolved = progress?.resolved ?? 0;
  const total = progress?.total ?? remainingLocal;
  const pct = total ? Math.round((resolved / total) * 100) : 0;

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6 gap-3 flex-wrap">
        <div>
          <Link to="/" className="m3-body-small" style={{ color: "var(--md-sys-color-primary)" }}>
            ← Exams
          </Link>
          <h1 className="m3-headline-medium m-0 mt-1">Review queue</h1>
          <p className="m3-body-small m-0">{examId}</p>
        </div>
        <p className="m3-title-large m-0">
          Item {Math.min(resolved + 1, total)} of {total}
        </p>
      </div>

      <div
        className="h-2 mb-6 overflow-hidden"
        style={{
          background: "var(--md-sys-color-surface-container-highest)",
          borderRadius: "var(--md-sys-shape-corner-full)",
        }}
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          style={{
            width: `${pct}%`,
            height: "100%",
            background: "var(--md-sys-color-primary)",
            transition: "width var(--md-sys-motion-duration-medium) var(--md-sys-motion-easing-expressive)",
          }}
        />
      </div>

      {error && (
        <p className="m3-body-large mb-4" style={{ color: "var(--md-sys-color-error)" }}>
          {error}
        </p>
      )}
      {doneMsg && (
        <p className="m3-body-large mb-4" style={{ color: "var(--md-sys-color-tertiary)" }}>
          {doneMsg}{" "}
          <Link to={`/exams/${encodeURIComponent(examId)}/results`}>View results</Link>
        </p>
      )}

      {current ? (
        <QueueCard
          key={current.review_item_id}
          item={current}
          exiting={exiting}
          onAgree={onAgree}
          onCorrect={(v, m, c) => void submit(v, m, c)}
          onExplain={() => setExplainOpen(true)}
        />
      ) : (
        <div className="m3-card p-8 text-center">
          <h2 className="m3-headline-medium">Queue clear</h2>
          <p className="m3-body-large">
            All deferred items have corrections. Finalize to aggregate marks.
          </p>
          <button
            type="button"
            disabled={finalizing}
            className="border-0 cursor-pointer px-6 py-3 mt-4"
            style={{
              background: "var(--md-sys-color-primary)",
              color: "var(--md-sys-color-on-primary)",
              borderRadius: "var(--md-sys-shape-corner-full)",
            }}
            onClick={() => void finalize()}
          >
            {finalizing ? "Finalizing…" : "Finalize exam"}
          </button>
        </div>
      )}

      <p className="m3-body-small mt-4">
        Shortcuts: <kbd>A</kbd> agree · <kbd>←</kbd>/<kbd>→</kbd> navigate
      </p>

      <BottomSheet
        open={explainOpen}
        title="Trust signals"
        onClose={() => setExplainOpen(false)}
      >
        {current && (
          <TrustDetail
            signals={current.signals}
            deferReason={current.defer_reason}
          />
        )}
      </BottomSheet>
    </div>
  );
}
