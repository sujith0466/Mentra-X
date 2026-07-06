import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import { Drawer } from "@/components/ui/Drawer";
import { AIResponseCard } from "@/components/widgets/AIResponseCard";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Toast, ToastMessage } from "@/components/feedback/Toast";
import { useUIStore } from "@/store/useUIStore";
import { useAuthStore } from "@/store/useAuthStore";
import { Send, Sparkles, ShieldCheck } from "lucide-react";

export const AppLayout: React.FC = () => {
  const { isChatOpen, toggleChat } = useUIStore();
  const { user } = useAuthStore();
  const [messages, setMessages] = useState<Array<{ id: number; role: "user" | "ai"; content: string }>>([
    {
      id: 1,
      role: "ai",
      content: `Hello ${user?.name || "Student"}! I am your Intelligent AI Assistant. Your Digital Twin is synced and AI Safety Verification is active. How can I assist your studies today?`,
    },
  ]);
  const [inputVal, setInputVal] = useState("");
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const handleSend = () => {
    if (!inputVal.trim()) return;
    const userMsg = { id: Date.now(), role: "user" as const, content: inputVal };
    setMessages((prev) => [...prev, userMsg]);
    setInputVal("");

    setTimeout(() => {
      const aiReply = {
        id: Date.now() + 1,
        role: "ai" as const,
        content: `I analyzed your query: "${userMsg.content}" through your personalized learning memory. I recommend reviewing Module 3 of the Cloud Architecture syllabus to reinforce your understanding.`,
      };
      setMessages((prev) => [...prev, aiReply]);
    }, 1000);
  };

  const handleDismissToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <div className="min-h-screen bg-obsidian-900 text-slate-100 flex flex-col font-sans">
      <Navbar />
      <div className="flex flex-1 relative">
        {user && <Sidebar />}
        <main className="flex-1 p-6 md:p-8 overflow-y-auto max-w-7xl mx-auto w-full">
          <Outlet />
        </main>
      </div>

      <Drawer isOpen={isChatOpen} onClose={toggleChat} title="Intelligent AI Tutoring Assistant" position="right">
        <div className="flex flex-col h-[calc(100vh-8rem)] justify-between space-y-4">
          <div className="flex items-center justify-between p-2 rounded-lg bg-obsidian-900 border border-white/5 text-xs text-slate-400">
            <span className="flex items-center gap-1.5 text-indigo-400">
              <Sparkles className="w-3.5 h-3.5" /> AI Engine: Adaptive Intelligence v2.5
            </span>
            <span className="flex items-center gap-1 text-cyan-400">
              <ShieldCheck className="w-3.5 h-3.5" /> Safety Validated
            </span>
          </div>

          <div className="flex-1 overflow-y-auto space-y-4 pr-1">
            {messages.map((m) =>
              m.role === "ai" ? (
                <AIResponseCard key={m.id} content={m.content} safetyStatus="APPROVE" confidenceScore={0.98} />
              ) : (
                <div key={m.id} className="flex justify-end">
                  <div className="bg-primary-600 text-white p-3 rounded-xl rounded-tr-none max-w-[85%] text-sm shadow-md shadow-indigo-500/10">
                    {m.content}
                  </div>
                </div>
              )
            )}
          </div>

          <div className="flex items-center space-x-2 pt-3 border-t border-obsidian-600">
            <Input
              placeholder="Ask anything about your courses..."
              value={inputVal}
              onChange={(e) => setInputVal(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <Button size="md" onClick={handleSend} className="shrink-0">
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </Drawer>

      <Toast messages={toasts} onDismiss={handleDismissToast} />
    </div>
  );
};
