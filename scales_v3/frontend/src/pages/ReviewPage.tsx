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
    setItems(data.items);
    setProgress(data.progress);
    setIndex(0);
  }, [examId]);

  useEffect(() => {
    load().catch((e: Error) => setError(e.message));
  }, [load]);

  const current = items[index] ?? null;

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
      setDoneMsg("Finals written. You can open results.");
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setFinalizing(false);
    }
  };

  const resolved = progress?.resolved ?? 0;
  const total = progress?.total ?? items.length;
  const remaining = progress?.remaining ?? items.length;
  const pct = total ? Math.round((resolved / total) * 100) : 0;

  return (
    <div className="shell" style={{ maxWidth: 820 }}>
      <div className="flex items-start justify-between gap-4 flex-wrap mb-6">
        <div>
          <Link to="/" className="m3-btn-text" style={{ paddingLeft: 0 }}>
            ← Exams
          </Link>
          <h1 className="m3-headline-large m-0 mt-1">Resolve DEFERs</h1>
          <p
            className="m3-body-small m-0 mt-1"
            style={{ wordBreak: "break-all" }}
          >
            {examId}
          </p>
        </div>
        <div className="text-right">
          <p className="m3-display-large m-0" style={{ fontSize: "2.5rem" }}>
            {remaining}
          </p>
          <p className="m3-label-small m-0">remaining</p>
        </div>
      </div>

      <div
        className="h-3 mb-8 overflow-hidden"
        style={{
          background: "var(--md-sys-color-surface-container-highest)",
          borderRadius: "var(--md-sys-shape-corner-full)",
        }}
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label="Review progress"
      >
        <div
          style={{
            width: `${pct}%`,
            height: "100%",
            transformOrigin: "left",
            background:
              "linear-gradient(90deg, var(--md-sys-color-primary), color-mix(in srgb, var(--md-sys-color-tertiary) 55%, var(--md-sys-color-primary)))",
            borderRadius: "inherit",
            transition:
              "width var(--md-sys-motion-duration-medium) var(--md-sys-motion-easing-expressive)",
          }}
        />
      </div>

      <p className="m3-body-small mt-0 mb-5">
        Item {Math.min(resolved + (current ? 1 : 0), total)} of {total}
        {" · "}
        Shortcuts: <kbd>A</kbd> agree · <kbd>←</kbd>/<kbd>→</kbd> browse
      </p>

      {error && (
        <p
          className="m3-body-large mb-4 px-4 py-3"
          style={{
            color: "var(--md-sys-color-on-error-container)",
            background: "var(--md-sys-color-error-container)",
            borderRadius: "var(--md-sys-shape-corner-medium)",
          }}
        >
          {error}
        </p>
      )}

      {doneMsg && (
        <p
          className="m3-body-large mb-4 px-4 py-3"
          style={{
            background: "var(--md-sys-color-primary-container)",
            color: "var(--md-sys-color-on-primary-container)",
            borderRadius: "var(--md-sys-shape-corner-medium)",
          }}
        >
          {doneMsg}{" "}
          <Link
            to={`/exams/${encodeURIComponent(examId)}/results`}
            style={{ fontWeight: 700, color: "inherit" }}
          >
            View results →
          </Link>
        </p>
      )}

      {current ? (
        <QueueCard
          key={current.review_item_id}
          item={current}
          exiting={exiting}
          busy={busy}
          onAgree={onAgree}
          onCorrect={(v, m, c) => void submit(v, m, c)}
          onExplain={() => setExplainOpen(true)}
        />
      ) : (
        <div className="m3-surface p-10 text-center">
          <p className="m3-label-small m-0 mb-2">Queue clear</p>
          <h2 className="m3-headline-large m-0">All DEFERs resolved</h2>
          <p className="m3-body-large mt-3 mb-6 max-w-md mx-auto">
            Finalize to fold teacher corrections into final scores for every
            student.
          </p>
          <button
            type="button"
            className="m3-fab"
            disabled={finalizing}
            onClick={() => void finalize()}
          >
            {finalizing ? "Finalizing…" : "Finalize exam"}
          </button>
        </div>
      )}

      <BottomSheet
        open={explainOpen}
        title="Why this was deferred"
        onClose={() => setExplainOpen(false)}
      >
        {current && (
          <TrustDetail
            signals={current.signals}
            deferReason={current.defer_reason}
            trustScore={current.trust_score}
          />
        )}
      </BottomSheet>
    </div>
  );
}
