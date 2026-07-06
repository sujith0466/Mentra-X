import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { LogIn, Mail, Lock, Sparkles } from "lucide-react";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { useAuthStore } from "@/store/useAuthStore";

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("sujith@mentrax.ai");
  const [password, setPassword] = useState("password123");
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
      if (email.includes("admin")) {
        setUser({
          id: "adm_001",
          name: "Sujith Admin",
          email: email,
          role: "admin",
        });
        navigate("/admin/dashboard");
      } else {
        setUser({
          id: "stu_101",
          name: "Sujith Kumar",
          email: email,
          role: "student",
          twin_id: "twin_alpha_99",
        });
        navigate("/student/dashboard");
      }
    }, 800);
  };

  const handleQuickDemo = (role: "student" | "admin") => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      if (role === "admin") {
        setUser({ id: "adm_001", name: "Sujith Admin", email: "admin@mentrax.ai", role: "admin" });
        navigate("/admin/dashboard");
      } else {
        setUser({ id: "stu_101", name: "Sujith Kumar", email: "sujith@mentrax.ai", role: "student", twin_id: "twin_alpha_99" });
        navigate("/student/dashboard");
      }
    }, 500);
  };

  return (
    <Card variant="glass" className="w-full space-y-6 p-8 shadow-2xl">
      <div className="text-center space-y-1">
        <h2 className="text-2xl font-bold text-white">Sign In to Your Account</h2>
        <p className="text-xs text-slate-400">Access your Digital Twin and AI adaptive study tools.</p>
      </div>

      {error && (
        <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-xs text-rose-300 text-center">
          {error}
        </div>
      )}

      <form onSubmit={handleLogin} className="space-y-4">
        <Input
          label="Email Address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          leftIcon={<Mail className="w-4 h-4" />}
          required
        />
        <Input
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          leftIcon={<Lock className="w-4 h-4" />}
          required
        />

        <Button type="submit" size="lg" className="w-full mt-2" isLoading={isLoading} leftIcon={<LogIn className="w-4 h-4" />}>
          Sign In
        </Button>
      </form>

      <div className="pt-4 border-t border-obsidian-600/60 space-y-3">
        <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 block text-center">
          Instant Enterprise Demo Access
        </span>
        <div className="grid grid-cols-2 gap-3">
          <Button size="sm" variant="outline" onClick={() => handleQuickDemo("student")} leftIcon={<Sparkles className="w-3.5 h-3.5 text-indigo-400" />}>
            Student Portal
          </Button>
          <Button size="sm" variant="outline" onClick={() => handleQuickDemo("admin")} leftIcon={<Sparkles className="w-3.5 h-3.5 text-amber-400" />}>
            Admin Operations
          </Button>
        </div>
      </div>

      <p className="text-xs text-center text-slate-400">
        Don&apos;t have an account?{" "}
        <Link to="/register" className="text-primary-500 font-semibold hover:underline">
          Create one now
        </Link>
      </p>
    </Card>
  );
};
