import { useState } from "react";
import Sidebar from "../../Components/Sidebar";
import Loading from "../../Components/Loading";
import ReportView from "../../Components/ReportView";
import { STEPS } from "../../steps";
import { runResearch } from "../../api";

const SUGGESTIONS = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"];
const IDLE = STEPS.map(() => "waiting");
const stepIndex = (id) => STEPS.findIndex((s) => s.id === id);

export default function HomePage() {
  const [topic, setTopic] = useState("");
  const [statuses, setStatuses] = useState(IDLE);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const mark = (i, status) =>
    setStatuses((prev) => prev.map((s, idx) => (idx === i ? status : s)));

  const handleEvent = (ev) => {
    if (ev.type === "status") {
      mark(stepIndex(ev.step), ev.status);
    } else if (ev.type === "result") {
      setResult({ topic, report: ev.report, feedback: ev.feedback });
    } else if (ev.type === "error") {
      if (ev.step) mark(stepIndex(ev.step), "error");
      setError(ev.message);
    }
  };

  const runPipeline = async () => {
    if (!topic.trim() || running) return;
    setRunning(true);
    setError("");
    setResult(null);
    setStatuses(IDLE);

    try {
      await runResearch(topic, handleEvent);
    } catch (e) {
      setStatuses((prev) => prev.map((s) => (s === "running" ? "error" : s)));
      setError(e.message);
    } finally {
      setRunning(false);
    }
  };

  const currentStep = statuses.findIndex((s) => s === "running");

  return (
    <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10">
      <div className="grid grid-cols-1 items-start gap-6 md:grid-cols-[minmax(0,1fr)_280px]">
        {/* ── Left column ─────────────────────────── */}
        <section className="space-y-6">
          {/* Header area */}
          <div className="max-w-2xl">
            <p className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--accent)]">
              Research workspace
            </p>
            <h1 className="text-2xl font-semibold tracking-tight text-[var(--text-primary)] sm:text-[30px]">
              Research, with sources you can follow.
            </h1>
            <p className="mt-2 max-w-xl text-[14px] leading-6 text-[var(--text-secondary)]">
              Choose a topic to create a clear report, backed by links to its sources.
            </p>
          </div>

          {/* Input card */}
          <div className="rounded-[var(--radius-lg)] border border-[var(--border-default)] bg-[var(--bg-raised)] p-4 shadow-[var(--shadow-card)] sm:p-5">
            <div className="mb-4">
              <h2 className="text-[15px] font-semibold text-[var(--text-primary)]">
                Start a research report
              </h2>
              <p className="mt-1 text-[13px] text-[var(--text-secondary)]">
                Enter a subject or pick one of the suggested topics.
              </p>
            </div>
            <label
              htmlFor="research-topic"
              className="mb-2 block text-[12px] font-semibold uppercase tracking-wider text-[var(--text-tertiary)]"
            >
              Research Topic
            </label>
            <div className="flex gap-3">
              <input
                id="research-topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && runPipeline()}
                placeholder="e.g. Quantum computing breakthroughs in 2025"
                className="min-w-0 flex-1 rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] px-4 py-2.5 text-[14px] text-[var(--text-primary)] placeholder-[var(--text-tertiary)] outline-none transition-colors focus:border-[var(--accent)]"
                aria-label="Research topic"
              />
              <button
                onClick={runPipeline}
                disabled={running || !topic.trim()}
                className="inline-flex items-center gap-2 whitespace-nowrap rounded-lg bg-[var(--accent)] px-5 py-2.5 text-[13px] font-semibold text-white shadow-sm transition-all hover:bg-[var(--accent-hover)] active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-40"
              >
                {running ? (
                  <>
                    <span
                      className="h-3.5 w-3.5 rounded-full border-2 border-white/40 border-t-white"
                      style={{ animation: "spin-smooth 0.8s linear infinite" }}
                    />
                    Running…
                  </>
                ) : (
                  <>
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <path d="M7 1.5v11M1.5 7h11" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                    </svg>
                    Start research
                  </>
                )}
              </button>
            </div>

            {/* Suggestions */}
            <div className="mt-3.5 flex flex-wrap items-center gap-2">
              <span className="text-[11px] font-medium uppercase tracking-widest text-[var(--text-tertiary)]">
                Suggestions
              </span>
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => setTopic(s)}
                  className="rounded-md border border-[var(--border-subtle)] bg-[var(--bg-surface)] px-2.5 py-1 text-[12px] text-[var(--text-secondary)] transition-colors hover:border-[var(--accent)]/30 hover:text-[var(--text-primary)]"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          {/* Status / Error / Result */}
          <div className="space-y-4">
            {running && currentStep >= 0 && (
              <div className="animate-fade-in rounded-[var(--radius-md)] border border-[var(--accent)]/20 bg-[var(--accent-muted)] px-4 py-3">
                <Loading size="h-4 w-4" text={STEPS[currentStep].loading} />
              </div>
            )}

            {error && (
              <div className="animate-fade-in rounded-[var(--radius-md)] border border-[var(--danger)]/30 bg-[var(--danger-muted)] px-4 py-3">
                <div className="flex items-start gap-2.5">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="mt-0.5 shrink-0 text-[var(--danger)]">
                    <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M8 5v3.5M8 10.5v.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  <p className="text-[13px] leading-relaxed text-[var(--danger)]">{error}</p>
                </div>
              </div>
            )}

            {result && <ReportView {...result} />}
          </div>
        </section>

        {/* ── Right column — Pipeline status ──────── */}
        <div className="md:sticky md:top-20">
          <Sidebar statuses={statuses} />
        </div>
      </div>
    </main>
  );
}