import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { UserPlus, Mail, Lock, User, BrainCircuit } from "lucide-react";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { useAuthStore } from "@/store/useAuthStore";

export const RegisterPage: React.FC = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<"student" | "instructor">("student");
  const [isLoading, setIsLoading] = useState(false);
  const { setUser } = useAuthStore();
  const navigate = useNavigate();

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      setUser({
        id: `stu_${Date.now()}`,
        name: name || "New Student",
        email: email,
        role: role,
        twin_id: `twin_${Math.floor(Math.random() * 1000)}`,
      });
      navigate("/student/dashboard");
    }, 800);
  };

  return (
    <Card variant="glass" className="w-full space-y-6 p-8 shadow-2xl">
      <div className="text-center space-y-1">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Create Enterprise Account</h2>
        <p className="text-xs text-slate-600 dark:text-slate-400">Initialize your personal AI Digital Twin and learning graph.</p>
      </div>

      <form onSubmit={handleRegister} className="space-y-4">
        <Input
          label="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Sujith Kumar"
          leftIcon={<User className="w-4 h-4" />}
          required
        />
        <Input
          label="Email Address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="sujith@mentrax.ai"
          leftIcon={<Mail className="w-4 h-4" />}
          required
        />
        <Input
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          leftIcon={<Lock className="w-4 h-4" />}
          required
        />

        <div className="space-y-1.5">
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Account Role</label>
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => setRole("student")}
              className={`p-3 rounded-lg border text-xs font-semibold flex items-center justify-center gap-2 transition-all ${
                role === "student"
                  ? "bg-primary-600/20 border-primary-500 text-slate-900 dark:text-white shadow-sm"
                  : "bg-slate-100 dark:bg-obsidian-900 border-slate-300 dark:border-obsidian-600 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
              }`}
            >
              <BrainCircuit className="w-4 h-4 text-indigo-500 dark:text-indigo-400" /> Student / Learner
            </button>
            <button
              type="button"
              onClick={() => setRole("instructor")}
              className={`p-3 rounded-lg border text-xs font-semibold flex items-center justify-center gap-2 transition-all ${
                role === "instructor"
                  ? "bg-primary-600/20 border-primary-500 text-slate-900 dark:text-white shadow-sm"
                  : "bg-slate-100 dark:bg-obsidian-900 border-slate-300 dark:border-obsidian-600 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
              }`}
            >
              <UserPlus className="w-4 h-4 text-ai-violet" /> Instructor / Faculty
            </button>
          </div>
        </div>

        <Button type="submit" size="lg" className="w-full mt-4 font-bold" isLoading={isLoading} leftIcon={<UserPlus className="w-4 h-4" />}>
          Register & Initialize Twin
        </Button>
      </form>

      <p className="text-xs text-center text-slate-600 dark:text-slate-400">
        Already registered?{" "}
        <Link to="/login" className="text-primary-600 dark:text-primary-500 font-semibold hover:underline">
          Sign In here
        </Link>
      </p>
    </Card>
  );
};
