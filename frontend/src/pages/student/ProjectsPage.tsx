import React, { useState } from "react";
import { FolderGit2, Plus, Sparkles, CheckCircle, Clock, ArrowRight, Code2, Terminal, Shield } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";

interface Project {
  id: string;
  title: string;
  domain: string;
  difficulty: string;
  description: string;
  progress: number;
  milestones: { title: string; completed: boolean }[];
  techStack: string[];
}

export const ProjectsPage: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([
    {
      id: "proj-01",
      title: "Autonomous RAG Knowledge Assistant with Vector Memory",
      domain: "Generative AI & Semantic Memory",
      difficulty: "Advanced",
      description: "Build an enterprise document ingestion pipeline that chunks markdown specifications, embeds them using OpenAI text-embedding-3-large, and serves cosine similarity queries via REST API and Vector Memory.",
      progress: 65,
      milestones: [
        { title: "Initialize REST API & Vector Collection", completed: true },
        { title: "Implement Recursive Character Text Chunking Pipeline", completed: true },
        { title: "Connect AI Safety Prompt Injection Defense", completed: false },
        { title: "Deploy Frontend Chat Widget with Citation Badges", completed: false },
      ],
      techStack: ["Python", "Flask", "VectorDB", "React", "TypeScript"],
    },
    {
      id: "proj-02",
      title: "Real-Time Student Telemetry Dashboard & Cognitive Twin",
      domain: "Full-Stack Enterprise Analytics",
      difficulty: "Intermediate",
      description: "Develop a reactive student progress monitor using Zustand state management, Tailwind CSS glassmorphism, and Recharts visualization components with zero layout shifts.",
      progress: 100,
      milestones: [
        { title: "Design Figma & Tailwind Design Token System", completed: true },
        { title: "Implement Zustand Persistent Authentication Store", completed: true },
        { title: "Integrate Recharts Exponential Moving Average Charts", completed: true },
      ],
      techStack: ["React 18", "Vite", "Tailwind CSS", "Zustand"],
    },
    {
      id: "proj-03",
      title: "Deterministic Tool Router for Multi-Agent Swarms",
      domain: "Multi-Agent Swarm Architecture",
      difficulty: "Expert",
      description: "Engineer a high-performance orchestration engine where specialized LLM agents dynamically invoke external database tools with strict JSON schema validation and fallback retry loops.",
      progress: 25,
      milestones: [
        { title: "Define Deterministic Tool Schemas with Pydantic", completed: true },
        { title: "Implement Multi-Agent Swarm Router Logic", completed: false },
        { title: "Simulate Concurrency Stress Tests under Heavy Load", completed: false },
      ],
      techStack: ["Python 3.11", "Multi-Agent Engine", "Pydantic", "AsyncIO"],
    },
  ]);

  const [activeProjectId, setActiveProjectId] = useState<string>("proj-01");
  const [isGeneratorOpen, setIsGeneratorOpen] = useState(false);
  const [genDomain, setGenDomain] = useState("AI & Machine Learning");
  const [genDifficulty, setGenDifficulty] = useState("Intermediate");
  const [generating, setGenerating] = useState(false);

  const activeProject = projects.find((p) => p.id === activeProjectId) || projects[0];

  const handleGenerateProject = (e: React.FormEvent) => {
    e.preventDefault();
    setGenerating(true);
    setTimeout(() => {
      const newProj: Project = {
        id: `proj-${Date.now()}`,
        title: `AI-Powered ${genDomain} Synthesizer Engine`,
        domain: genDomain,
        difficulty: genDifficulty,
        description: `An autonomous end-to-end ${genDomain.toLowerCase()} application tailored to your current Digital Twin mastery vectors. Features real-time telemetry and AI safety validation.`,
        progress: 0,
        milestones: [
          { title: "Project Architecture Blueprint & Schema Setup", completed: false },
          { title: "Core Algorithmic Logic & Vector Index Integration", completed: false },
          { title: "Unit Testing & ESDLC Regression Suite", completed: false },
        ],
        techStack: ["TypeScript", "Python", "VectorDB", "Vite"],
      };
      setProjects([newProj, ...projects]);
      setActiveProjectId(newProj.id);
      setGenerating(false);
      setIsGeneratorOpen(false);
    }, 1500);
  };

  const toggleMilestone = (milestoneIdx: number) => {
    setProjects((prev) =>
      prev.map((p) => {
        if (p.id !== activeProjectId) return p;
        const updatedMilestones = p.milestones.map((m, idx) =>
          idx === milestoneIdx ? { ...m, completed: !m.completed } : m
        );
        const completedCount = updatedMilestones.filter((m) => m.completed).length;
        const newProgress = Math.round((completedCount / updatedMilestones.length) * 100);
        return { ...p, milestones: updatedMilestones, progress: newProgress };
      })
    );
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <FolderGit2 className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            AI Project Builder & Portfolio Engine
          </Badge>
          <h1 className="text-3xl font-extrabold text-white">Student Project Studio</h1>
          <p className="text-sm text-slate-400">Build production-grade AI systems, track milestone progress, and enrich your academic GitHub portfolio.</p>
        </div>
        <Button variant="primary" onClick={() => setIsGeneratorOpen(true)} className="px-5 py-2.5 self-start sm:self-center">
          <Sparkles className="w-4 h-4 mr-2 text-cyan-400" />
          AI Project Generator
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Left Column: Projects List */}
        <div className="space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 px-1">Your Active Projects</h3>
          <div className="space-y-3">
            {projects.map((proj) => {
              const isActive = proj.id === activeProjectId;
              return (
                <Card
                  key={proj.id}
                  variant={isActive ? "glow" : "default"}
                  onClick={() => setActiveProjectId(proj.id)}
                  className={`p-5 cursor-pointer transition-all border ${
                    isActive ? "border-indigo-500/50 shadow-lg" : "border-white/5 hover:border-white/15"
                  }`}
                >
                  <div className="flex justify-between items-start gap-2 mb-2">
                    <Badge variant={proj.progress === 100 ? "success" : "info"}>{proj.difficulty}</Badge>
                    <span className="text-xs font-bold text-slate-400">{proj.progress}%</span>
                  </div>
                  <h4 className="text-base font-bold text-white mb-1 line-clamp-1">{proj.title}</h4>
                  <p className="text-xs text-indigo-400 font-semibold mb-3">{proj.domain}</p>
                  
                  {/* Progress Bar */}
                  <div className="w-full h-1.5 bg-obsidian-900 rounded-full overflow-hidden border border-white/5">
                    <div
                      className={`h-full transition-all duration-300 ${proj.progress === 100 ? "bg-emerald-400" : "bg-gradient-to-r from-indigo-500 to-cyan-400"}`}
                      style={{ width: `${proj.progress}%` }}
                    />
                  </div>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Right Column: Project Detail & Milestone Tracker */}
        <div className="lg:col-span-2">
          {activeProject && (
            <Card variant="default" className="p-8 space-y-8">
              {/* Top Banner */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-white/10">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="default">{activeProject.domain}</Badge>
                    <Badge variant={activeProject.progress === 100 ? "success" : "info"}>
                      {activeProject.progress === 100 ? "Completed" : "In Progress"}
                    </Badge>
                  </div>
                  <h2 className="text-2xl sm:text-3xl font-extrabold text-white pt-1">{activeProject.title}</h2>
                </div>
                <div className="text-right">
                  <span className="text-3xl font-extrabold text-cyan-400">{activeProject.progress}%</span>
                  <span className="block text-xs text-slate-400 uppercase tracking-wider">Milestone Velocity</span>
                </div>
              </div>

              {/* Description & Tech Stack */}
              <div className="space-y-4">
                <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300">Project Overview</h3>
                <p className="text-sm text-slate-300 leading-relaxed font-sans">{activeProject.description}</p>
                
                <div className="pt-2 flex flex-wrap gap-2 items-center">
                  <span className="text-xs font-semibold text-slate-400 mr-2">Tech Stack:</span>
                  {activeProject.techStack.map((tech) => (
                    <span key={tech} className="px-2.5 py-1 rounded-md bg-obsidian-900 text-cyan-300 text-xs font-mono border border-white/10">
                      {tech}
                    </span>
                  ))}
                </div>
              </div>

              {/* Milestone Tracker */}
              <div className="space-y-4 pt-4 border-t border-white/10">
                <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-emerald-400" />
                  Milestone Progress Roadmap
                </h3>
                
                <div className="space-y-3">
                  {activeProject.milestones.map((ms, idx) => (
                    <div
                      key={ms.title}
                      onClick={() => toggleMilestone(idx)}
                      className={`p-4 rounded-xl border flex items-center justify-between gap-4 cursor-pointer transition-all ${
                        ms.completed
                          ? "bg-emerald-500/10 border-emerald-500/30 text-white"
                          : "bg-obsidian-900/60 border-white/10 text-slate-300 hover:border-white/20"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <input
                          type="checkbox"
                          checked={ms.completed}
                          onChange={() => {}}
                          className="w-5 h-5 rounded bg-obsidian-950 border-white/20 text-emerald-500 focus:ring-0 cursor-pointer"
                        />
                        <span className={`text-sm font-semibold ${ms.completed ? "line-through text-slate-400" : "text-white"}`}>
                          {ms.title}
                        </span>
                      </div>
                      {ms.completed && <Badge variant="success" className="text-[10px]">Verified</Badge>}
                    </div>
                  ))}
                </div>
              </div>

              {/* Actions Footer */}
              <div className="pt-6 border-t border-white/10 flex flex-wrap justify-between items-center gap-4">
                <span className="text-xs text-slate-400 inline-flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5 text-indigo-400" />
                  Code assertions verified by AI Safety Layer
                </span>
                <div className="flex gap-3">
                  <Button variant="secondary" className="text-xs py-2">
                    <Code2 className="w-4 h-4 mr-1.5" />
                    Open Sandbox Workspace
                  </Button>
                  <Button variant="primary" className="text-xs py-2">
                    Submit Project for Review
                    <ArrowRight className="w-4 h-4 ml-1.5" />
                  </Button>
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>

      {/* Generator Modal */}
      <Modal isOpen={isGeneratorOpen} onClose={() => setIsGeneratorOpen(false)} title="AI Project Generator">
        <form onSubmit={handleGenerateProject} className="space-y-5 text-slate-300">
          <p className="text-sm">
            Select your preferred domain and target difficulty. Our intelligent AI assistant will formulate an end-to-end project specification tailored to your learning mastery profile.
          </p>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              Technical Domain
            </label>
            <select
              value={genDomain}
              onChange={(e) => setGenDomain(e.target.value)}
              className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="AI & Machine Learning">AI & Machine Learning</option>
              <option value="Full-Stack Web Systems">Full-Stack Web Systems</option>
              <option value="Cloud Native & Kubernetes">Cloud Native & Kubernetes</option>
              <option value="Cybersecurity & Encryption">Cybersecurity & Encryption</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              Target Difficulty Tier
            </label>
            <select
              value={genDifficulty}
              onChange={(e) => setGenDifficulty(e.target.value)}
              className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="Beginner">Beginner (Foundations & Syntax)</option>
              <option value="Intermediate">Intermediate (Full-Stack & APIs)</option>
              <option value="Advanced">Advanced (Vector DBs & Swarms)</option>
              <option value="Expert">Expert (Kernel & Distributed Systems)</option>
            </select>
          </div>
          <div className="pt-4 flex justify-end gap-3">
            <Button type="button" variant="secondary" onClick={() => setIsGeneratorOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" disabled={generating}>
              <Sparkles className="w-4 h-4 mr-1.5" />
              {generating ? "Swarm Generating Blueprint..." : "Generate AI Project"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
