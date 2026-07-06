import React, { useState } from "react";
import { motion } from "framer-motion";
import { Check, Sparkles, Zap, Shield, Award, ArrowRight } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Link } from "react-router-dom";

export const PricingPage: React.FC = () => {
  const [billingCycle, setBillingCycle] = useState<"monthly" | "annual">("annual");

  const plans = [
    {
      name: "Student Starter",
      price: billingCycle === "annual" ? "0" : "0",
      period: "forever",
      description: "Essential AI tutoring and basic Digital Twin DNA tracking for individual learners.",
      badge: "Free Forever",
      variant: "default" as const,
      features: [
        "Access to 5+ Core AI & Computer Science Courses",
        "Standard Cognitive Digital Twin Graph",
        "50 AI Tutor Interactions / day",
        "Community Discussion Forum Access",
        "Standard Progress Tracking",
      ],
      cta: "Get Started Free",
      link: "/register",
    },
    {
      name: "Scholar Pro",
      price: billingCycle === "annual" ? "19" : "29",
      period: "per month",
      description: "Advanced cognitive swarms, unlimited code sandbox, and career mock interviews.",
      badge: "Most Popular",
      variant: "glow" as const,
      features: [
        "Unlimited Access to All Enterprise Courses",
        "Real-Time Adaptive Digital Twin Mutation",
        "Unlimited Intelligent AI Tutoring Assistant",
        "Interactive Coding Arena & Debug Assistant",
        "AI Career Roadmap & Mock Interview Scoring",
        "Personalized Learning Memory Timeline Sync",
        "Priority AI Safety Verification",
      ],
      cta: "Start 14-Day Pro Trial",
      link: "/register?plan=pro",
    },
    {
      name: "Enterprise Campus",
      price: "Custom",
      period: "per institution",
      description: "Full university deployment with administrative governance, custom syllabuses, and analytics.",
      badge: "Institutional",
      variant: "gradient" as const,
      features: [
        "Everything in Scholar Pro for All Students",
        "Dedicated Admin Operations & Telemetry Console",
        "Custom Course & Video Ingestion Engine",
        "Institutional AI Observability & Safety Logs",
        "GDPR Privacy Export & Compliance Governance",
        "Dedicated Enterprise Success Architect",
        "Custom Domain & SSO Integration",
      ],
      cta: "Contact Campus Sales",
      link: "/contact",
    },
  ];

  return (
    <div className="min-h-screen py-16 px-4 sm:px-6 lg:px-8 space-y-16">
      {/* Hero Header */}
      <div className="max-w-4xl mx-auto text-center space-y-6">
        <Badge variant="info" className="px-3 py-1 text-xs">
          <Sparkles className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
          Transparent Enterprise Pricing
        </Badge>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight">
          Invest in Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Cognitive AI Future</span>
        </h1>
        <p className="text-lg text-slate-300 max-w-2xl mx-auto">
          Choose the plan that fits your academic journey or campus infrastructure. Scale seamlessly with our deterministic multi-agent tutoring swarms.
        </p>

        {/* Billing Toggle */}
        <div className="flex items-center justify-center gap-4 pt-4">
          <span className={`text-sm font-semibold ${billingCycle === "monthly" ? "text-white" : "text-slate-400"}`}>
            Monthly Billing
          </span>
          <button
            type="button"
            onClick={() => setBillingCycle(billingCycle === "monthly" ? "annual" : "monthly")}
            className="w-14 h-8 flex items-center bg-obsidian-800 rounded-full p-1 border border-white/10 transition-colors focus:outline-none"
          >
            <motion.div
              layout
              className="w-6 h-6 bg-indigo-500 rounded-full shadow-md"
              animate={{ x: billingCycle === "annual" ? 24 : 0 }}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            />
          </button>
          <span className={`text-sm font-semibold flex items-center gap-1.5 ${billingCycle === "annual" ? "text-white" : "text-slate-400"}`}>
            Annual Billing
            <span className="bg-emerald-500/20 text-emerald-400 text-xs px-2 py-0.5 rounded-full border border-emerald-500/30">
              Save 35%
            </span>
          </span>
        </div>
      </div>

      {/* Pricing Cards */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">
        {plans.map((plan, idx) => (
          <motion.div
            key={plan.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.15 }}
            className="flex flex-col"
          >
            <Card variant={plan.variant} className="p-8 flex flex-col justify-between h-full space-y-8 relative overflow-hidden">
              {plan.variant === "glow" && (
                <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl pointer-events-none" />
              )}
              
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-xl font-bold text-white">{plan.name}</h3>
                  <Badge variant={plan.variant === "glow" ? "success" : "default"}>{plan.badge}</Badge>
                </div>
                <p className="text-sm text-slate-400 min-h-[40px]">{plan.description}</p>
                
                <div className="pt-2">
                  <span className="text-4xl font-extrabold text-white">${plan.price}</span>
                  {plan.price !== "Custom" && <span className="text-slate-400 text-sm ml-1">/ {plan.period}</span>}
                </div>
              </div>

              <div className="space-y-3 flex-1 pt-4 border-t border-white/10">
                <p className="text-xs font-semibold uppercase tracking-wider text-slate-300">Included Features:</p>
                <ul className="space-y-2.5 text-sm text-slate-300">
                  {plan.features.map((feat) => (
                    <li key={feat} className="flex items-start gap-2.5">
                      <Check className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                      <span>{feat}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="pt-6">
                <Link to={plan.link}>
                  <Button variant={plan.variant === "glow" ? "primary" : "secondary"} className="w-full justify-center py-3 text-sm">
                    {plan.cta}
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </Link>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Trust & Guarantee Banner */}
      <div className="max-w-4xl mx-auto">
        <Card variant="glass" className="p-8 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div className="space-y-2">
            <Shield className="w-8 h-8 text-indigo-400 mx-auto" />
            <h4 className="text-sm font-bold text-white">Safety Protected</h4>
            <p className="text-xs text-slate-400">All data encrypted at rest and audited by AI Safety monitors.</p>
          </div>
          <div className="space-y-2">
            <Zap className="w-8 h-8 text-cyan-400 mx-auto" />
            <h4 className="text-sm font-bold text-white">Instant Activation</h4>
            <p className="text-xs text-slate-400">No waitlists. Your Digital Twin graph begins seeding immediately.</p>
          </div>
          <div className="space-y-2">
            <Award className="w-8 h-8 text-emerald-400 mx-auto" />
            <h4 className="text-sm font-bold text-white">14-Day Refund Guarantee</h4>
            <p className="text-xs text-slate-400">Cancel anytime with 1-click in your account settings. Zero hassle.</p>
          </div>
        </Card>
      </div>
    </div>
  );
};
