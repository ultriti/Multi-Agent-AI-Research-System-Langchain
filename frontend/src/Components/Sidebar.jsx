import Loading from "./Loading";
import { STEPS } from "../steps";

const badge = {
  waiting: <span className="text-xs tracking-widest text-gray-500">WAITING</span>,
  running: <Loading />,
  done: <span className="text-xs tracking-widest text-green-400">DONE</span>,
  error: <span className="text-xs tracking-widest text-red-400">FAILED</span>,
};

export default function Sidebar({ statuses }) {
  return (
    <aside>
      <h2 className="mb-4 text-xl font-bold text-white">Pipeline</h2>
      <div className="space-y-3">
        {STEPS.map((step, i) => (
          <div
            key={step.title}
            className={`rounded-xl border p-4 transition ${
              statuses[i] === "running"
                ? "border-orange-500/60 bg-orange-500/5"
                : "border-white/10 bg-white/5"
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-xs font-bold text-orange-500">0{i + 1}</span>
                <span className="font-semibold text-white">{step.title}</span>
              </div>
              {badge[statuses[i]]}
            </div>
            <p className="mt-1 text-sm text-gray-400">{step.desc}</p>
          </div>
        ))}
      </div>
    </aside>
  );
}