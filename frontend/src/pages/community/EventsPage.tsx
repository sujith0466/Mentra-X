import React, { useState } from "react";
import { Calendar, Clock, MapPin, Video, Users, Plus, CheckCircle, ExternalLink, Sparkles } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";

interface EventItem {
  id: string;
  title: string;
  speaker: string;
  date: string;
  time: string;
  location: string;
  isVirtual: boolean;
  attendeesCount: number;
  description: string;
  isRSVPed: boolean;
  tag: string;
}

export const EventsPage: React.FC = () => {
  const [events, setEvents] = useState<EventItem[]>([
    {
      id: "ev-1",
      title: "Live Masterclass: Scaling Qdrant Vector Memory to 10M Nodes",
      speaker: "Dr. Aris Thorne (Chief Vector Architect)",
      date: "July 15, 2026",
      time: "2:00 PM - 3:30 PM EST",
      location: "Virtual Webinar (Zoom)",
      isVirtual: true,
      attendeesCount: 342,
      description: "Explore advanced HNSW quantization techniques, distributed shard rebalancing, and hybrid MySQL synchronization for enterprise AI applications.",
      isRSVPed: true,
      tag: "Masterclass",
    },
    {
      id: "ev-2",
      title: "AI Agent Hackathon: Build an Autonomous Assistant in 48 Hours",
      speaker: "Mentra X DevTools Team",
      date: "July 22, 2026",
      time: "9:00 AM EST Kickoff",
      location: "MIT Stata Center & Discord Stream",
      isVirtual: false,
      attendeesCount: 510,
      description: "Compete for $10,000 in cloud credits by engineering deterministic multi-agent engines with verifiable AI Safety boundaries.",
      isRSVPed: false,
      tag: "Hackathon",
    },
    {
      id: "ev-3",
      title: "Enterprise AI Security Audit & Compliance Panel",
      speaker: "Sarah Jenkins & AI Safety Architects",
      date: "August 5, 2026",
      time: "1:00 PM - 2:00 PM EST",
      location: "Virtual Stream",
      isVirtual: true,
      attendeesCount: 188,
      description: "A deep dive into GDPR privacy exports, PII redaction heuristics, and similarity interception protocols in production environments.",
      isRSVPed: false,
      tag: "Panel",
    },
  ]);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newSpeaker, setNewSpeaker] = useState("");
  const [newDate, setNewDate] = useState("");
  const [newDesc, setNewDesc] = useState("");

  const handleCreateEvent = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    const added: EventItem = {
      id: `ev-${Date.now()}`,
      title: newTitle,
      speaker: newSpeaker || "Community Speaker",
      date: newDate || "Upcoming",
      time: "6:00 PM EST",
      location: "Virtual Stream",
      isVirtual: true,
      attendeesCount: 1,
      description: newDesc,
      isRSVPed: true,
      tag: "Community Workshop",
    };

    setEvents([added, ...events]);
    setIsModalOpen(false);
    setNewTitle("");
    setNewSpeaker("");
    setNewDesc("");
  };

  const toggleRSVP = (id: string) => {
    setEvents((prev) =>
      prev.map((ev) => {
        if (ev.id !== id) return ev;
        const newStatus = !ev.isRSVPed;
        return {
          ...ev,
          isRSVPed: newStatus,
          attendeesCount: ev.attendeesCount + (newStatus ? 1 : -1),
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
            <Calendar className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Campus & Virtual Schedule
          </Badge>
          <h1 className="text-3xl font-extrabold text-white">Upcoming Events & Live Workshops</h1>
          <p className="text-sm text-slate-400">Join live webinars, hackathons, and guest lectures from industry AI leaders.</p>
        </div>
        <Button variant="primary" onClick={() => setIsModalOpen(true)} className="px-5 py-2.5 self-start sm:self-center">
          <Plus className="w-4 h-4 mr-2" />
          Host Event
        </Button>
      </div>

      {/* Events List */}
      <div className="space-y-6">
        {events.map((ev) => (
          <Card key={ev.id} variant={ev.isRSVPed ? "glow" : "default"} className="p-6 sm:p-8 transition-all hover:border-white/20">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
              <div className="space-y-3 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant="default" className="text-xs">{ev.tag}</Badge>
                  <span className="text-xs font-bold text-cyan-400 flex items-center gap-1">
                    <Users className="w-3.5 h-3.5" />
                    {ev.attendeesCount} Registered
                  </span>
                  <span className="text-slate-500">&bull;</span>
                  <span className="text-xs text-slate-400 font-semibold">{ev.speaker}</span>
                </div>

                <h3 className="text-xl sm:text-2xl font-bold text-white">{ev.title}</h3>
                <p className="text-sm text-slate-300 leading-relaxed max-w-3xl font-sans">{ev.description}</p>

                <div className="flex flex-wrap items-center gap-6 pt-2 text-xs text-slate-300">
                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-indigo-400" />
                    <span className="font-bold text-white">{ev.date}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-cyan-400" />
                    <span>{ev.time}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {ev.isVirtual ? <Video className="w-4 h-4 text-emerald-400" /> : <MapPin className="w-4 h-4 text-red-400" />}
                    <span>{ev.location}</span>
                  </div>
                </div>
              </div>

              <div className="shrink-0 flex flex-col sm:flex-row lg:flex-col items-start sm:items-center lg:items-end justify-between gap-3 pt-4 lg:pt-0 border-t lg:border-t-0 border-white/10">
                {ev.isRSVPed && (
                  <span className="inline-flex items-center gap-1.5 text-xs text-emerald-400 font-bold bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
                    <CheckCircle className="w-3.5 h-3.5" />
                    RSVP Confirmed
                  </span>
                )}
                <Button
                  variant={ev.isRSVPed ? "secondary" : "primary"}
                  onClick={() => toggleRSVP(ev.id)}
                  className="w-full sm:w-auto px-6 py-3 text-xs font-bold"
                >
                  {ev.isRSVPed ? "Cancel Registration" : "RSVP Now & Add to Calendar"}
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Host Event Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Host an Academic Workshop">
        <form onSubmit={handleCreateEvent} className="space-y-4 text-slate-300">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Event Title</label>
            <Input placeholder="e.g., Intro to Transformers Lab Session" value={newTitle} onChange={(e) => setNewTitle(e.target.value)} required />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Speaker / Host Name</label>
            <Input placeholder="e.g., Prof. Sarah Jenkins" value={newSpeaker} onChange={(e) => setNewSpeaker(e.target.value)} />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Date & Time</label>
            <Input placeholder="e.g., July 30, 2026 at 4:00 PM EST" value={newDate} onChange={(e) => setNewDate(e.target.value)} />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Description & Prerequisites</label>
            <textarea
              rows={4}
              placeholder="Provide agenda and required background knowledge..."
              value={newDesc}
              onChange={(e) => setNewDesc(e.target.value)}
              required
              className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div className="pt-4 flex justify-end gap-3">
            <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary">
              Publish Event
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
