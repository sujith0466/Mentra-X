import React from "react";
import { ArrowUpRight, ArrowDownRight, Users, Activity, Zap, Shield, Check, DollarSign } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { cn } from "@/utils/cn";

export interface MetricCardProps {
  title: string;
  value: string | number;
  trend?: number;
  trendLabel?: string;
  change?: string;
  isPositive?: boolean;
  icon?: React.ReactNode | string;
  subtitle?: string;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  trend,
  trendLabel = "vs last month",
  change,
  isPositive: customIsPositive,
  icon,
  subtitle,
  className,
}) => {
  const isPositive = customIsPositive !== undefined ? customIsPositive : (trend !== undefined && trend >= 0);
  const showBadge = trend !== undefined || change !== undefined;

  const renderIcon = () => {
    if (!icon) return null;
    if (typeof icon === "string") {
      const iconMap: Record<string, React.ReactNode> = {
        users: <Users className="w-5 h-5" />,
        activity: <Activity className="w-5 h-5" />,
        zap: <Zap className="w-5 h-5" />,
        shield: <Shield className="w-5 h-5" />,
        check: <Check className="w-5 h-5" />,
        dollar: <DollarSign className="w-5 h-5" />,
      };
      return iconMap[icon] || null;
    }
    return icon;
  };

  return (
    <Card variant="interactive" className={cn("flex flex-col justify-between p-5", className)}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-400">{title}</span>
        {icon && <div className="p-2 rounded-lg bg-white/5 text-primary-500">{renderIcon()}</div>}
      </div>

      <div className="mt-4 flex items-baseline justify-between">
        <div className="flex flex-col">
          <span className="text-2xl font-bold tracking-tight text-white">{value}</span>
          {subtitle && <span className="text-xs text-slate-500 mt-0.5">{subtitle}</span>}
        </div>

        {showBadge && (
          <div
            className={cn(
              "flex items-center space-x-1 text-xs font-semibold px-2 py-1 rounded-full",
              isPositive
                ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
            )}
          >
            {isPositive ? <ArrowUpRight className="w-3.5 h-3.5" /> : <ArrowDownRight className="w-3.5 h-3.5" />}
            {trend !== undefined ? (
              <>
                <span>{Math.abs(trend)}%</span>
                <span className="text-[10px] text-slate-500 ml-1 hidden sm:inline">{trendLabel}</span>
              </>
            ) : (
              <span>{change}</span>
            )}
          </div>
        )}
      </div>
    </Card>
  );
};
