import React, { useState } from "react";
import { KeyRound, Mail, ArrowLeft, CheckCircle, Shield } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Link } from "react-router-dom";

export const ForgotPasswordPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return;
    setSubmitted(true);
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-12">
      <Card variant="glass" className="w-full max-w-md p-8 space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mx-auto mb-4">
            <KeyRound className="w-6 h-6 text-indigo-400" />
          </div>
          <h1 className="text-2xl font-extrabold text-white">Reset Account Password</h1>
          <p className="text-sm text-slate-400">
            Enter your student or faculty email address and we will dispatch a secure Enkrypt verification link.
          </p>
        </div>

        {submitted ? (
          <div className="p-6 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-center space-y-3">
            <CheckCircle className="w-10 h-10 text-emerald-400 mx-auto" />
            <h3 className="text-base font-bold text-white">Verification Link Sent!</h3>
            <p className="text-xs text-slate-300">
              If an active Mentra X account exists for <strong className="text-white">{email}</strong>, a password reset link has been dispatched. Please check your inbox and spam folder.
            </p>
            <div className="pt-2">
              <Link to="/login">
                <Button variant="secondary" className="w-full justify-center text-xs">
                  Return to Login
                </Button>
              </Link>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
                <Input
                  type="email"
                  placeholder="e.g., student@campus.edu"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="pl-10 w-full"
                />
              </div>
            </div>

            <Button type="submit" variant="primary" className="w-full justify-center py-3">
              Send Verification Link
            </Button>
          </form>
        )}

        <div className="pt-4 border-t border-white/10 text-center flex justify-between items-center text-xs text-slate-400">
          <Link to="/login" className="hover:text-white inline-flex items-center gap-1">
            <ArrowLeft className="w-3.5 h-3.5" />
            Back to Login
          </Link>
          <span className="inline-flex items-center gap-1 text-emerald-400">
            <Shield className="w-3.5 h-3.5" />
            Enkrypt SSL
          </span>
        </div>
      </Card>
    </div>
  );
};
