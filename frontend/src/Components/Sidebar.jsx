import Loading from "./Loading";
import { STEPS } from "../steps";

/* Status indicator — small, clean, informational */
function StatusBadge({ status }) {
  switch (status) {
    case "running":
      return <Loading />;
    case "done":
      return (
        <span className="inline-flex items-center gap-1 text-[11px] font-medium tracking-wide text-[var(--success)]">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M2.5 6.5L4.5 8.5L9.5 3.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          DONE
        </span>
      );
    case "error":
      return (
        <span className="inline-flex items-center gap-1 text-[11px] font-medium tracking-wide text-[var(--danger)]">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M3 9L9 3M3 3l6 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          FAILED
        </span>
      );
    default:
      return (
        <span className="text-[11px] font-medium tracking-wide text-[var(--text-tertiary)]">
          PENDING
        </span>
      );
  }
}

export default function Sidebar({ statuses }) {
  const runningStep = statuses.findIndex((status) => status === "running");
  const completeCount = statuses.filter((status) => status === "done").length;
  const hasError = statuses.includes("error");
  const summary = hasError
    ? "A step needs attention"
    : runningStep >= 0
    ? `Step ${runningStep + 1} of ${STEPS.length} in progress`
    : completeCount === STEPS.length
    ? "Research complete"
    : "Ready when you are";

  return (
    <aside className="animate-fade-in rounded-[var(--radius-lg)] border border-[var(--border-default)] bg-[var(--bg-raised)] p-4 shadow-[var(--shadow-card)] sm:p-5">
      <div className="mb-4 border-b border-[var(--border-subtle)] pb-4">
        <div className="flex items-center justify-between gap-3">
          <h2 className="text-[15px] font-semibold text-[var(--text-primary)]">
            Research process
          </h2>
          {completeCount > 0 && (
            <span className="text-[11px] tabular-nums text-[var(--text-tertiary)]">
              {completeCount}/{STEPS.length}
            </span>
          )}
        </div>
        <p className="mt-1 text-[12px] leading-5 text-[var(--text-secondary)]">
          {summary}
        </p>
      </div>

      {/* Steps list */}
      <div className="space-y-2.5">
        {STEPS.map((step, i) => {
          const isRunning = statuses[i] === "running";
          const isDone = statuses[i] === "done";
          const isError = statuses[i] === "error";

          return (
            <div
              key={step.id}
              className={[
                "rounded-[var(--radius-md)] border p-3 transition-colors duration-200",
                isRunning
                  ? "border-[var(--accent)]/35 bg-[var(--accent-muted)]"
                  : isDone
                  ? "border-[var(--success)]/15 bg-[var(--success-muted)]"
                  : isError
                  ? "border-[var(--danger)]/25 bg-[var(--danger-muted)]"
                  : "border-[var(--border-subtle)] bg-[var(--bg-raised)]",
              ].join(" ")}
              aria-current={isRunning ? "step" : undefined}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  {/* Step number */}
                  <span
                    className={[
                      "flex h-6 w-6 items-center justify-center rounded-md text-[11px] font-bold",
                      isRunning
                        ? "bg-[var(--accent)] text-white"
                        : isDone
                        ? "bg-[var(--success)]/15 text-[var(--success)]"
                        : isError
                        ? "bg-[var(--danger)]/10 text-[var(--danger)]"
                        : "bg-[var(--bg-surface)] text-[var(--text-tertiary)]",
                    ].join(" ")}
                  >
                    {i + 1}
                  </span>
                  <span className="text-sm font-medium text-[var(--text-primary)]">
                    {step.title}
                  </span>
                </div>
                <StatusBadge status={statuses[i]} />
              </div>
              <p className="mt-1.5 pl-[34px] text-[12px] leading-relaxed text-[var(--text-secondary)]">
                {step.desc}
              </p>
            </div>
          );
        })}
      </div>
    </aside>
  );
}