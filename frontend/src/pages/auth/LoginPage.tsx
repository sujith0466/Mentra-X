import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { LogIn, Mail, Lock } from "lucide-react";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { useAuthStore } from "@/store/useAuthStore";

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { setUser } = useAuthStore();
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    setTimeout(() => {
      setIsLoading(false);
      const nameFromEmail = email.split("@")[0].replace(".", " ");
      const formattedName = nameFromEmail.charAt(0).toUpperCase() + nameFromEmail.slice(1);
      
      if (email.includes("admin")) {
        setUser({
          id: "adm_001",
          name: formattedName || "Enterprise Administrator",
          email: email,
          role: "admin",
        });
        navigate("/admin/dashboard");
      } else {
        setUser({
          id: "stu_101",
          name: formattedName || "Authenticated Learner",
          email: email,
          role: "student",
          twin_id: "twin_alpha_99",
        });
        navigate("/student/dashboard");
      }
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
          Welcome back
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Sign in to continue your learning journey.
        </p>
      </div>

      {/* Error banner */}
      {error && (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 text-xs text-rose-600 dark:text-rose-300">
          <span className="shrink-0">⚠️</span>
          {error}
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleLogin} className="space-y-4">
        <Input
          label="Email Address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@university.edu"
          leftIcon={<Mail className="w-4 h-4" />}
          required
        />
        <div className="space-y-1">
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            leftIcon={<Lock className="w-4 h-4" />}
            required
          />
          <div className="flex justify-end">
            <button
              type="button"
              className="text-[11px] text-indigo-600 dark:text-indigo-400 hover:underline font-medium"
            >
              Forgot password?
            </button>
          </div>
        </div>

        <Button
          type="submit"
          size="lg"
          className="w-full mt-1 font-bold tracking-wide"
          isLoading={isLoading}
          leftIcon={<LogIn className="w-4 h-4" />}
        >
          Sign In
        </Button>
      </form>

      {/* Divider */}
      <div className="relative flex items-center gap-3">
        <div className="flex-1 border-t border-slate-200 dark:border-white/10" />
        <span className="text-[11px] text-slate-400 font-medium uppercase tracking-wider">or</span>
        <div className="flex-1 border-t border-slate-200 dark:border-white/10" />
      </div>

      {/* Footer */}
      <p className="text-sm text-center text-slate-500 dark:text-slate-400">
        Don&apos;t have an account?{" "}
        <Link
          to="/register"
          className="text-indigo-600 dark:text-indigo-400 font-semibold hover:underline underline-offset-2"
        >
          Create one — it&apos;s free
        </Link>
      </p>
    </Card>
  );
};
