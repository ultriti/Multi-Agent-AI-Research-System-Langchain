import { STEPS } from "../../steps";

export default function AboutPage() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="mb-4 text-3xl font-bold text-white">About ResearchMind</h1>
      <p className="mb-8 text-gray-400">
        ResearchMind is a multi-agent research pipeline built with LangChain and Gemini.
        Enter a topic and the four-stage workflow produces a report and a separate review.
      </p>
      <ol className="space-y-3">
        {STEPS.map((s, i) => (
          <li key={s.title} className="rounded-xl border border-white/10 bg-white/5 p-4">
            <span className="mr-3 font-bold text-orange-500">0{i + 1}</span>
            <span className="font-semibold text-white">{s.title}</span>
            <p className="mt-1 text-sm text-gray-400">{s.desc}</p>
          </li>
        ))}
      </ol>
    </main>
  );
}