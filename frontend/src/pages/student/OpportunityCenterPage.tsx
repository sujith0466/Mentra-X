import React, { useState, useEffect } from "react";
import {
  Sparkles,
  Briefcase,
  Trophy,
  Award,
  BookOpen,
  Filter,
  RefreshCw,
  Bell,
  CheckCircle2,
  Calendar,
  Search
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { OpportunityCard, MatchedOpportunity } from "@/components/opportunity/OpportunityCard";
import { SkillGapCard, SkillGapData } from "@/components/opportunity/SkillGapCard";
import {
  ResumeReadinessCard,
  ResumeReadinessData
} from "@/components/opportunity/ResumeReadinessCard";
import { TimelineCard, TimelineEntry } from "@/components/opportunity/TimelineCard";

interface OpportunityNotification {
  notification_id: string;
  title: string;
  message: string;
  category: string;
  action_url: string;
  created_at: string;
}

export const OpportunityCenterPage: React.FC = () => {
  const [activeCategory, setActiveCategory] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedSkillGapId, setSelectedSkillGapId] = useState<string | null>(null);

  const [feed, setFeed] = useState<MatchedOpportunity[]>([
    {
      opportunity: {
        opportunity_id: "opp-swe-google",
        title: "Google Software Engineering Summer Internship",
        organization: "Google Core AI",
        category: "INTERNSHIP",
        location: "Remote / Bangalore",
        stipend_or_reward: "$8,500 / mo + Mentorship",
        deadline: "2026-08-15",
        required_skills: ["Python", "Algorithms", "System Design"],
        description:
          "Work alongside Google AI researchers on highly scalable distributed LLM pipelines.",
        external_url: "https://careers.google.com/students"
      },
      match_percentage: 92.5,
      readiness_level: "IMMEDIATE_READY",
      explanations: [
        {
          factor: "Skill Alignment",
          impact: "POSITIVE",
          detail: "Strong proficiency in Python, Algorithms (+23.3%)",
          score_delta: 23.3
        },
        {
          factor: "Autonomous Learning Consistency",
          impact: "POSITIVE",
          detail: "High Habit Index (88.5/100) indicates strong follow-through (+12%)",
          score_delta: 12.0
        },
        {
          factor: "Prerequisite Gap",
          impact: "NEGATIVE",
          detail: "Missing required skills: System Design (-5%)",
          score_delta: -5.0
        }
      ],
      lifecycle_status: "RECOMMENDED"
    },
    {
      opportunity: {
        opportunity_id: "opp-hack-eth",
        title: "Global Open Source AI Global Hackathon",
        organization: "Mentra X & OpenSource Consortium",
        category: "HACKATHON",
        location: "Virtual / Global",
        stipend_or_reward: "$50,000 Prize Pool",
        deadline: "2026-07-28",
        required_skills: ["Python", "React", "Docker", "Machine Learning"],
        description:
          "Build agentic AI applications that solve critical educational equity bottlenecks.",
        external_url: "https://hackathon.mentrax.io"
      },
      match_percentage: 89.0,
      readiness_level: "IMMEDIATE_READY",
      explanations: [
        {
          factor: "Skill Alignment",
          impact: "POSITIVE",
          detail: "Verified Python, React, Machine Learning (+26.2%)",
          score_delta: 26.2
        }
      ],
      lifecycle_status: "APPLIED"
    },
    {
      opportunity: {
        opportunity_id: "opp-cert-aws",
        title: "AWS Certified Machine Learning Specialty Fellowship",
        organization: "Amazon Web Services Education",
        category: "CERTIFICATION",
        location: "Online Self-Paced",
        stipend_or_reward: "100% Exam Voucher + Cloud Credit",
        deadline: "2026-09-01",
        required_skills: ["Python", "Cloud Architecture", "Deep Learning"],
        description: "Official AWS certification track with sponsored cloud laboratory sandboxes.",
        external_url: "https://aws.amazon.com/certification"
      },
      match_percentage: 84.0,
      readiness_level: "NEAR_READY",
      explanations: [
        {
          factor: "ATS Resume Strength",
          impact: "POSITIVE",
          detail: "Resume formatting and keyword density score 82/100 (+8%)",
          score_delta: 8.0
        }
      ],
      lifecycle_status: "INTERESTED"
    }
  ]);

  const [timeline, setTimeline] = useState<TimelineEntry[]>([
    {
      entry_id: "tl-101",
      user_id: 1,
      opportunity_id: "opp-swe-google",
      opportunity_title: "Google Software Engineering Summer Internship",
      organization: "Google Core AI",
      status: "SAVED",
      updated_at: "2026-07-09 10:15",
      reminder_note: "Application deadline approaches in August 2026."
    },
    {
      entry_id: "tl-102",
      user_id: 1,
      opportunity_id: "opp-hack-eth",
      opportunity_title: "Global Open Source AI Global Hackathon",
      organization: "Mentra X & OpenSource Consortium",
      status: "APPLIED",
      updated_at: "2026-07-08 14:20",
      reminder_note: "Submission checkpoint scheduled for July 28, 2026."
    }
  ]);

  const [notifications, setNotifications] = useState<OpportunityNotification[]>([
    {
      notification_id: "notif-1",
      title: "High Opportunity Match (92.5%)",
      message:
        "You are strongly qualified for Google Software Engineering Summer Internship at Google Core AI.",
      category: "NEW_MATCH",
      action_url: "/student/opportunities",
      created_at: "Just now"
    }
  ]);

  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchOverview = async () => {
      try {
        setLoading(true);
        const res = await fetch("/api/v1/opportunity/overview");
        if (res.ok) {
          const json = await res.json();
          if (json?.data?.recommended_feed) {
            setFeed(json.data.recommended_feed);
          }
          if (json?.data?.timeline) {
            setTimeline(json.data.timeline);
          }
          if (json?.data?.notifications) {
            setNotifications(json.data.notifications);
          }
        }
      } catch {
        // Fallback silently to rich demo state
      } finally {
        setLoading(false);
      }
    };
    fetchOverview();
  }, []);

  const handleStatusChange = async (opportunityId: string, newStatus: string) => {
    // Optimistically update timeline state
    const target = feed.find((f) => f.opportunity.opportunity_id === opportunityId);
    if (target) {
      target.lifecycle_status = newStatus;
      setTimeline((prev) => [
        {
          entry_id: `tl-${Date.now()}`,
          user_id: 1,
          opportunity_id: opportunityId,
          opportunity_title: target.opportunity.title,
          organization: target.opportunity.organization,
          status: newStatus,
          updated_at: "Just now",
          reminder_note: `Updated status to ${newStatus}`
        },
        ...prev.filter((p) => p.opportunity_id !== opportunityId)
      ]);
    }

    try {
      await fetch("/api/v1/opportunity/status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ opportunity_id: opportunityId, status: newStatus })
      });
    } catch {
      // Ignore API error during offline demo
    }
  };

  const categories = [
    "ALL",
    "INTERNSHIP",
    "HACKATHON",
    "JOB",
    "SCHOLARSHIP",
    "CERTIFICATION",
    "RESEARCH"
  ];

  const filteredFeed = feed.filter((item) => {
    const matchesCategory =
      activeCategory === "ALL" || item.opportunity.category === activeCategory;
    const matchesSearch =
      !searchQuery ||
      item.opportunity.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.opportunity.organization.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const selectedOpportunityItem = feed.find(
    (item) => item.opportunity.opportunity_id === selectedSkillGapId
  ) || feed[0];

  const defaultSkillGap: SkillGapData = {
    opportunity_id: selectedOpportunityItem.opportunity.opportunity_id,
    current_skills: ["Python", "Algorithms"],
    missing_skills: ["System Design"],
    learning_path_steps: ["Complete 4-Module System Design & Load Balancing Path (System Design)"],
    estimated_readiness_days: 6,
    current_match_pct: selectedOpportunityItem.match_percentage,
    expected_match_after_remediation_pct: Math.min(98.0, selectedOpportunityItem.match_percentage + 5.5)
  };

  const defaultResumeReadiness: ResumeReadinessData = {
    opportunity_id: selectedOpportunityItem.opportunity.opportunity_id,
    ats_score: 84.0,
    matched_keywords: ["Python", "Algorithms", "Machine Learning"],
    missing_keywords: ["System Design", "Docker"],
    suggested_improvements: [
      "Embed targeted bullet points featuring keywords: System Design, Docker.",
      "Quantify project impact metrics (e.g., 'Reduced latency by 45%')."
    ],
    missing_projects_note:
      "Consider adding a capstone project explicitly showcasing: System Design, Docker."
  };

  return (
    <div className="space-y-8 py-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-obsidian-600 pb-6">
        <div>
          <div className="flex items-center space-x-2">
            <Badge variant="indigo" size="sm">
              <Sparkles className="w-3.5 h-3.5 mr-1" />
              Opportunity Intelligence Center
            </Badge>
            <Badge variant="success" size="sm">
              Continuous Multi-Provider Feed
            </Badge>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white mt-2">
            Opportunity Center
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
            Proactive AI matching that connects your Digital Twin, Weakness Profile, and Resume ATS
            readiness to internships, hackathons, certifications, and research programs.
          </p>
        </div>

        <Button
          size="md"
          variant="outline"
          leftIcon={<RefreshCw className="w-4 h-4" />}
          onClick={() => window.location.reload()}
        >
          Sync Real-Time Feed
        </Button>
      </div>

      {/* Proactive AI Notifications Banner */}
      {notifications.length > 0 && (
        <div className="p-4 rounded-xl bg-gradient-to-r from-indigo-500/10 via-purple-500/10 to-transparent border border-indigo-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-500 flex items-center justify-center text-white shrink-0">
              <Bell className="w-4 h-4" />
            </div>
            <div>
              <span className="text-sm font-bold text-slate-900 dark:text-white block">
                {notifications[0].title}
              </span>
              <span className="text-xs text-slate-600 dark:text-slate-300">
                {notifications[0].message}
              </span>
            </div>
          </div>
          <Badge variant="cyan" size="sm">
            AI Proactive Alert
          </Badge>
        </div>
      )}

      {/* Category Pills & Search Bar */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-1.5">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeCategory === cat
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "bg-slate-100 dark:bg-obsidian-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="relative w-full md:w-64">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search opportunities..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Main Grid: Feed (Left 2 cols) & Skill Gap + Resume Readiness (Right 1 col) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">
              Recommended Opportunity Feed
            </h2>
            <span className="text-xs font-semibold text-slate-400">
              Showing {filteredFeed.length} matches
            </span>
          </div>

          {filteredFeed.map((item) => (
            <OpportunityCard
              key={item.opportunity.opportunity_id}
              item={item}
              onStatusChange={handleStatusChange}
              onInspectSkillGap={(id) => setSelectedSkillGapId(id)}
            />
          ))}
        </div>

        <div className="space-y-6">
          <SkillGapCard
            data={defaultSkillGap}
            opportunityTitle={selectedOpportunityItem.opportunity.title}
          />

          <ResumeReadinessCard data={defaultResumeReadiness} />
        </div>
      </div>

      {/* Lifecycle Timeline Row */}
      <TimelineCard entries={timeline} onStatusChange={handleStatusChange} />
    </div>
  );
};
