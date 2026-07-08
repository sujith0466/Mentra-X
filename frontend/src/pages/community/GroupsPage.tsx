import React, { useState } from "react";
import { Users, Plus, CheckCircle2, BookOpen, Code2, Calendar } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { motion } from "framer-motion";

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
      name: "Database Systems & NLP Study Group",
      category: "AI & Databases",
      membersCount: 142,
      description: "Explore database design, SQL optimisation, natural language processing, and hybrid retrieval techniques together.",
      isMember: true,
      meetingSchedule: "Tuesdays 6:00 PM EST",
      tags: ["SQL", "NLP", "Python"],
    },
    {
      id: "grp-2",
      name: "AI App Builders",
      category: "AI Applications",
      membersCount: 89,
      description: "Learn to build robust AI applications and collaborate on open source projects.",
      isMember: false,
      meetingSchedule: "Thursdays 5:00 PM EST",
      tags: ["Projects", "AI", "Development"],
    },
    {
      id: "grp-3",
      name: "AI Safety & Ethics Group",
      category: "AI Safety",
      membersCount: 64,
      description: "Discussing best practices for building safe, ethical, and secure AI systems.",
      isMember: false,
      meetingSchedule: "Fridays 3:00 PM EST",
      tags: ["Security", "Safety", "Ethics"],
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
      meetingSchedule: groupSchedule || "Flexible schedule",
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
      <motion.div
        className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-white/10 pb-6"
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div>
          <Badge variant="info" className="mb-2">
            <Users className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Collaborative Study Circles
          </Badge>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">
            Study Groups
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Join subject-focused groups, collaborate on projects, and prep for technical interviews together.
          </p>
        </div>
        <Button
          variant="primary"
          onClick={() => setIsModalOpen(true)}
          className="px-5 py-2.5 self-start sm:self-center shrink-0"
        >
          <Plus className="w-4 h-4 mr-2" />
          Create Group
        </Button>
      </motion.div>

      {/* Groups Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {groups.map((grp, index) => (
          <motion.div
            key={grp.id}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, delay: index * 0.07 }}
          >
            <Card
              variant={grp.isMember ? "glow" : "default"}
              className="p-6 flex flex-col justify-between space-y-5 h-full hover:-translate-y-0.5 hover:shadow-md transition-all duration-200 border-slate-200 dark:border-white/8"
            >
              <div className="space-y-3">
                {/* Top row: category + member count */}
                <div className="flex justify-between items-center">
                  <Badge variant="default" className="text-xs">
                    {grp.category}
                  </Badge>
                  <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 dark:text-slate-400">
                    <Users className="w-3.5 h-3.5" />
                    {grp.membersCount.toLocaleString()} members
                  </span>
                </div>

                <h3 className="text-base font-bold text-slate-900 dark:text-white leading-snug">
                  {grp.name}
                </h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
                  {grp.description}
                </p>

                {/* Schedule */}
                <div className="flex items-center gap-2 text-xs text-slate-400">
                  <Calendar className="w-3.5 h-3.5 shrink-0 text-indigo-400" />
                  <span>
                    <span className="font-semibold text-slate-700 dark:text-slate-300">
                      Meets:
                    </span>{" "}
                    {grp.meetingSchedule}
                  </span>
                </div>

                {/* Tags */}
                <div className="flex flex-wrap gap-1.5">
                  {grp.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-300 text-[10px] font-semibold border border-indigo-100 dark:border-indigo-500/20"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              {/* Action row */}
              <div className="pt-4 border-t border-slate-100 dark:border-white/8 flex items-center justify-between gap-3">
                {grp.isMember ? (
                  <span className="inline-flex items-center gap-1.5 text-xs text-emerald-600 dark:text-emerald-400 font-semibold">
                    <CheckCircle2 className="w-4 h-4" />
                    Active Member
                  </span>
                ) : (
                  <span className="text-xs text-slate-400">Open to join</span>
                )}

                <Button
                  variant={grp.isMember ? "secondary" : "primary"}
                  onClick={() => toggleMembership(grp.id)}
                  className="text-xs px-4 py-2 shrink-0"
                >
                  {grp.isMember ? "Leave Group" : "Join Group"}
                </Button>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Create Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create a Study Group">
        <form onSubmit={handleCreateGroup} className="space-y-4 text-slate-600 dark:text-slate-300">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 dark:text-slate-300 mb-1">
              Group Name
            </label>
            <Input
              placeholder="e.g., Transformers & Attention Workshop"
              value={groupName}
              onChange={(e) => setGroupName(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 dark:text-slate-300 mb-1">
              Subject Area
            </label>
            <select
              value={groupCategory}
              onChange={(e) => setGroupCategory(e.target.value)}
              className="w-full bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="AI & Databases">AI & Databases</option>
              <option value="Advanced AI Systems">Advanced AI Systems</option>
              <option value="AI Safety">AI Safety</option>
              <option value="Full-Stack Engineering">Full-Stack Engineering</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 dark:text-slate-300 mb-1">
              Meeting Schedule
            </label>
            <Input
              placeholder="e.g., Wednesdays at 7:00 PM EST"
              value={groupSchedule}
              onChange={(e) => setGroupSchedule(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 dark:text-slate-300 mb-1">
              Description
            </label>
            <textarea
              rows={4}
              placeholder="What will your group study? Any prerequisite knowledge?"
              value={groupDesc}
              onChange={(e) => setGroupDesc(e.target.value)}
              required
              className="w-full bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
            />
          </div>
          <div className="pt-4 flex justify-end gap-3">
            <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary">
              Create Group
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
