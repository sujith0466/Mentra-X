import React from "react";
import { cn } from "@/utils/cn";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "primary" | "success" | "warning" | "danger" | "purple" | "cyan" | "info";
  size?: "sm" | "md";
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant = "default", size = "sm", children, ...props }, ref) => {
    const variants = {
      default: "bg-white/10 text-slate-300 border-white/10",
      primary: "bg-primary-500/10 text-indigo-300 border-indigo-500/20",
      success: "bg-emerald-500/10 text-emerald-300 border-emerald-500/20",
      warning: "bg-amber-500/10 text-amber-300 border-amber-500/20",
      danger: "bg-rose-500/10 text-rose-300 border-rose-500/20",
      purple: "bg-purple-500/10 text-purple-300 border-purple-500/20",
      cyan: "bg-cyan-500/10 text-cyan-300 border-cyan-500/20",
      info: "bg-cyan-500/10 text-cyan-300 border-cyan-500/20",
    };

    const sizes = {
      sm: "px-2 py-0.5 text-xs",
      md: "px-2.5 py-1 text-sm",
    };

    return (
      <span
        ref={ref}
        className={cn(
          "inline-flex items-center font-medium rounded-full border transition-colors",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        {children}
      </span>
    );
  }
);

Badge.displayName = "Badge";
