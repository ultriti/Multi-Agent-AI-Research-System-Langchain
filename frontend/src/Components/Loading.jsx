export default function Loading({ text = "", size = "h-4 w-4" }) {
  return (
    <div className="flex items-center gap-2 text-sm text-orange-400">
      <span className={`${size} animate-spin rounded-full border-2 border-orange-400 border-t-transparent`} />
      {text && <span>{text}</span>}
    </div>
  );
}