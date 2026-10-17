import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ReportView({ topic, report, feedback }) {
  const [tab, setTab] = useState("report");
  const [copied, setCopied] = useState(false);
  const score = feedback.match(/(\d+(?:\.\d+)?)\s*\/\s*10/)?.[1];

  const copy = async () => {
    await navigator.clipboard.writeText(report);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const download = () => {
    const url = URL.createObjectURL(new Blob([report], { type: "text/markdown" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = `${topic.slice(0, 40) || "report"}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const tabBtn = (id, label) => (
    <button
      onClick={() => setTab(id)}
      className={[
        "px-4 py-2 text-[13px] font-medium rounded-lg transition-all duration-200",
        tab === id
          ? "bg-[var(--accent)] text-white shadow-sm"
          : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-surface-hover)]",
      ].join(" ")}
    >
      {label}
    </button>
  );

  return (
    <div className="animate-fade-in-up overflow-hidden rounded-[var(--radius-lg)] border border-[var(--border-default)] bg-[var(--bg-raised)] shadow-[var(--shadow-card)]">
      <div className="border-b border-[var(--border-subtle)] px-5 py-4 sm:px-6">
        <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--text-tertiary)]">
          Research report
        </p>
        <h2 className="mt-1 break-words text-lg font-semibold leading-snug text-[var(--text-primary)]">
          {topic}
        </h2>
      </div>

      {/* Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--border-subtle)] px-4 py-3 sm:px-5">
        <div className="flex gap-1">
          {tabBtn("report", "Report")}
          {tabBtn("feedback", `Review${score ? ` · ${score}/10` : ""}`)}
        </div>
        {tab === "report" && (
          <div className="flex gap-2">
            <button
              onClick={copy}
              className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] px-3 py-1.5 text-[12px] font-medium text-[var(--text-secondary)] transition hover:border-[var(--border-focus)] hover:text-[var(--text-primary)]"
            >
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <rect x="4.5" y="4.5" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.2"/>
                <path d="M9.5 4.5V3a1.5 1.5 0 0 0-1.5-1.5H3A1.5 1.5 0 0 0 1.5 3v5A1.5 1.5 0 0 0 3 9.5h1.5" stroke="currentColor" strokeWidth="1.2"/>
              </svg>
              {copied ? "Copied!" : "Copy"}
            </button>
            <button
              onClick={download}
              className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] px-3 py-1.5 text-[12px] font-medium text-[var(--text-secondary)] transition hover:border-[var(--border-focus)] hover:text-[var(--text-primary)]"
            >
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M7 1.5v8M7 9.5l-2.5-2.5M7 9.5l2.5-2.5M2.5 12.5h9" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Download
            </button>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="px-4 py-5 sm:px-6">
        <article className="prose prose-invert max-w-none prose-headings:text-[var(--text-primary)] prose-headings:font-semibold prose-strong:text-[var(--text-primary)] prose-a:text-[var(--accent)] prose-a:underline-offset-4 hover:prose-a:decoration-[var(--accent)] prose-p:text-[var(--text-secondary)] prose-li:text-[var(--text-secondary)] prose-code:text-[var(--accent)] prose-code:bg-[var(--bg-surface)] prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-[13px] prose-pre:bg-[var(--bg-surface)] prose-pre:border prose-pre:border-[var(--border-subtle)]">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {tab === "report" ? report : feedback}
          </ReactMarkdown>
        </article>
      </div>
    </div>
  );
}