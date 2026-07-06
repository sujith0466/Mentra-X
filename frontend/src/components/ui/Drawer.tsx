import React, { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import { cn } from "@/utils/cn";

export interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  position?: "left" | "right";
  className?: string;
}

export const Drawer: React.FC<DrawerProps> = ({
  isOpen,
  onClose,
  title,
  children,
  position = "right",
  className,
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  const slideVariants = {
    right: { initial: { x: "100%" }, animate: { x: 0 }, exit: { x: "100%" } },
    left: { initial: { x: "-100%" }, animate: { x: 0 }, exit: { x: "-100%" } },
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-hidden">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-obsidian-900/80 backdrop-blur-sm"
          />
          <div className={cn("fixed inset-y-0 flex max-w-full", position === "right" ? "right-0 pl-10" : "left-0 pr-10")}>
            <motion.div
              variants={slideVariants[position]}
              initial="initial"
              animate="animate"
              exit="exit"
              transition={{ type: "spring", damping: 25, stiffness: 250 }}
              className={cn(
                "w-screen max-w-md bg-obsidian-800 border-l border-obsidian-600 shadow-2xl flex flex-col z-10",
                position === "left" && "border-r border-l-0",
                className
              )}
            >
              <div className="flex items-center justify-between px-6 py-4 border-b border-obsidian-600">
                {title && <h3 className="text-lg font-semibold text-white">{title}</h3>}
                <button
                  onClick={onClose}
                  className="text-slate-400 hover:text-white rounded-lg p-1 hover:bg-white/5 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="flex-1 overflow-y-auto p-6">{children}</div>
            </motion.div>
          </div>
        </div>
      )}
    </AnimatePresence>
  );
};
