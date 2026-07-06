import React, { useState } from "react";
import { LifeBuoy, MessageSquare, Send, CheckCircle, AlertCircle, FileText, PhoneCall } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";

export const HelpPage: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [ticketSubject, setTicketSubject] = useState("");
  const [ticketMessage, setTicketMessage] = useState("");
  const [ticketSubmitted, setTicketSubmitted] = useState(false);

  const handleSubmitTicket = (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticketSubject.trim() || !ticketMessage.trim()) return;
    setTicketSubmitted(true);
    setTimeout(() => {
      setIsModalOpen(false);
      setTicketSubmitted(false);
      setTicketSubject("");
      setTicketMessage("");
    }, 2000);
  };

  const helpTopics = [
    {
      title: "Getting Started & Onboarding",
      description: "How to set up your profile, take the initial DNA assessment, and enroll in your first course.",
      icon: FileText,
      link: "/docs",
    },
    {
      title: "AI Tutor & Study Planner",
      description: "Troubleshooting intelligent AI tutoring interactions or adjusting study schedule parameters.",
      icon: MessageSquare,
      link: "/faq",
    },
    {
      title: "Coding Arena & Sandboxes",
      description: "Resolving code compilation timeouts, terminal output errors, or automated test discrepancies.",
      icon: AlertCircle,
      link: "/faq",
    },
    {
      title: "Account, Billing & GDPR",
      description: "Managing subscription renewals, payment methods, exporting vector memory, or privacy requests.",
      icon: CheckCircle,
      link: "/contact",
    },
  ];

  return (
    <div className="min-h-screen py-16 px-4 sm:px-6 lg:px-8 space-y-16">
      {/* Hero */}
      <div className="max-w-4xl mx-auto text-center space-y-6">
        <Badge variant="info" className="px-3 py-1 text-xs">
          <LifeBuoy className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
          24/7 Enterprise Support
        </Badge>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight">
          How Can We <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Help You?</span>
        </h1>
        <p className="text-lg text-slate-300 max-w-2xl mx-auto">
          Our specialized support engineers and autonomous diagnostic agents are ready to assist with any technical or academic inquiries.
        </p>

        <div className="pt-4 flex flex-wrap justify-center gap-4">
          <Button variant="primary" onClick={() => setIsModalOpen(true)} className="px-6 py-3">
            <MessageSquare className="w-4 h-4 mr-2" />
            Submit Support Ticket
          </Button>
          <a href="#topics">
            <Button variant="secondary" className="px-6 py-3">
              Browse Help Topics
            </Button>
          </a>
        </div>
      </div>

      {/* Topics Grid */}
      <div id="topics" className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        {helpTopics.map((topic) => {
          const Icon = topic.icon;
          return (
            <Card key={topic.title} variant="default" className="p-6 flex items-start gap-5 hover:border-indigo-500/50 transition-all">
              <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center shrink-0">
                <Icon className="w-6 h-6 text-indigo-400" />
              </div>
              <div className="space-y-2 flex-1">
                <h3 className="text-lg font-bold text-white">{topic.title}</h3>
                <p className="text-sm text-slate-400 leading-relaxed">{topic.description}</p>
                <div className="pt-2">
                  <a href={topic.link} className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 inline-flex items-center gap-1">
                    Explore Guide &rarr;
                  </a>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Emergency Contact Card */}
      <div className="max-w-4xl mx-auto">
        <Card variant="gradient" className="p-8 flex flex-col sm:flex-row items-center justify-between gap-6 text-center sm:text-left">
          <div className="space-y-2">
            <Badge variant="success">Institutional SLAs Active</Badge>
            <h3 className="text-2xl font-bold text-white">Need Urgent Campus Assistance?</h3>
            <p className="text-sm text-slate-300">
              Enterprise Campus administrators have access to dedicated 1-hour response SLAs and direct phone escalation.
            </p>
          </div>
          <a href="tel:18005550199">
            <Button variant="secondary" className="px-6 py-3 whitespace-nowrap">
              <PhoneCall className="w-4 h-4 mr-2" />
              Call Enterprise Desk
            </Button>
          </a>
        </Card>
      </div>

      {/* Ticket Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Submit Support Ticket">
        {ticketSubmitted ? (
          <div className="p-8 text-center space-y-4">
            <CheckCircle className="w-12 h-12 text-emerald-400 mx-auto animate-bounce" />
            <h3 className="text-xl font-bold text-white">Ticket Submitted Successfully!</h3>
            <p className="text-sm text-slate-300">
              Your diagnostic telemetry has been captured. Support Ticket #TCK-{Math.floor(1000 + Math.random() * 9000)} has been dispatched to our support swarms.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmitTicket} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Subject</label>
              <Input
                placeholder="e.g., Code compilation timeout on Challenge #4"
                value={ticketSubject}
                onChange={(e) => setTicketSubject(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Message & Steps to Reproduce</label>
              <textarea
                rows={4}
                placeholder="Describe what occurred, any error messages displayed, and what you expected..."
                value={ticketMessage}
                onChange={(e) => setTicketMessage(e.target.value)}
                required
                className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div className="pt-4 flex justify-end gap-3">
              <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" variant="primary">
                <Send className="w-4 h-4 mr-2" />
                Submit Ticket
              </Button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
};
