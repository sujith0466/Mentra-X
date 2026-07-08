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
    <Card
      variant="glass"
      className="w-full p-8 space-y-6 rounded-2xl shadow-2xl border border-slate-200/60 dark:border-white/8 bg-white/90 dark:bg-obsidian-800/90 backdrop-blur-xl"
    >
      {/* Heading */}
      <div className="text-center space-y-1.5">
        <h2 className="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white">
          Create your account
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Start learning smarter with your personalised AI study plan.
        </p>
      </div>

      <form onSubmit={handleRegister} className="space-y-4">
        <Input
          label="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter your full name"
          leftIcon={<User className="w-4 h-4" />}
          required
        />
        <Input
          label="Email Address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@university.edu"
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

        {/* Role selector */}
        <div className="space-y-2">
          <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
            I am joining as a…
          </label>
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => setRole("student")}
              className={`p-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-2 transition-all duration-150 ${
                role === "student"
                  ? "bg-indigo-600/10 border-indigo-500 text-indigo-700 dark:text-indigo-300 shadow-sm"
                  : "bg-slate-50 dark:bg-obsidian-900 border-slate-200 dark:border-obsidian-600 text-slate-500 dark:text-slate-400 hover:border-slate-300 dark:hover:border-obsidian-500"
              }`}
            >
              <BrainCircuit className="w-4 h-4 text-indigo-500 dark:text-indigo-400" />
              Student
            </button>
            <button
              type="button"
              onClick={() => setRole("instructor")}
              className={`p-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-2 transition-all duration-150 ${
                role === "instructor"
                  ? "bg-indigo-600/10 border-indigo-500 text-indigo-700 dark:text-indigo-300 shadow-sm"
                  : "bg-slate-50 dark:bg-obsidian-900 border-slate-200 dark:border-obsidian-600 text-slate-500 dark:text-slate-400 hover:border-slate-300 dark:hover:border-obsidian-500"
              }`}
            >
              <UserPlus className="w-4 h-4 text-violet-500 dark:text-violet-400" />
              Instructor
            </button>
          </div>
        </div>

        <Button
          type="submit"
          size="lg"
          className="w-full mt-2 font-bold tracking-wide"
          isLoading={isLoading}
          leftIcon={<UserPlus className="w-4 h-4" />}
        >
          Create My Account
        </Button>
      </form>

      {/* Divider */}
      <div className="relative flex items-center gap-3">
        <div className="flex-1 border-t border-slate-200 dark:border-white/10" />
        <span className="text-[11px] text-slate-400 font-medium uppercase tracking-wider">or</span>
        <div className="flex-1 border-t border-slate-200 dark:border-white/10" />
      </div>

      <p className="text-sm text-center text-slate-500 dark:text-slate-400">
        Already have an account?{" "}
        <Link
          to="/login"
          className="text-indigo-600 dark:text-indigo-400 font-semibold hover:underline underline-offset-2"
        >
          Sign in here
        </Link>
      </p>
    </Card>
  );
};
