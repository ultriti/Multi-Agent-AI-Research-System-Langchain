import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ReportView({ topic, report, feedback }) {
  const [tab, setTab] = useState("report");
  const score = feedback.match(/(\d+(?:\.\d+)?)\s*\/\s*10/)?.[1];

  const copy = () => navigator.clipboard.writeText(report);

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
      className={`rounded-md px-4 py-1.5 text-sm ${
        tab === id ? "bg-orange-500 text-white" : "bg-white/5 text-gray-400 hover:text-white"
      }`}
    >
      {label}
    </button>
  );

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex gap-2">
          {tabBtn("report", "Report")}
          {tabBtn("feedback", `Critic Feedback${score ? ` (${score}/10)` : ""}`)}
        </div>
        {tab === "report" && (
          <div className="flex gap-2 text-sm">
            <button onClick={copy} className="rounded-md bg-white/5 px-3 py-1.5 hover:bg-white/10">Copy</button>
            <button onClick={download} className="rounded-md bg-white/5 px-3 py-1.5 hover:bg-white/10">Download .md</button>
          </div>
        )}
      </div>

      <article className="prose prose-invert max-w-none prose-headings:text-white prose-strong:text-white prose-a:text-orange-400">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {tab === "report" ? report : feedback}
        </ReactMarkdown>
      </article>
    </div>
  );
}