import React, { useState } from "react";
import { Outlet, Link, useLocation } from "react-router-dom";
import {
  Sparkles, Sun, Moon, LogOut, ArrowRight, ShieldCheck, Menu, X,
  BookOpen, HelpCircle, DollarSign, FileText, Mail, Home,
  Code2, Share2, Globe, MessageCircle,
} from "lucide-react";
import { useAuthStore } from "@/store/useAuthStore";
import { useUIStore } from "@/store/useUIStore";

const navLinks = [
  { to: "/",        label: "Home",          icon: Home },
  { to: "/courses", label: "Courses",       icon: BookOpen },
  { to: "/pricing", label: "Pricing",       icon: DollarSign },
  { to: "/faq",     label: "FAQ",           icon: HelpCircle },
  { to: "/docs",    label: "Docs",          icon: FileText },
  { to: "/contact", label: "Contact",       icon: Mail },
];

const footerLinks = {
  platform: [
    { to: "/courses",  label: "Course Catalog" },
    { to: "/pricing",  label: "Pricing" },
    { to: "/docs",     label: "Documentation" },
    { to: "/faq",      label: "FAQ" },
    { to: "/about",    label: "About Us" },
  ],
  community: [
    { to: "/community/discussions", label: "Discussion Forum" },
    { to: "/community/leaderboard", label: "Leaderboard" },
    { to: "/community/groups",      label: "Study Groups" },
    { to: "/community/events",      label: "Events" },
  ],
  support: [
    { to: "/help",    label: "Help Center" },
    { to: "/contact", label: "Contact Support" },
    { to: "/login",   label: "Student Login" },
    { to: "/register",label: "Create Account" },
  ],
};

