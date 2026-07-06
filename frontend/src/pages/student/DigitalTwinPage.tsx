import React from "react";
import { BrainCircuit, Activity, Zap, ShieldCheck, Database, RefreshCw } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { DigitalTwinCard } from "@/components/widgets/DigitalTwinCard";
import { MemoryTimeline } from "@/components/widgets/MemoryTimeline";
import { ExplainabilityPanel } from "@/components/widgets/ExplainabilityPanel";
import { ConfidenceMeter } from "@/components/widgets/ConfidenceMeter";
import { useAuthStore } from "@/store/useAuthStore";

export const DigitalTwinPage: React.FC = () => {
  const { user } = useAuthStore();

  const memoryEvents = [
    { id: 1, timestamp: "10 mins ago", concept: "Mastra Swarm Routing", retrievalScore: 0.99, summary: "Indexed deterministic tool router definitions with 0% hallucination variance." },
    { id: 2, timestamp: "2 hours ago", concept: "Qdrant HNSW Parameters", retrievalScore: 0.94, summary: "Vector similarity search heuristics reviewed during Module 3 lab session." },
    { id: 3, timestamp: "Yesterday", concept: "Enkrypt Safety Interception", retrievalScore: 0.98, summary: "Passed 36/36 ESDLC regression checks during enterprise security verification." },
  ];

  const reasoningSteps = [
    { step: 1, title: "Syllabus Embedding Alignment", detail: "Compared student notes against authoritative course syllabus embedding #4092.", status: "passed" as const },
    { step: 2, title: "Velocity & Retention Calculation", detail: "Computed exponential moving average of quiz accuracy over last 14 days (2.8x velocity).", status: "passed" as const },
    { step: 3, title: "Hallucination & Safety Boundary", detail: "Enkrypt Layer 6 verified zero synthetic or off-topic knowledge assertions.", status: "passed" as const },
  ];

  return (
    <div className="space-y-8 py-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-obsidian-600 pb-6">
        <div>
          <div className="flex items-center space-x-2">
            <Badge variant="purple" size="sm">Cognitive Architecture</Badge>
            <Badge variant="cyan" size="sm">Real-Time Sync</Badge>
          </div>
          <h1 className="text-3xl font-extrabold text-white mt-1">My Student Digital Twin</h1>
          <p className="text-sm text-slate-400 mt-1">Live visualization of your persistent knowledge graph and cognitive retention heuristics.</p>
        </div>
        <Button size="md" variant="outline" leftIcon={<RefreshCw className="w-4 h-4" />}>
          Force Graph Re-Sync
        </Button>
      </div>

      <DigitalTwinCard
        studentName={user?.name || "Sujith"}
        healthScore={92}
        knowledgeMastery={84}
        studyVelocity={2.8}
        streakDays={14}
        status="healthy"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <MemoryTimeline events={memoryEvents} title="Recent Cognitive Memory Index (Qdrant Vector DB)" />

          <ExplainabilityPanel
            score={0.965}
            steps={reasoningSteps}
            model="Enkrypt Cognitive Verifier v6.2"
          />
        </div>

        <div className="space-y-6">
          <Card variant="default" className="p-6 space-y-6">
            <h3 className="font-bold text-sm text-white uppercase tracking-wider flex items-center gap-2">
              <Activity className="w-4 h-4 text-indigo-400" /> Retention Diagnostic
            </h3>
            <ConfidenceMeter score={0.92} label="Core Concept Retention" />
            <ConfidenceMeter score={0.88} label="Code Execution Competency" />
            <ConfidenceMeter score={0.99} label="Safety & Governance Compliance" />

            <div className="pt-4 border-t border-obsidian-600 space-y-2 text-xs text-slate-400">
              <div className="flex justify-between">
                <span>Vector Dimension:</span>
                <span className="font-mono text-white">1536 (OpenAI / Gemini)</span>
              </div>
              <div className="flex justify-between">
                <span>Memory Persistence:</span>
                <span className="font-mono text-emerald-400">Permanent (Qdrant Cloud)</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
