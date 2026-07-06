import React, { useState } from "react";
import { Send, CheckCircle2, Mail, Phone, MapPin } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

export const ContactPage: React.FC = () => {
  const [submitted, setSubmitted] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !message) return;
    setSubmitted(true);
  };

  return (
    <div className="py-8 max-w-4xl mx-auto space-y-12">
      <div className="text-center space-y-3">
        <h1 className="text-3xl font-extrabold text-white">Connect With Our Engineering Team</h1>
        <p className="text-sm text-slate-400">Have questions about Mentra X enterprise licensing, custom AI swarms, or security?</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="space-y-6 md:col-span-1">
          <Card variant="default" className="space-y-4">
            <div className="flex items-center space-x-3 text-sm text-slate-300">
              <Mail className="w-5 h-5 text-indigo-400 shrink-0" />
              <span>enterprise@mentrax.ai</span>
            </div>
            <div className="flex items-center space-x-3 text-sm text-slate-300">
              <Phone className="w-5 h-5 text-emerald-400 shrink-0" />
              <span>+1 (800) MENTRA-AI</span>
            </div>
            <div className="flex items-center space-x-3 text-sm text-slate-300">
              <MapPin className="w-5 h-5 text-amber-400 shrink-0" />
              <span>Silicon Valley AI Research Labs, USA</span>
            </div>
          </Card>
        </div>

        <div className="md:col-span-2">
          <Card variant="glass" className="p-6">
            {submitted ? (
              <div className="py-12 text-center space-y-4">
                <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto animate-bounce" />
                <h3 className="text-xl font-bold text-white">Inquiry Received</h3>
                <p className="text-sm text-slate-300">Our enterprise solutions architect will respond within 24 hours.</p>
                <Button size="sm" variant="outline" onClick={() => setSubmitted(false)}>Send Another Message</Button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <Input label="Full Name" placeholder="Dr. Elena Rostova" value={name} onChange={(e) => setName(e.target.value)} required />
                <Input label="Enterprise Email" type="email" placeholder="elena@university.edu" value={email} onChange={(e) => setEmail(e.target.value)} required />
                <div className="flex flex-col space-y-1.5">
                  <label className="text-sm font-medium text-slate-300">How can we help?</label>
                  <textarea
                    rows={4}
                    placeholder="Describe your AI learning or integration requirements..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    required
                    className="w-full rounded-lg bg-obsidian-900 border border-obsidian-600 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                  />
                </div>
                <Button type="submit" size="md" className="w-full" rightIcon={<Send className="w-4 h-4" />}>
                  Submit Enterprise Inquiry
                </Button>
              </form>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
