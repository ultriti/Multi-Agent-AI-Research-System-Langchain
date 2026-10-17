export default function Loading({ text = "", size = "h-4 w-4" }) {
  return (
    <div className="flex items-center gap-2.5 text-sm text-[var(--accent)]">
      <span
        className={`${size} rounded-full border-2 border-[var(--accent)] border-t-transparent`}
        style={{ animation: "spin-smooth 0.8s linear infinite" }}
      />
      {text && <span className="text-[var(--text-secondary)] text-[13px]">{text}</span>}
    </div>
  );
}