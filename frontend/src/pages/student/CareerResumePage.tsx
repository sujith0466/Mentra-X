import React, { useState } from "react";
import { Briefcase, Upload, Sparkles, CheckCircle2, TrendingUp } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { AIResponseCard } from "@/components/widgets/AIResponseCard";
import { ChartComponent } from "@/components/widgets/ChartComponent";

export const CareerResumePage: React.FC = () => {
  const [analyzing, setAnalyzing] = useState(false);
  const [analyzed, setAnalyzed] = useState(true);

  const handleUpload = () => {
    setAnalyzing(true);
    setTimeout(() => {
      setAnalyzing(false);
      setAnalyzed(true);
    }, 1200);
  };

  const skillGaps = [
    { label: "React 18 & TypeScript", value: 95, color: "from-emerald-500 to-teal-400" },
    { label: "Mastra Swarm Orchestration", value: 85, color: "from-primary-600 to-indigo-400" },
    { label: "Qdrant Vector Engineering", value: 80, color: "from-ai-violet to-purple-500" },
    { label: "Kubernetes Enterprise Scaling", value: 65, color: "from-amber-500 to-orange-400" },
  ];

  return (
    <div className="space-y-8 py-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-obsidian-600 pb-6">
        <div>
          <div className="flex items-center space-x-2">
            <Badge variant="cyan" size="sm">AI Career Navigator</Badge>
          </div>
          <h1 className="text-3xl font-extrabold text-white mt-1">Resume Analyzer & Career Roadmap</h1>
          <p className="text-sm text-slate-400 mt-1">Match your Digital Twin competencies against live enterprise job market vectors.</p>
        </div>
        <Button size="md" onClick={handleUpload} isLoading={analyzing} leftIcon={<Upload className="w-4 h-4" />}>
          Upload New Resume (.pdf)
        </Button>
      </div>

      {analyzed && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <AIResponseCard
              title="Mastra Career Diagnostic Report"
              content="Your resume demonstrates strong competency in frontend architecture and state management. To reach the Principal AI Solutions Architect salary band ($240k+), we recommend closing your skill gap in Kubernetes cluster autoscaling."
              confidenceScore={0.97}
              modelName="Gemini-2.5-Pro-Career"
            />

            <ChartComponent
              title="Skill Mastery vs Enterprise Target Role"
              data={skillGaps}
              type="bar"
            />

            <Card variant="default" className="p-6 space-y-4">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-emerald-400" /> Personalized Career Roadmap
              </h3>
              <div className="space-y-4">
                {[
                  { step: "Step 1: Immediate Action", desc: "Complete Module 4 of Vector Memory Systems to achieve 90%+ Qdrant competency.", status: "In Progress" },
                  { step: "Step 2: Portfolio Polish", desc: "Deploy your Enkrypt Safety Layer demo to Vercel and link it in your GitHub README.", status: "Recommended" },
                  { step: "Step 3: Mock Technical Interview", desc: "Run a 30-minute system design simulation with our Mastra Interview Agent.", status: "Unlocked" },
                ].map((item, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-obsidian-900 border border-obsidian-600 flex items-start justify-between">
                    <div>
                      <h4 className="font-semibold text-sm text-white">{item.step}</h4>
                      <p className="text-xs text-slate-400 mt-1">{item.desc}</p>
                    </div>
                    <Badge variant={item.status === "In Progress" ? "primary" : "purple"}>{item.status}</Badge>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          <div className="space-y-6">
            <Card variant="glow" className="p-6 space-y-4">
              <h3 className="font-bold text-sm text-white uppercase tracking-wider">Target Role Compatibility</h3>
              <div className="text-4xl font-extrabold text-emerald-400">88.5%</div>
              <p className="text-xs text-slate-400">Matched against Senior AI Frontend Engineer roles at Tier-1 tech enterprises.</p>
              <div className="pt-4 border-t border-obsidian-600 space-y-2 text-xs text-slate-300">
                <div className="flex items-center justify-between">
                  <span>Avg Salary Band</span>
                  <span className="font-bold text-white">$180k - $240k</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Market Demand</span>
                  <span className="font-bold text-emerald-400">Very High (99th %tile)</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};