export const PublicLayout: React.FC = () => {
  const { user, logout } = useAuthStore();
  const { theme, toggleTheme } = useUIStore();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const dashboardPath = user?.role === "admin" ? "/admin/dashboard" : "/student/dashboard";

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-obsidian-900 text-slate-900 dark:text-slate-100 flex flex-col transition-colors duration-200">

      {/* ── NAVBAR ─────────────────────────────────────── */}
      <header className="sticky top-0 z-40 w-full h-16 bg-white/85 dark:bg-obsidian-900/85 backdrop-blur-xl border-b border-slate-200/80 dark:border-white/8 flex items-center justify-between px-5 lg:px-10 transition-all duration-200">

        {/* Brand */}
        <div className="flex items-center gap-8">
          <Link to="/" className="flex items-center gap-2.5 group" aria-label="Mentra X Home">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-400 flex items-center justify-center shadow-md shadow-indigo-500/30 group-hover:shadow-indigo-500/50 transition-shadow">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <div className="flex flex-col leading-none">
              <span className="text-sm font-bold text-slate-900 dark:text-white tracking-tight">Mentra X</span>
              <span className="text-[9px] font-semibold text-indigo-600 dark:text-indigo-400 tracking-widest uppercase mt-0.5">AI Learning</span>
            </div>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1" aria-label="Main navigation">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all duration-150 ${
                  location.pathname === link.to
                    ? "text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-500/10"
                    : "text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5"
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-2">
          {/* Safety badge — desktop only */}
          <div className="hidden lg:flex items-center gap-1.5 text-[10px] font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-100 dark:border-emerald-500/20 px-2.5 py-1 rounded-full">
            <ShieldCheck className="w-3 h-3" /> AI Safety Verified
          </div>

          {/* Theme toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 transition-all"
            aria-label="Toggle theme"
          >
            {theme === "dark" ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* Auth section */}
          {user ? (
            <div className="flex items-center gap-2 pl-2 border-l border-slate-200 dark:border-white/10">
              <Link
                to={dashboardPath}
                className="inline-flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-500 transition-all shadow-sm shadow-indigo-500/25"
              >
                <span>Dashboard</span>
                <ArrowRight className="w-3 h-3" />
              </Link>
              <button
                onClick={logout}
                className="p-2 rounded-lg text-slate-400 hover:text-rose-500 dark:hover:text-rose-400 hover:bg-rose-500/10 transition-all"
                aria-label="Log out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="hidden sm:flex items-center gap-2 pl-2 border-l border-slate-200 dark:border-white/10">
              <Link
                to="/login"
                className="px-3 py-1.5 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors"
              >
                Log In
              </Link>
              <Link
                to="/register"
                className="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-500 transition-all shadow-sm shadow-indigo-500/25"
              >
                Start Free
              </Link>
            </div>
          )}

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-white/5 transition-all"
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {/* Mobile nav drawer */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-30 top-16">
          <div className="absolute inset-0 bg-black/20 dark:bg-black/40 backdrop-blur-sm" onClick={() => setMobileOpen(false)} />
          <div className="absolute top-0 left-0 right-0 bg-white dark:bg-obsidian-900 border-b border-slate-200 dark:border-white/10 p-4 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                onClick={() => setMobileOpen(false)}
                className="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-white/5 transition-colors"
              >
                <link.icon className="w-4 h-4 text-slate-400" />
                {link.label}
              </Link>
            ))}
            {!user && (
              <div className="pt-3 border-t border-slate-100 dark:border-white/8 flex gap-2">
                <Link to="/login" onClick={() => setMobileOpen(false)} className="flex-1 text-center py-2 text-sm font-semibold text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-white/10 rounded-lg hover:bg-slate-50 dark:hover:bg-white/5 transition-colors">Log In</Link>
                <Link to="/register" onClick={() => setMobileOpen(false)} className="flex-1 text-center py-2 text-sm font-semibold bg-indigo-600 text-white rounded-lg hover:bg-indigo-500 transition-colors">Start Free</Link>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── MAIN CONTENT ───────────────────────────────── */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* ── FOOTER ─────────────────────────────────────── */}
      <footer className="w-full bg-white dark:bg-obsidian-900 border-t border-slate-200 dark:border-white/8 mt-16">
        <div className="max-w-7xl mx-auto px-6 lg:px-10 pt-14 pb-8">

          {/* Main footer grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-10 pb-12 border-b border-slate-100 dark:border-white/6">

            {/* Brand column — wider */}
            <div className="lg:col-span-2 space-y-4">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-400 flex items-center justify-center shadow-md shadow-indigo-500/30">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <div>
                  <div className="text-sm font-bold text-slate-900 dark:text-white">Mentra X</div>
                  <div className="text-[10px] text-indigo-600 dark:text-indigo-400 font-semibold tracking-widest uppercase">AI Learning Platform</div>
                </div>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-xs">
                Your personal AI learning companion — adapting to your pace, filling your knowledge gaps, and preparing you for the career you deserve.
              </p>

              {/* Trust badges */}
              <div className="space-y-1.5 text-xs">
                <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-medium">
                  <ShieldCheck className="w-3.5 h-3.5" /> AI Safety Verified
                </div>
                <div className="flex items-center gap-1.5 text-slate-500 dark:text-slate-400">
                  <ShieldCheck className="w-3.5 h-3.5" /> GDPR &amp; Privacy Compliant
                </div>
                <div className="flex items-center gap-1.5 text-slate-500 dark:text-slate-400">
                  <ShieldCheck className="w-3.5 h-3.5" /> Real-Time Audit Logging
                </div>
              </div>

              {/* Social icons */}
              <div className="flex items-center gap-2 pt-1">
                {[
                  { Icon: Code2,         href: "https://github.com", label: "GitHub" },
                  { Icon: Share2,        href: "https://twitter.com", label: "Twitter" },
                  { Icon: Globe,         href: "https://linkedin.com", label: "LinkedIn" },
                  { Icon: MessageCircle, href: "https://discord.com", label: "Discord" },
                ].map(({ Icon, href, label }) => (
                  <a
                    key={label}
                    href={href}
                    aria-label={label}
                    className="w-8 h-8 rounded-lg flex items-center justify-center bg-slate-100 dark:bg-obsidian-800 text-slate-500 dark:text-slate-400 hover:bg-indigo-50 dark:hover:bg-indigo-500/10 hover:text-indigo-600 dark:hover:text-indigo-400 transition-all border border-transparent hover:border-indigo-100 dark:hover:border-indigo-500/20"
                  >
                    <Icon className="w-3.5 h-3.5" />
                  </a>
                ))}
              </div>
            </div>

            {/* Platform links */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white mb-4">Platform</h4>
              <ul className="space-y-2.5">
                {footerLinks.platform.map((l) => (
                  <li key={l.to}>
                    <Link to={l.to} className="text-xs text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Community links */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white mb-4">Community</h4>
              <ul className="space-y-2.5">
                {footerLinks.community.map((l) => (
                  <li key={l.to}>
                    <Link to={l.to} className="text-xs text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Support links */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white mb-4">Support</h4>
              <ul className="space-y-2.5">
                {footerLinks.support.map((l) => (
                  <li key={l.to}>
                    <Link to={l.to} className="text-xs text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Bottom bar */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 text-xs text-slate-400">
            <p>© {new Date().getFullYear()} Mentra X. All rights reserved.</p>
            <div className="flex items-center gap-5">
              <Link to="/about"   className="hover:text-slate-600 dark:hover:text-slate-200 transition-colors">About</Link>
              <Link to="/contact" className="hover:text-slate-600 dark:hover:text-slate-200 transition-colors">Contact</Link>
              <Link to="/help"    className="hover:text-slate-600 dark:hover:text-slate-200 transition-colors">Help</Link>
              <Link to="/docs"    className="hover:text-slate-600 dark:hover:text-slate-200 transition-colors">Docs</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};
