import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }) =>
  [
    "relative px-3 py-1.5 text-[13px] font-medium rounded-md transition-colors duration-200",
    isActive
      ? "text-[var(--text-primary)] bg-[var(--bg-surface)]"
      : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-surface-hover)]",
  ].join(" ");

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-[var(--bg-base)]/80 border-b border-[var(--border-subtle)]">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 h-14">
        {/* Logo */}
        <NavLink to="/" className="flex items-center gap-2 group">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[var(--accent)] text-white text-xs font-bold shadow-sm">
            R
          </div>
          <span className="text-[15px] font-semibold tracking-tight text-[var(--text-primary)]">
            Research<span className="text-[var(--accent)]">Mind</span>
          </span>
        </NavLink>

        {/* Navigation */}
        <div className="flex items-center gap-1">
          <NavLink to="/" className={linkClass} end>
            Home
          </NavLink>
          <NavLink to="/about" className={linkClass}>
            About
          </NavLink>
        </div>
      </nav>
    </header>
  );
}