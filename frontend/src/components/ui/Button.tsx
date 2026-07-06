import React from "react";
import { motion, HTMLMotionProps } from "framer-motion";
import { Loader2 } from "lucide-react";
import { cn } from "@/utils/cn";

export interface ButtonProps extends Omit<HTMLMotionProps<"button">, "ref" | "children"> {
  children?: React.ReactNode;
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      isLoading = false,
      leftIcon,
      rightIcon,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      "inline-flex items-center justify-center font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 disabled:opacity-50 disabled:pointer-events-none rounded-lg";

    const variants = {
      primary:
        "bg-primary-600 text-white hover:bg-primary-500 shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/30 border border-indigo-400/20",
      secondary:
        "bg-slate-200 dark:bg-obsidian-700 text-slate-800 dark:text-slate-100 hover:bg-slate-300 dark:hover:bg-obsidian-600 border border-slate-300 dark:border-obsidian-600",
      outline:
        "bg-transparent text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-obsidian-600 hover:border-indigo-500/50 hover:bg-slate-100 dark:hover:bg-white/5",
      ghost: "bg-transparent text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 hover:text-slate-900 dark:hover:text-white",
      danger:
        "bg-ai-rose/80 text-white hover:bg-ai-rose border border-rose-400/30 shadow-lg shadow-rose-500/20",
    };

    const sizes = {
      sm: "text-xs px-3 py-1.5 gap-1.5",
      md: "text-sm px-4 py-2 gap-2",
      lg: "text-base px-6 py-3 gap-2.5",
    };

    return (
      <motion.button
        ref={ref}
        whileHover={{ scale: disabled || isLoading ? 1 : 1.01 }}
        whileTap={{ scale: disabled || isLoading ? 1 : 0.98 }}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && <Loader2 className="w-4 h-4 animate-spin" />}
        {!isLoading && leftIcon && <span className="inline-flex">{leftIcon}</span>}
        <span>{children}</span>
        {!isLoading && rightIcon && <span className="inline-flex">{rightIcon}</span>}
      </motion.button>
    );
  }
);

Button.displayName = "Button";
