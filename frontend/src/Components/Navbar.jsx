import { NavLink } from "react-router-dom";

const link = ({ isActive }) =>
  `px-3 py-1 rounded-md text-sm transition ${
    isActive ? "text-orange-400" : "text-gray-400 hover:text-white"
  }`;

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between border-b border-white/10 px-6 py-4">
      <span className="text-lg font-bold text-white">
        Research<span className="text-orange-500">Mind</span>
      </span>
      <div className="flex gap-2">
        <NavLink to="/" className={link}>Home</NavLink>
        <NavLink to="/about" className={link}>About</NavLink>
      </div>
    </nav>
  );
}