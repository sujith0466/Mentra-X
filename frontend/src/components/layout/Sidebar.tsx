import React from "react";
import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  BookOpen,
  BrainCircuit,
  TrendingUp,
  Code2,
  Users,
  ShieldAlert,
  ChevronLeft,
  ChevronRight,
  Briefcase,
  FileCheck2,
  MessageSquare,
  Trophy,
  Calendar,
  FolderGit2,
  FileText,
  Activity,
  Shield,
} from "lucide-react";
import { useAuthStore } from "@/store/useAuthStore";
import { useUIStore } from "@/store/useUIStore";
import { cn } from "@/utils/cn";

export const Sidebar: React.FC = () => {
  const { user } = useAuthStore();
  const { isSidebarCollapsed, toggleSidebar } = useUIStore();
  const location = useLocation();

  const studentLinks = [
    { title: "Dashboard", href: "/student/dashboard", icon: LayoutDashboard },
    { title: "My Courses", href: "/student/my-courses", icon: BookOpen },
    { title: "Digital Twin", href: "/student/twin", icon: BrainCircuit, badge: "AI" },
    { title: "AI Tutor Swarm", href: "/student/ai/tutor", icon: MessageSquare, badge: "24/7" },
    { title: "Skill Assessment", href: "/student/assessment", icon: Activity },
    { title: "Study Notes", href: "/student/notes", icon: FileText },
    { title: "Recommendations", href: "/student/recommendations", icon: TrendingUp },
    { title: "Project Studio", href: "/student/projects", icon: FolderGit2 },
    { title: "Study Planner", href: "/student/ai/planner", icon: Calendar },
    { title: "Coding Arena", href: "/student/coding", icon: Code2 },
    { title: "Career & Resume", href: "/student/career/resume", icon: Briefcase },
    { title: "Interview Prep", href: "/student/interview", icon: FileCheck2 },
  ];

  const communityLinks = [
    { title: "Discussions Forum", href: "/community/discussions", icon: MessageSquare },
    { title: "XP Leaderboard", href: "/community/leaderboard", icon: Trophy, badge: "Top" },
    { title: "Study Guilds", href: "/community/groups", icon: Users },
    { title: "Live Events", href: "/community/events", icon: Calendar },
  ];

  const adminLinks = [
    { title: "AI Operations", href: "/admin/dashboard", icon: LayoutDashboard },
    { title: "Platform Analytics", href: "/admin/analytics", icon: TrendingUp },
    { title: "Swarm Monitoring", href: "/admin/ai-monitoring", icon: Activity, badge: "Live" },
    { title: "Enkrypt Security", href: "/admin/enkrypt", icon: Shield, badge: "Layer 6" },
    { title: "Manage Students", href: "/admin/students", icon: Users },
    { title: "Manage Courses", href: "/admin/courses", icon: BookOpen },
    { title: "Audit Logs", href: "/admin/audit-logs", icon: ShieldAlert },
  ];

  const isRoleAdmin = user?.role === "admin";
  const mainLinks = isRoleAdmin ? adminLinks : studentLinks;

  return (
    <motion.aside
      initial={false}
      animate={{ width: isSidebarCollapsed ? 80 : 260 }}
      className="sticky top-16 h-[calc(100vh-4rem)] bg-obsidian-800 border-r border-obsidian-600 flex flex-col justify-between p-4 transition-all z-30 shrink-0 overflow-y-auto"
    >
      <div className="space-y-6">
        <div className="flex items-center justify-between px-2">
          {!isSidebarCollapsed && (
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              {isRoleAdmin ? "Enterprise Admin" : "Student LMS Portal"}
            </span>
          )}
          <button
            onClick={toggleSidebar}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-white/5 transition-colors ml-auto"
            title={isSidebarCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            {isSidebarCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Main Navigation Section */}
        <nav className="space-y-1">
          {mainLinks.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                to={link.href}
                className={cn(
                  "flex items-center space-x-3 px-3 py-2.5 rounded-xl font-medium text-sm transition-all relative group",
                  isActive
                    ? "bg-primary-600/10 text-primary-500 border border-primary-500/20 shadow-sm shadow-indigo-500/10"
                    : "text-slate-400 hover:text-slate-200 hover:bg-white/5"
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeSidebarIndicator"
                    className="absolute left-0 w-1 h-6 bg-primary-500 rounded-r-full"
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
                <Icon className={cn("w-5 h-5 shrink-0", isActive ? "text-primary-500" : "text-slate-400 group-hover:text-slate-200")} />
                {!isSidebarCollapsed && <span className="truncate">{link.title}</span>}
                {!isSidebarCollapsed && link.badge && (
                  <span className="ml-auto px-1.5 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    {link.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>

        {/* Community Network Section (For Students & Admins) */}
        <div className="pt-4 border-t border-white/10 space-y-2">
          {!isSidebarCollapsed && (
            <span className="px-2 text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
              Community Network
            </span>
          )}
          <nav className="space-y-1">
            {communityLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname.startsWith(link.href);
              return (
                <Link
                  key={link.href}
                  to={link.href}
                  className={cn(
                    "flex items-center space-x-3 px-3 py-2 rounded-xl font-medium text-xs transition-all relative group",
                    isActive
                      ? "bg-cyan-600/10 text-cyan-400 border border-cyan-500/20 shadow-sm"
                      : "text-slate-400 hover:text-slate-200 hover:bg-white/5"
                  )}
                >
                  <Icon className={cn("w-4 h-4 shrink-0", isActive ? "text-cyan-400" : "text-slate-400 group-hover:text-slate-200")} />
                  {!isSidebarCollapsed && <span className="truncate">{link.title}</span>}
                  {!isSidebarCollapsed && link.badge && (
                    <span className="ml-auto px-1.5 py-0.5 rounded text-[9px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                      {link.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {!isSidebarCollapsed && (
        <div className="mt-6 p-3 rounded-xl bg-obsidian-900 border border-obsidian-600/50 flex items-center space-x-3 shrink-0">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <div className="flex flex-col text-xs">
            <span className="font-semibold text-slate-300">Enkrypt Layer 6</span>
            <span className="text-[10px] text-slate-500">100% Validated</span>
          </div>
        </div>
      )}
    </motion.aside>
  );
};
