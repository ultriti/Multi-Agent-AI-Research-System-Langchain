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
      // connection problem: mark whatever was running as failed
      setStatuses((prev) => prev.map((s) => (s === "running" ? "error" : s)));
      setError(e.message);
    } finally {
      setRunning(false);
    }
  };

  const currentStep = statuses.findIndex((s) => s === "running");

  return (
    <main className="mx-auto grid max-w-6xl gap-10 px-6 py-10 lg:grid-cols-[1fr_360px]">
      <section>
        <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-orange-500">
          Research Topic
        </p>
        <input
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && runPipeline()}
          placeholder="e.g. Quantum computing breakthroughs in 2025"
          className="w-full rounded-lg border border-white/10 bg-white/10 px-4 py-3 text-white outline-none focus:border-orange-500"
        />
        <button
          onClick={runPipeline}
          disabled={running || !topic.trim()}
          className="mt-4 w-full rounded-lg bg-gradient-to-r from-orange-400 to-orange-600 py-3 font-semibold text-white shadow-lg shadow-orange-500/20 transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          ⚡ Run Research Pipeline
        </button>

        <div className="mt-6 flex flex-wrap items-center gap-2">
          <span className="text-xs uppercase tracking-widest text-gray-500">Try →</span>
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => setTopic(s)}
              className="rounded-md bg-white/5 px-3 py-1.5 text-sm text-gray-300 hover:bg-white/10"
            >
              {s}
            </button>
          ))}
        </div>

        <div className="mt-8">
          {running && currentStep >= 0 && (
            <Loading size="h-5 w-5" text={STEPS[currentStep].loading} />
          )}
          {error && (
            <p className="rounded-lg border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-300">
              {error}
            </p>
          )}
          {result && <ReportView {...result} />}
        </div>
      </section>

      <Sidebar statuses={statuses} />
    </main>
  );
}