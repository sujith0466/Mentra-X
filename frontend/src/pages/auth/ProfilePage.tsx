import React, { useState } from "react";
import { User, Award, Shield, Save, CheckCircle, Camera, Brain, BookOpen } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Badge } from "@/components/ui/Badge";
import { useAuthStore } from "@/store/useAuthStore";

export const ProfilePage: React.FC = () => {
  const { user, setUser } = useAuthStore();
  const [name, setName] = useState(user?.name || "Sujith Kumar");
  const [email, setEmail] = useState(user?.email || "sujith@mentrax.ai");
  const [bio, setBio] = useState("Computer Science engineering student specializing in Enterprise Architecture & AI Engineering.");
  const [githubUrl, setGithubUrl] = useState("https://github.com/sujith0466");
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    if (user && setUser) {
      setUser({ ...user, name, email });
    }
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="max-w-5xl mx-auto py-10 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">Academic Identity & DNA</Badge>
          <h1 className="text-3xl font-extrabold text-white">Student Profile & Settings</h1>
          <p className="text-sm text-slate-400">Manage your personal information, skill vectors, and institutional credentials.</p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" className="px-3 py-1">
            <Shield className="w-3.5 h-3.5 mr-1 inline" />
            Verified Student
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Left Column: Avatar & Summary Card */}
        <div className="space-y-6">
          <Card variant="glow" className="p-6 text-center space-y-4">
            <div className="relative w-24 h-24 mx-auto">
              <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-indigo-500 to-cyan-400 p-1">
                <div className="w-full h-full rounded-full bg-obsidian-950 flex items-center justify-center text-2xl font-bold text-white">
                  {name.charAt(0)}
                </div>
              </div>
              <button className="absolute bottom-0 right-0 p-2 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg border border-white/20 transition-all">
                <Camera className="w-4 h-4" />
              </button>
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">{name}</h3>
              <p className="text-xs text-slate-400">{email}</p>
            </div>
            <div className="pt-2 flex justify-center gap-2">
              <Badge variant="default">XP: 14,250</Badge>
              <Badge variant="success">Level 8</Badge>
            </div>
          </Card>

          <Card variant="default" className="p-6 space-y-4">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <Brain className="w-4 h-4 text-indigo-400" />
              Digital Twin Knowledge State
            </h4>
            <div className="space-y-3 text-xs text-slate-300">
              <div className="flex justify-between items-center">
                <span>Algorithmic Complexity</span>
                <span className="font-bold text-cyan-400">94%</span>
              </div>
              <div className="w-full h-1.5 bg-obsidian-900 rounded-full overflow-hidden">
                <div className="h-full bg-cyan-400 w-[94%]" />
              </div>

              <div className="flex justify-between items-center pt-1">
                <span>Vector Embeddings</span>
                <span className="font-bold text-indigo-400">88%</span>
              </div>
              <div className="w-full h-1.5 bg-obsidian-900 rounded-full overflow-hidden">
                <div className="h-full bg-indigo-400 w-[88%]" />
              </div>

              <div className="flex justify-between items-center pt-1">
                <span>Full-Stack Architecture</span>
                <span className="font-bold text-emerald-400">91%</span>
              </div>
              <div className="w-full h-1.5 bg-obsidian-900 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-400 w-[91%]" />
              </div>
            </div>
          </Card>
        </div>

        {/* Right Column: Edit Profile Form */}
        <div className="lg:col-span-2 space-y-6">
          <Card variant="default" className="p-8 space-y-6">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-bold text-white">Personal & Academic Details</h3>
              {saved && (
                <span className="inline-flex items-center gap-1.5 text-xs text-emerald-400 font-semibold animate-pulse">
                  <CheckCircle className="w-4 h-4" />
                  Profile Updated Successfully
                </span>
              )}
            </div>

            <form onSubmit={handleSave} className="space-y-5">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                    Full Name
                  </label>
                  <Input value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                    Institutional Email
                  </label>
                  <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                  Academic Bio / Research Focus
                </label>
                <textarea
                  rows={3}
                  value={bio}
                  onChange={(e) => setBio(e.target.value)}
                  className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                    GitHub / Portfolio URL
                  </label>
                  <Input value={githubUrl} onChange={(e) => setGithubUrl(e.target.value)} />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                    Academic Major
                  </label>
                  <Input value="B.S. in Computer Science (AI Track)" disabled className="opacity-70" />
                </div>
              </div>

              <div className="pt-4 border-t border-white/10 flex justify-end">
                <Button type="submit" variant="primary" className="px-6 py-2.5">
                  <Save className="w-4 h-4 mr-2" />
                  Save Changes
                </Button>
              </div>
            </form>
          </Card>
        </div>
      </div>
    </div>
  );
};
