import React, { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, AlertCircle, Info, X } from "lucide-react";
import { cn } from "@/utils/cn";

export interface ToastMessage {
  id: string;
  type?: "success" | "error" | "info";
  title: string;
  description?: string;
}

export interface ToastProps {
  messages: ToastMessage[];
  onDismiss: (id: string) => void;
}

export const Toast: React.FC<ToastProps> = ({ messages, onDismiss }) => {
  useEffect(() => {
    if (messages.length > 0) {
      const timer = setTimeout(() => {
        onDismiss(messages[0].id);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [messages, onDismiss]);

  const icons = {
    success: <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />,
    error: <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />,
    info: <Info className="w-5 h-5 text-indigo-400 shrink-0" />,
  };

  const borders = {
    success: "border-emerald-500/30",
    error: "border-rose-500/30",
    info: "border-indigo-500/30",
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col space-y-2 max-w-sm w-full pointer-events-none">
      <AnimatePresence>
        {messages.map((msg) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, x: 100, scale: 0.95 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className={cn(
              "pointer-events-auto flex items-start justify-between p-4 rounded-xl bg-white dark:bg-obsidian-800/90 backdrop-blur-md border shadow-glass",
              borders[msg.type || "info"]
            )}
          >
            <div className="flex items-start space-x-3">
              {icons[msg.type || "info"]}
              <div>
                <h4 className="text-sm font-semibold text-slate-900 dark:text-white">{msg.title}</h4>
                {msg.description && <p className="text-xs text-slate-600 dark:text-slate-300 mt-0.5">{msg.description}</p>}
              </div>
            </div>
            <button
              onClick={() => onDismiss(msg.id)}
              className="text-slate-400 hover:text-slate-900 dark:text-white p-1 rounded hover:bg-white/5 transition-colors ml-2"
            >
              <X className="w-4 h-4" />
            </button>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};
