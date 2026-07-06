import React, { useState } from "react";
import { Users, Plus, Shield, ArrowRight, BookOpen, Code2, Sparkles, CheckCircle2 } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";

interface Group {
  id: string;
  name: string;
  category: string;
  membersCount: number;
  description: string;
  isMember: boolean;
  meetingSchedule: string;
  tags: string[];
}

export const GroupsPage: React.FC = () => {
  const [groups, setGroups] = useState<Group[]>([
    {
      id: "grp-1",
      name: "Qdrant Vector DB & RAG Study Guild",
      category: "AI & Databases",
      membersCount: 142,
      description: "Dedicated campus circle exploring high-dimensional embedding spaces, HNSW graph parameters, and hybrid MySQL synchronization.",
      isMember: true,
      meetingSchedule: "Tuesdays 6:00 PM EST",
      tags: ["VectorDB", "Qdrant", "Python"],
    },
    {
      id: "grp-2",
      name: "Mastra Swarm Architects & Engineers",
      category: "Multi-Agent Systems",
      membersCount: 89,
      description: "Building production-ready tool routers, fallback loops, and asynchronous agent collaboration pipelines.",
      isMember: false,
      meetingSchedule: "Thursdays 5:00 PM EST",
      tags: ["Mastra", "Swarm", "Agents"],
    },
    {
      id: "grp-3",
      name: "Enkrypt Layer 6 Security & Governance",
      category: "AI Safety",
      membersCount: 64,
      description: "Auditing prompt injection defenses, PII redaction heuristics, and similarity interception boundaries.",
      isMember: false,
      meetingSchedule: "Fridays 3:00 PM EST",
      tags: ["Security", "Enkrypt", "ESDLC"],
    },
  ]);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [groupName, setGroupName] = useState("");
  const [groupCategory, setGroupCategory] = useState("AI & Databases");
  const [groupDesc, setGroupDesc] = useState("");
  const [groupSchedule, setGroupSchedule] = useState("");

  const handleCreateGroup = (e: React.FormEvent) => {
    e.preventDefault();
    if (!groupName.trim()) return;

    const newGrp: Group = {
      id: `grp-${Date.now()}`,
      name: groupName,
      category: groupCategory,
      membersCount: 1,
      description: groupDesc,
      isMember: true,
      meetingSchedule: groupSchedule || "TBD",
      tags: [groupCategory.split(" ")[0], "New"],
    };

    setGroups([newGrp, ...groups]);
    setIsModalOpen(false);
    setGroupName("");
    setGroupDesc("");
  };

  const toggleMembership = (id: string) => {
    setGroups((prev) =>
      prev.map((g) => {
        if (g.id !== id) return g;
        const newStatus = !g.isMember;
        return {
          ...g,
          isMember: newStatus,
          membersCount: g.membersCount + (newStatus ? 1 : -1),
        };
      })
    );
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <Users className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Collaborative Study Circles
          </Badge>
          <h1 className="text-3xl font-extrabold text-white">Academic Study Groups & Guilds</h1>
          <p className="text-sm text-slate-400">Join specialized campus circles, collaborate on AI student projects, and prepare for career technical evaluations.</p>
        </div>
        <Button variant="primary" onClick={() => setIsModalOpen(true)} className="px-5 py-2.5 self-start sm:self-center">
          <Plus className="w-4 h-4 mr-2" />
          Create New Guild
        </Button>
      </div>

      {/* Groups Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {groups.map((grp) => (
          <Card
            key={grp.id}
            variant={grp.isMember ? "glow" : "default"}
            className="p-6 flex flex-col justify-between space-y-6 transition-all hover:border-indigo-500/50"
          >
            <div className="space-y-3">
              <div className="flex justify-between items-start gap-2">
                <Badge variant="default" className="text-xs">{grp.category}</Badge>
                <span className="text-xs font-bold text-cyan-400 flex items-center gap-1">
                  <Users className="w-3.5 h-3.5" />
                  {grp.membersCount}
                </span>
              </div>

              <h3 className="text-lg font-bold text-white leading-snug">{grp.name}</h3>
              <p className="text-xs text-slate-300 leading-relaxed font-sans">{grp.description}</p>
              
              <div className="pt-2 text-xs text-slate-400 flex items-center gap-2">
                <span className="font-semibold text-white">Schedule:</span>
                <span>{grp.meetingSchedule}</span>
              </div>

              <div className="flex flex-wrap gap-1.5 pt-2">
                {grp.tags.map((tag) => (
                  <span key={tag} className="px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 text-[10px] border border-white/5">
                    #{tag}
                  </span>
                ))}
              </div>
            </div>

            <div className="pt-4 border-t border-white/10 flex items-center justify-between">
              {grp.isMember ? (
                <span className="inline-flex items-center gap-1.5 text-xs text-emerald-400 font-bold">
                  <CheckCircle2 className="w-4 h-4" />
                  Active Guild Member
                </span>
              ) : (
                <span className="text-xs text-slate-400">Open for Enrollment</span>
              )}

              <Button
                variant={grp.isMember ? "secondary" : "primary"}
                onClick={() => toggleMembership(grp.id)}
                className="text-xs px-4 py-2"
              >
                {grp.isMember ? "Leave Group" : "Join Guild"}
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Create Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create Study Group or Guild">
        <form onSubmit={handleCreateGroup} className="space-y-4 text-slate-300">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Group Name</label>
            <Input placeholder="e.g., Transformers & Attention Workshop" value={groupName} onChange={(e) => setGroupName(e.target.value)} required />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Category</label>
            <select
              value={groupCategory}
              onChange={(e) => setGroupCategory(e.target.value)}
              className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="AI & Databases">AI & Databases</option>
              <option value="Multi-Agent Systems">Multi-Agent Systems</option>
              <option value="AI Safety">AI Safety</option>
              <option value="Full-Stack Engineering">Full-Stack Engineering</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Meeting Schedule</label>
            <Input placeholder="e.g., Wednesdays at 7:00 PM EST" value={groupSchedule} onChange={(e) => setGroupSchedule(e.target.value)} />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Description & Objectives</label>
            <textarea
              rows={4}
              placeholder="Describe the study objectives and prerequisite courses..."
              value={groupDesc}
              onChange={(e) => setGroupDesc(e.target.value)}
              required
              className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div className="pt-4 flex justify-end gap-3">
            <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary">
              Create Guild
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
