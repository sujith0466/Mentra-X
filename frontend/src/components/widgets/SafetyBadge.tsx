import React from "react";
import { ShieldCheck, ShieldAlert, RefreshCw, AlertTriangle } from "lucide-react";
import { cn } from "@/utils/cn";

export type EnkryptAction = "APPROVE" | "REGENERATE" | "HARD_FAIL" | "VERIFIED";

export interface SafetyBadgeProps {
  status: EnkryptAction | string;
  score?: number;
  showIcon?: boolean;
  className?: string;
}

export const SafetyBadge: React.FC<SafetyBadgeProps> = ({
  status,
  score,
  showIcon = true,
  className,
}) => {
  const configs: Record<string, { label: string; bg: string; text: string; border: string; icon: any }> = {
    APPROVE: {
      label: "Safety Approved",
      bg: "bg-emerald-500/10",
      text: "text-emerald-300",
      border: "border-emerald-500/30",
      icon: ShieldCheck,
    },
    VERIFIED: {
      label: "Safety Verified",
      bg: "bg-cyan-500/10",
      text: "text-cyan-300",
      border: "border-cyan-500/30",
      icon: ShieldCheck,
    },
    REGENERATE: {
      label: "Regenerating Response",
      bg: "bg-amber-500/10",
      text: "text-amber-300",
      border: "border-amber-500/30",
      icon: RefreshCw,
    },
    HARD_FAIL: {
      label: "Safety Intercepted",
      bg: "bg-rose-500/10",
      text: "text-rose-300",
      border: "border-rose-500/30",
      icon: ShieldAlert,
    },
    DEFAULT: {
      label: String(status),
      bg: "bg-slate-500/10",
      text: "text-slate-300",
      border: "border-slate-500/30",
      icon: AlertTriangle,
    },
  };

  const config = configs[status] || configs.DEFAULT;
  const Icon = config.icon;

  return (
    <div
      className={cn(
        "inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border shadow-sm transition-all",
        config.bg,
        config.text,
        config.border,
        className
      )}
    >
      {showIcon && <Icon className="w-3.5 h-3.5 shrink-0" />}
      <span>{config.label}</span>
      {score !== undefined && (
        <span className="ml-1 pl-1 border-l border-white/20 font-mono text-[10px]">
          {(score * 100).toFixed(0)}%
        </span>
      )}
    </div>
  );
};
