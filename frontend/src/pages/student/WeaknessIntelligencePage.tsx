import React, { useState, useEffect } from "react";
import { ShieldAlert, Zap, Award, AlertTriangle, CheckCircle, RefreshCw, Sparkles, BookOpen, BrainCircuit, Activity, ArrowRight } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { useAuthStore } from "@/store/useAuthStore";
import { weaknessApi, WeaknessItem, WeaknessProfileResponse } from "@/services/weaknessApi";
import { RemediationPlanModal } from "@/components/widgets/RemediationPlanModal";
import { PreTestVulnerabilityBanner } from "@/components/widgets/PreTestVulnerabilityBanner";

export const WeaknessIntelligencePage: React.FC = () => {
  const { user } = useAuthStore();
  const userId = Number(user?.id) || 338; // Default fallback for dev/demo

  const [loading, setLoading] = useState<boolean>(true);
  const [profileData, setProfileData] = useState<WeaknessProfileResponse["profile"] | null>(null);
  const [selectedWeakness, setSelectedWeakness] = useState<WeaknessItem | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [showPreTestBanner, setShowPreTestBanner] = useState<boolean>(true);

  useEffect(() => {
    fetchProfile();
  }, [userId]);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const res = await weaknessApi.getProfile(userId);
      setProfileData(res.profile);
    } catch (err) {
      console.error("Failed to fetch weakness profile:", err);
      // Fallback demo data if backend offline
      setProfileData({
        user_id: userId,
        overall_confidence: 78.4,
        timeline_state: "Recovery",
        last_updated: new Date().toISOString(),
        weaknesses: [
          { concept_id: "calculus_integration", concept_name: "Calculus Integration & Substitution", mastery_score: 0.32, severity: "Critical", mistake_count: 6, why_detected: "Repeated boundary condition errors in Quiz #4 and AI Tutor syntax confusion." },
          { concept_id: "matrix_determinants", concept_name: "Matrix Determinants & Eigenvalues", mastery_score: 0.54, severity: "At Risk", mistake_count: 3, why_detected: "Slow answering velocity and 2 failed practice drills." },
          { concept_id: "binary_search_trees", concept_name: "Binary Search Tree Rebalancing", mastery_score: 0.68, severity: "Needs Practice", mistake_count: 2, why_detected: "Minor logical fallback errors during Coding Arena challenge." },
        ],
        strengths: [
          { concept_id: "vector_similarity", concept_name: "Vector Similarity & Advanced Indexing", mastery_score: 0.96, severity: "Mastery", mistake_count: 0, why_detected: "100% accuracy across 3 consecutive lab assignments." },
          { concept_id: "tutor_routing", concept_name: "Intelligent Multi-AI team Routing", mastery_score: 0.92, severity: "Mastery", mistake_count: 1, why_detected: "High retention velocity verified by Learning Profile." },
        ],
      });
    } finally {
      setLoading(false);
    }
  };

  const handleOpenRemediation = (item: WeaknessItem) => {
    setSelectedWeakness(item);
    setIsModalOpen(true);
  };

  const handleVerificationSuccess = (newScore: number) => {
    if (profileData && selectedWeakness) {
      const updatedWeaknesses = profileData.weaknesses.map((w) =>
        w.concept_id === selectedWeakness.concept_id
          ? { ...w, mastery_score: newScore, severity: "Learning" as const }
          : w
      );
      setProfileData({ ...profileData, weaknesses: updatedWeaknesses });
    }
  };

  const getSeverityBadge = (sev: WeaknessItem["severity"]) => {
    switch (sev) {
      case "Critical": return <Badge variant="danger">Critical Gap</Badge>;
      case "At Risk": return <Badge variant="warning">At Risk</Badge>;
      case "Needs Practice": return <Badge variant="info">Needs Practice</Badge>;
      case "Learning": return <Badge variant="cyan">In Recovery</Badge>;
      case "Mastery": return <Badge variant="success">Mastery</Badge>;
      default: return <Badge variant="default">{sev}</Badge>;
    }
  };

  return (
    <div className="space-y-8 py-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 dark:border-obsidian-600 pb-6">
        <div>
          <div className="flex items-center space-x-2">
            <Badge variant="purple" size="sm">Enterprise Edition</Badge>
            <Badge variant="danger" size="sm">Adaptive Vulnerability Defense</Badge>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white mt-1">Weakness Intelligence & Remediation</h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time diagnostic heuristics, pre-test vulnerability mitigation, and closed-loop AI remediation workflows.
          </p>
        </div>
        <Button size="md" variant="outline" onClick={fetchProfile} leftIcon={<RefreshCw className="w-4 h-4" />}>
          Re-Scan Knowledge Graph
        </Button>
      </div>

      {/* Pre-Test Vulnerability Demo Banner */}
      {showPreTestBanner && (
        <PreTestVulnerabilityBanner
          quizTitle="Advanced JEE Calculus Midterm #2"
          vulnerabilities={[
            { concept_id: "calculus_integration", risk_level: "Critical (32% Mastery)", reason: "6 recent calculation boundary errors" },
            { concept_id: "matrix_determinants", risk_level: "At Risk (54% Mastery)", reason: "Velocity decay over last 14 days" }
          ]}
          onStartWarmup={(cId) => {
            const found = profileData?.weaknesses.find(w => w.concept_id === cId);
            if (found) handleOpenRemediation(found);
          }}
          onProceedAnyway={() => setShowPreTestBanner(false)}
        />
      )}

      {/* Overview Heuristics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card variant="gradient" className="p-5 border-indigo-500/20">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Overall Confidence</span>
            <Activity className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold text-slate-900 dark:text-white mt-2">
            {profileData && typeof profileData.overall_confidence === 'number' ? `${profileData.overall_confidence.toFixed(1)}%` : "—"}
          </div>
          <div className="text-xs text-emerald-400 mt-1 flex items-center">
            <Zap className="w-3 h-3 mr-1" /> Verified by Learning Profile
          </div>
        </Card>

        <Card variant="default" className="p-5 border-rose-500/20 bg-rose-950/10">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Diagnosed Weaknesses</span>
            <ShieldAlert className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-slate-900 dark:text-white mt-2">
            {profileData?.weaknesses?.length || "0"}
          </div>
          <div className="text-xs text-rose-300 mt-1">Requires active remediation drill</div>
        </Card>

        <Card variant="default" className="p-5 border-amber-500/20 bg-amber-950/10">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Timeline State</span>
            <BrainCircuit className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-300 mt-2">
            {profileData ? profileData.timeline_state : "Normal"}
          </div>
          <div className="text-xs text-slate-400 mt-1">Automated path injection active</div>
        </Card>

        <Card variant="default" className="p-5 border-emerald-500/20 bg-emerald-950/10">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Strength Intelligence</span>
            <Award className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-300 mt-2">
            {profileData?.strengths?.length || "0"}
          </div>
          <div className="text-xs text-slate-400 mt-1">High-mastery core pillars</div>
        </Card>
      </div>

      {/* Weakness Catalog Table */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center">
            <AlertTriangle className="w-5 h-5 text-amber-400 mr-2" />
            Active Concept Vulnerabilities
          </h2>
          <span className="text-xs text-slate-400 font-mono">Sorted by risk severity</span>
        </div>

        {loading ? (
          <div className="py-12 flex justify-center">
            <div className="w-8 h-8 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin" />
          </div>
        ) : profileData && Array.isArray(profileData.weaknesses) && profileData.weaknesses.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {profileData.weaknesses.map((item, idx) => (
              <Card key={idx} variant="default" className="p-5 border-slate-200 dark:border-white/10 hover:border-slate-300 dark:border-white/20 transition-all flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    {getSeverityBadge(item.severity)}
                    <span className="text-xs font-mono font-bold text-slate-400">
                      {item.mastery_score !== undefined ? (item.mastery_score * 100).toFixed(0) : 0}% Mastery
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white mt-1">{item.concept_name || item.concept_id}</h3>
                  <p className="text-xs text-slate-600 dark:text-slate-300 mt-2 bg-slate-50 dark:bg-obsidian-900/80 p-2.5 rounded-md border border-slate-200 dark:border-white/5">
                    <strong className="text-indigo-400">Why Detected:</strong> {item.why_detected || "Detected via adaptive quiz failure heuristics."}
                  </p>
                  <div className="mt-3 flex items-center justify-between text-xs text-slate-400">
                    <span>Mistakes Logged: <strong className="text-slate-900 dark:text-white">{item.mistake_count}</strong></span>
                    <span>Status: <span className="text-amber-400">Action Required</span></span>
                  </div>
                </div>

                <div className="mt-5 pt-3 border-t border-slate-200 dark:border-white/10">
                  <Button
                    variant="primary"
                    size="sm"
                    className="w-full justify-between"
                    onClick={() => handleOpenRemediation(item)}
                    rightIcon={<ArrowRight className="w-4 h-4" />}
                  >
                    Launch 4-Step Remediation Plan
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="p-8 text-center bg-slate-50 dark:bg-obsidian-900/40 border-emerald-500/30">
            <CheckCircle className="w-10 h-10 text-emerald-400 mx-auto mb-2" />
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">No Active Vulnerabilities Detected!</h3>
            <p className="text-sm text-slate-400 mt-1">Your Learning Profile reports healthy mastery across all evaluated syllabus vectors.</p>
          </Card>
        )}
      </div>

      {/* Strength Heuristics Section */}
      <div className="space-y-4 pt-4">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center">
          <Award className="w-5 h-5 text-emerald-400 mr-2" />
          Verified Strength Intelligence
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Array.isArray(profileData?.strengths) && profileData.strengths.map((item, idx) => (
            <Card key={idx} className="p-4 border-emerald-500/20 bg-emerald-950/5 flex items-center justify-between">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-slate-900 dark:text-white">{item.concept_name || item.concept_id}</span>
                  <Badge variant="success" size="sm">{item.mastery_score !== undefined ? (item.mastery_score * 100).toFixed(0) : 0}% Mastery</Badge>
                </div>
                <p className="text-xs text-slate-400 mt-1">{item.why_detected}</p>
              </div>
              <CheckCircle className="w-6 h-6 text-emerald-400 shrink-0" />
            </Card>
          ))}
        </div>
      </div>

      {/* Interactive Remediation Plan Modal */}
      {selectedWeakness && (
        <RemediationPlanModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          userId={userId}
          conceptId={selectedWeakness.concept_id}
          conceptName={selectedWeakness.concept_name}
          onVerificationSuccess={handleVerificationSuccess}
        />
      )}
    </div>
  );
};
