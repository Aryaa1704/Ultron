import { NavLink, Route, Routes } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import DashboardPage from "./pages/DashboardPage";
import SettingsPage from "./pages/SettingsPage";

const linkBase = "px-4 py-2 rounded-lg transition";
const activeClass = "bg-neon text-black";
const idleClass = "bg-surface text-slate-200 hover:bg-neon/25";

export default function App() {
  return (
    <div className="min-h-screen bg-jet text-slate-100">
      <header className="border-b border-neon/30 bg-surface/60 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <h1 className="text-xl font-semibold tracking-wide text-neonSoft">JARVIS-OS</h1>
          <nav className="flex gap-2">
            {[
              { to: "/", label: "Dashboard" },
              { to: "/chat", label: "Chat" },
              { to: "/settings", label: "Settings" }
            ].map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `${linkBase} ${isActive ? activeClass : idleClass}`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  );
}
