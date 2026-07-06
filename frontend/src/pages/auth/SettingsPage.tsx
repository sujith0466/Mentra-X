import React, { useState } from "react";
import { Sliders, Bell, Shield, Lock, Trash2, Download, CheckCircle, Moon, Cpu } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";

export const SettingsPage: React.FC = () => {
  const [tutorMode, setTutorMode] = useState<"socratic" | "direct">("socratic");
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [streakReminders, setStreakReminders] = useState(true);
  const [shareTelemetry, setShareTelemetry] = useState(true);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleExport = () => {
    setExporting(true);
    setTimeout(() => {
      setExporting(false);
      alert("Your Qdrant semantic memory vectors and LMS transcript have been exported as mentra_data_export.json.");
    }, 1500);
  };

  return (
    <div className="max-w-4xl mx-auto py-10 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">Platform Preferences</Badge>
          <h1 className="text-3xl font-extrabold text-white">Account & AI Governance Settings</h1>
          <p className="text-sm text-slate-400">Configure your cognitive tutoring swarms, notification schedules, and GDPR privacy controls.</p>
        </div>
        {saved && (
          <span className="inline-flex items-center gap-1.5 text-xs text-emerald-400 font-semibold">
            <CheckCircle className="w-4 h-4" />
            Preferences Saved
          </span>
        )}
      </div>

      <div className="space-y-6">
        {/* AI Tutor Interaction Style */}
        <Card variant="default" className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Cpu className="w-5 h-5 text-indigo-400" />
                Mastra AI Tutoring Interaction Mode
              </h3>
              <p className="text-xs text-slate-400">
                Choose how autonomous tutoring swarms guide you through difficult concepts and coding challenges.
              </p>
            </div>
            <Badge variant={tutorMode === "socratic" ? "success" : "default"}>
              {tutorMode === "socratic" ? "Socratic Mentoring" : "Direct Solutions"}
            </Badge>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            <button
              onClick={() => setTutorMode("socratic")}
              className={`p-4 rounded-xl text-left border transition-all ${
                tutorMode === "socratic"
                  ? "bg-indigo-500/10 border-indigo-500/50 text-white shadow-md"
                  : "bg-obsidian-900 border-white/5 text-slate-400 hover:border-white/20"
              }`}
            >
              <h4 className="text-sm font-bold mb-1">Socratic Mentoring (Recommended)</h4>
              <p className="text-xs leading-relaxed opacity-80">
                The AI tutor asks probing questions and provides progressive hints to foster active critical thinking and long-term retention.
              </p>
            </button>

            <button
              onClick={() => setTutorMode("direct")}
              className={`p-4 rounded-xl text-left border transition-all ${
                tutorMode === "direct"
                  ? "bg-cyan-500/10 border-cyan-500/50 text-white shadow-md"
                  : "bg-obsidian-900 border-white/5 text-slate-400 hover:border-white/20"
              }`}
            >
              <h4 className="text-sm font-bold mb-1">Direct Solutions Mode</h4>
              <p className="text-xs leading-relaxed opacity-80">
                The AI tutor provides immediate code corrections and direct answers with concise theoretical explanations for fast review.
              </p>
            </button>
          </div>
        </Card>

        {/* Notifications & Reminders */}
        <Card variant="default" className="p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Bell className="w-5 h-5 text-cyan-400" />
            Notifications & Learning Reminders
          </h3>
          
          <div className="space-y-4 divide-y divide-white/10 text-sm">
            <div className="flex items-center justify-between pt-2">
              <div>
                <span className="font-semibold text-white block">Daily Study Streak Reminders</span>
                <span className="text-xs text-slate-400">Receive an email prompt if you haven't completed a lesson or quiz today.</span>
              </div>
              <input
                type="checkbox"
                checked={streakReminders}
                onChange={(e) => setStreakReminders(e.target.checked)}
                className="w-5 h-5 rounded bg-obsidian-900 border-white/20 text-indigo-500 focus:ring-0"
              />
            </div>

            <div className="flex items-center justify-between pt-4">
              <div>
                <span className="font-semibold text-white block">Course & Syllabus Announcements</span>
                <span className="text-xs text-slate-400">Receive alerts when new video lectures or coding challenges are published.</span>
              </div>
              <input
                type="checkbox"
                checked={emailAlerts}
                onChange={(e) => setEmailAlerts(e.target.checked)}
                className="w-5 h-5 rounded bg-obsidian-900 border-white/20 text-indigo-500 focus:ring-0"
              />
            </div>
          </div>
        </Card>

        {/* GDPR Privacy & Data Sovereignty */}
        <Card variant="default" className="p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Shield className="w-5 h-5 text-emerald-400" />
            GDPR Privacy & Data Sovereignty
          </h3>
          <p className="text-xs text-slate-400">
            You maintain full ownership over your Digital Twin vector embeddings, chat transcripts, and coding history.
          </p>

          <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
            <div>
              <span className="text-sm font-bold text-white block">Export Semantic Memory Vectors</span>
              <span className="text-xs text-slate-400">Download all your Qdrant knowledge state embeddings in JSON format.</span>
            </div>
            <Button variant="secondary" onClick={handleExport} disabled={exporting} className="text-xs py-2">
              <Download className="w-4 h-4 mr-1.5" />
              {exporting ? "Compiling Export..." : "Export Data Archive"}
            </Button>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-white/10">
            <div>
              <span className="text-sm font-bold text-red-400 block">Delete Academic Account & Twin</span>
              <span className="text-xs text-slate-400">Permanently erase your account, XP, course progress, and Qdrant embeddings.</span>
            </div>
            <Button variant="danger" onClick={() => setIsDeleteModalOpen(true)} className="text-xs py-2">
              <Trash2 className="w-4 h-4 mr-1.5" />
              Delete Account
            </Button>
          </div>
        </Card>

        <div className="flex justify-end pt-4">
          <Button variant="primary" onClick={handleSave} className="px-8 py-3">
            Save All Settings
          </Button>
        </div>
      </div>

      {/* Delete Modal */}
      <Modal isOpen={isDeleteModalOpen} onClose={() => setIsDeleteModalOpen(false)} title="Confirm Account Deletion">
        <div className="space-y-4 text-slate-300">
          <p className="text-sm">
            Are you absolutely certain you wish to delete your account? This action will permanently erase your Digital Twin graph, revoke access to all enterprise courses, and purge your vector embeddings from Qdrant.
          </p>
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-xs text-red-300">
            <strong>Warning:</strong> Institutional SLA compliance requires a 30-day grace period before irreversible storage purge.
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button variant="secondary" onClick={() => setIsDeleteModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="danger" onClick={() => { setIsDeleteModalOpen(false); alert("Account deletion request logged."); }}>
              Confirm Purge
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};
