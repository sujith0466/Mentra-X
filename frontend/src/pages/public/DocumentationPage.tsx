import React, { useState } from "react";
import { BookOpen, Code, Shield, Cpu, Terminal, ArrowRight, CheckCircle2 } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export const DocumentationPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"arch" | "api" | "security" | "sdk">("arch");

  const tabs = [
    { id: "arch", label: "Cognitive Architecture", icon: Cpu },
    { id: "api", label: "REST API & Webhooks", icon: Terminal },
    { id: "security", label: "Enkrypt Security Layer", icon: Shield },
    { id: "sdk", label: "Integration SDKs", icon: Code },
  ];

  return (
    <div className="min-h-screen py-16 px-4 sm:px-6 lg:px-8 space-y-12">
      {/* Header */}
      <div className="max-w-4xl mx-auto text-center space-y-6">
        <Badge variant="info" className="px-3 py-1 text-xs">
          <BookOpen className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
          Technical Specification & Reference
        </Badge>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Mentra X <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Documentation</span>
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
          Explore the architecture specifications, REST API schemas, vector memory integrations, and safety governance protocols powering our enterprise platform.
        </p>
      </div>

      {/* Navigation Tabs */}
      <div className="max-w-4xl mx-auto flex flex-wrap justify-center gap-2 border-b border-slate-200 dark:border-white/10 pb-4">
        {tabs.map((t) => {
          const Icon = t.icon;
          const isActive = activeTab === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id as any)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-semibold transition-all ${
                isActive
                  ? "bg-gradient-to-r from-indigo-600 to-cyan-600 text-slate-900 dark:text-white shadow-lg shadow-indigo-500/25"
                  : "bg-white dark:bg-obsidian-800/60 text-slate-400 hover:text-slate-900 dark:text-white hover:bg-slate-100 dark:bg-obsidian-700/60 border border-slate-200 dark:border-white/5"
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{t.label}</span>
            </button>
          );
        })}
      </div>

      {/* Content Panels */}
      <div className="max-w-5xl mx-auto">
        {activeTab === "arch" && (
          <div className="space-y-6">
            <Card variant="glow" className="p-8 space-y-6">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Cpu className="w-6 h-6 text-indigo-400" />
                Multi-Layered Cognitive Swarm Architecture
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                Mentra X decouples user presentation from cognitive AI orchestration. The application is structured into distinct, deterministic layers designed for zero latency spikes and maximum resilience:
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10 space-y-2">
                  <h3 className="text-sm font-bold text-cyan-400">1. Single Page Application (SPA) Layer</h3>
                  <p className="text-xs text-slate-400">
                    Built on React 18, TypeScript, Vite, and Tailwind CSS. State is managed deterministically via Zustand and TanStack Query with optimistic UI mutations.
                  </p>
                </div>
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10 space-y-2">
                  <h3 className="text-sm font-bold text-indigo-400">2. Flask WSGI & REST API Layer</h3>
                  <p className="text-xs text-slate-400">
                    High-performance Python 3.11 monolith handling authentication, RBAC authorization, session persistence, and API request routing (`/api/v1/*`).
                  </p>
                </div>
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10 space-y-2">
                  <h3 className="text-sm font-bold text-emerald-400">3. Hybrid Relational & Vector Storage</h3>
                  <p className="text-xs text-slate-400">
                    MySQL 8.0 manages 46+ structured tables (users, courses, enrollments). Qdrant Vector Database indexes high-dimensional student semantic memory embeddings.
                  </p>
                </div>
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10 space-y-2">
                  <h3 className="text-sm font-bold text-purple-400">4. Mastra Cognitive Swarms</h3>
                  <p className="text-xs text-slate-400">
                    Specialized agents (Career AI, Tutor AI, DevTools AI) execute tool calling with deterministic prompt versioning and zero hallucination variance.
                  </p>
                </div>
              </div>
            </Card>
          </div>
        )}

        {activeTab === "api" && (
          <div className="space-y-6">
            <Card variant="default" className="p-8 space-y-6">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Terminal className="w-6 h-6 text-cyan-400" />
                Enterprise REST API Endpoints
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-300">
                All API requests require a valid JWT Bearer token or authenticated HTTP-only session cookie. Endpoints return standard JSON payloads with explicit error codes.
              </p>

              <div className="space-y-4">
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 font-mono text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-emerald-400 font-bold">GET /api/v1/courses</span>
                    <Badge variant="success">Authenticated</Badge>
                  </div>
                  <p className="text-slate-400 font-sans">Returns paginated course catalog with syllabus module counts and skill difficulty vectors.</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 font-mono text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-indigo-400 font-bold">POST /student/api/twin/mutate</span>
                    <Badge variant="info">Digital Twin</Badge>
                  </div>
                  <p className="text-slate-400 font-sans">Accepts quiz attempt or coding submission telemetry to recalculate student mastery vectors in Qdrant.</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 font-mono text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-cyan-400 font-bold">POST /api/v1/ai/tutor</span>
                    <Badge variant="default">Mastra Swarm</Badge>
                  </div>
                  <p className="text-slate-400 font-sans">Executes Socratic tutoring swarm query with Enkrypt safety interceptor verification.</p>
                </div>
              </div>
            </Card>
          </div>
        )}

        {activeTab === "security" && (
          <div className="space-y-6">
            <Card variant="gradient" className="p-8 space-y-6">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Shield className="w-6 h-6 text-emerald-400" />
                Enkrypt Security Layer 6 Protocols
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                Mentra X embeds Enkrypt Layer 6 directly into the runtime execution pipeline. No AI response bypasses security validation.
              </p>

              <ul className="space-y-3 text-sm text-slate-600 dark:text-slate-300 pt-2">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <strong className="text-slate-900 dark:text-white">Real-Time Hallucination Interception:</strong> Every AI claim is verified against authoritative course embeddings using cosine similarity thresholds (&gt;0.85 required).
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <strong className="text-slate-900 dark:text-white">PII & Credentials Redaction:</strong> Student personal identifiers, passwords, and API keys are automatically stripped from prompts before swarm dispatch.
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <strong className="text-slate-900 dark:text-white">Prompt Injection Defense:</strong> Semantic heuristics block adversarial jailbreaks or attempts to override system pedagogical directives.
                  </div>
                </li>
              </ul>
            </Card>
          </div>
        )}

        {activeTab === "sdk" && (
          <div className="space-y-6">
            <Card variant="glass" className="p-8 space-y-6">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Code className="w-6 h-6 text-purple-400" />
                Mentra X Integration SDKs & Integrations
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-300">
                Integrate Mentra X cognitive twins into institutional LMS portals (Canvas, Moodle, Blackboard) via our standard Python and TypeScript client libraries.
              </p>

              <div className="p-4 rounded-xl bg-white dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 font-mono text-xs text-slate-600 dark:text-slate-300 overflow-x-auto">
                <code>
                  # Install Mentra X Python SDK<br />
                  pip install mentra-x-sdk<br /><br />
                  from mentra_sdk import MentraClient<br />
                  client = MentraClient(api_key="mx_live_89a7f...")<br /><br />
                  # Query student twin mastery state<br />
                  state = client.twin.get_knowledge_state(student_id="stu_010")<br />
                  print(f"Overall Competency: &#123;state.competency_score&#125;%")
                </code>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};
