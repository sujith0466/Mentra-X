import React from "react";
import { motion, HTMLMotionProps } from "framer-motion";
import { cn } from "@/utils/cn";

export interface CardProps extends HTMLMotionProps<"div"> {
  variant?: "default" | "glass" | "glow" | "interactive" | "gradient";
  children: React.ReactNode;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = "default", children, ...props }, ref) => {
    const variants = {
      default: "bg-obsidian-800 border border-obsidian-600 rounded-xl p-6 shadow-enterprise",
      glass: "bg-obsidian-800/80 backdrop-blur-md border border-white/10 rounded-xl p-6 shadow-glass",
      glow: "bg-obsidian-800 border border-indigo-500/30 rounded-xl p-6 shadow-glow",
      gradient: "bg-gradient-to-tr from-obsidian-800 via-obsidian-900 to-indigo-950/40 border border-indigo-500/30 rounded-xl p-6 shadow-glow",
      interactive:
        "bg-obsidian-800 border border-obsidian-600 rounded-xl p-6 shadow-enterprise cursor-pointer hover:border-indigo-500/50 hover:shadow-glow transition-all duration-200",
    };

    return (
      <motion.div
        ref={ref}
        whileHover={variant === "interactive" ? { y: -2 } : undefined}
        className={cn(variants[variant], className)}
        {...props}
      >
        {children}
      </motion.div>
    );
  }
);

Card.displayName = "Card";

export const CardHeader = ({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col space-y-1.5 pb-4 border-b border-obsidian-600/50 mb-4", className)} {...props}>
    {children}
  </div>
);

export const CardTitle = ({ className, children, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3 className={cn("text-lg font-semibold leading-none tracking-tight text-white", className)} {...props}>
    {children}
  </h3>
);

export const CardDescription = ({ className, children, ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
  <p className={cn("text-sm text-slate-400", className)} {...props}>
    {children}
  </p>
);

export const CardContent = ({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("pt-0", className)} {...props}>
    {children}
  </div>
);

export const CardFooter = ({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex items-center pt-4 border-t border-obsidian-600/50 mt-4", className)} {...props}>
    {children}
  </div>
);
