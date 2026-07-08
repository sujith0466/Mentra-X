import React, { useState, useEffect } from "react";
import { CheckCircle2, Circle, AlertCircle, Play, ShieldCheck, ArrowRight, Sparkles, HelpCircle } from "lucide-react";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { weaknessApi, RemediationPlan, CustomQuizQuestion } from "@/services/weaknessApi";

export interface RemediationPlanModalProps {
  isOpen: boolean;
  onClose: () => void;
  userId: number;
  conceptId: string;
  conceptName?: string;
  onVerificationSuccess?: (newScore: number) => void;
}

export const RemediationPlanModal: React.FC<RemediationPlanModalProps> = ({
  isOpen,
  onClose,
  userId,
  conceptId,
  conceptName,
  onVerificationSuccess,
}) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [plan, setPlan] = useState<RemediationPlan | null>(null);
  const [quiz, setQuiz] = useState<CustomQuizQuestion[]>([]);
  const [activeStep, setActiveStep] = useState<number>(1);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [verificationResult, setVerificationResult] = useState<{ verified: boolean; message?: string } | null>(null);

  useEffect(() => {
    if (isOpen && userId && conceptId) {
      loadPlanAndDrill();
    }
  }, [isOpen, userId, conceptId]);

  const loadPlanAndDrill = async () => {
    setLoading(true);
    setVerificationResult(null);
    setSelectedOption(null);
    try {
      const planRes = await weaknessApi.getRemediationPlan(userId, conceptId);
      setPlan(planRes.remediation_plan);

      const quizRes = await weaknessApi.generateQuiz(userId, conceptId);
      setQuiz(quizRes.custom_quiz.questions || []);
    } catch (err) {
      console.error("Error loading remediation plan:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifySubmission = async () => {
    if (selectedOption === null || quiz.length === 0) return;
    const currentQ = quiz[0];
    const isCorrect = selectedOption === currentQ.correct_option_index;

    try {
      const res = await weaknessApi.verifyRemediation({
        user_id: userId,
        concept_id: conceptId,
        passed: isCorrect,
        new_score: isCorrect ? 0.85 : 0.45,
      });

      setVerificationResult({
        verified: res.verified,
        message: isCorrect
          ? "🎉 Root-Cause Misconception Cured! Your Digital Twin mastery has been updated to 85%."
          : "⚠️ Incorrect option. Please review Step 2 (Worked Examples) and try the drill again.",
      });

      if (isCorrect && onVerificationSuccess) {
        onVerificationSuccess(res.updated_score || 0.85);
      }
    } catch (err) {
      console.error("Verification failed:", err);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`AI Remediation Intelligence — ${conceptName || conceptId}`}
      description="Tailored 4-step recovery workflow designed to eliminate root-cause misconceptions."
      maxWidth="2xl"
    >
      {loading ? (
        <div className="py-12 flex flex-col items-center justify-center space-y-4">
          <div className="w-8 h-8 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin" />
          <span className="text-sm font-mono text-slate-400">Synthesizing Misconception Recovery Path...</span>
        </div>
      ) : plan ? (
        <div className="space-y-6">
          {/* Avoidance Constraints Banner */}
          {plan.avoidance_constraints && (
            <Card className="p-3 bg-indigo-950/40 border-indigo-500/30 flex items-center justify-between text-xs">
              <div className="flex items-center space-x-2">
                <Sparkles className="w-4 h-4 text-indigo-400 shrink-0" />
                <span className="text-slate-600 dark:text-slate-300">
                  <strong className="text-slate-900 dark:text-white">Pedagogical Avoidance Active:</strong> Skipping Level(s) {" "}
                  {plan.avoidance_constraints.levels_to_avoid?.join(", ") || "None"} to prevent cognitive frustration.
                </span>
              </div>
              <Badge variant="purple" size="sm">Taxonomy Guard</Badge>
            </Card>
          )}

          {/* 4-Step Timeline */}
          <div className="grid grid-cols-4 gap-2 border-b border-slate-200 dark:border-white/10 pb-4">
            {plan.step_by_step_path?.map((step) => {
              const isActive = activeStep === step.step_number;
              const isDone = activeStep > step.step_number || (step.step_number === 4 && verificationResult?.verified);
              return (
                <div
                  key={step.step_number}
                  onClick={() => setActiveStep(step.step_number)}
                  className={`p-3 rounded-lg border cursor-pointer transition-all ${
                    isActive
                      ? "bg-indigo-500/20 border-indigo-500 text-slate-900 dark:text-white shadow-lg shadow-indigo-500/10"
                      : isDone
                      ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300"
                      : "bg-white dark:bg-obsidian-800/50 border-slate-200 dark:border-white/5 text-slate-400 hover:border-slate-300 dark:border-white/20"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-bold">STEP {step.step_number}</span>
                    {isDone ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <Circle className="w-3.5 h-3.5 opacity-40" />
                    )}
                  </div>
                  <div className="text-sm font-semibold mt-1 truncate">{step.title}</div>
                </div>
              );
            })}
          </div>

          {/* Step Detail View */}
          <div className="min-h-[220px] bg-slate-50 dark:bg-obsidian-900/60 p-5 rounded-xl border border-slate-200 dark:border-white/10">
            {activeStep === 1 && (
              <div className="space-y-4">
                <div className="flex items-center space-x-2">
                  <Badge variant="cyan">Step 1 — Foundation Audit</Badge>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Review Prerequisite Foundations</h3>
                <p className="text-sm text-slate-600 dark:text-slate-300">
                  {plan.step_by_step_path[0]?.description ||
                    "Before tackling complex integration problems, ensure your grasp of basic algebraic substitution and power rule boundary conditions is solid."}
                </p>
                <Button variant="primary" size="sm" onClick={() => setActiveStep(2)} rightIcon={<ArrowRight className="w-4 h-4" />}>
                  Proceed to Step 2: Guided Learning
                </Button>
              </div>
            )}

            {activeStep === 2 && (
              <div className="space-y-4">
                <div className="flex items-center space-x-2">
                  <Badge variant="purple">Step 2 — Targeted Study</Badge>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Concrete Worked Numerical Examples</h3>
                <p className="text-sm text-slate-600 dark:text-slate-300">
                  {plan.step_by_step_path[1]?.description ||
                    "Study step-by-step worked derivations. Avoid abstract analogies; focus on concrete variable transformations."}
                </p>
                <div className="p-4 rounded-lg bg-white dark:bg-obsidian-900 border border-indigo-500/20 font-mono text-xs text-indigo-300">
                  {`Example: ∫ 2x * cos(x^2) dx  =>  let u = x^2, du = 2x dx  =>  ∫ cos(u) du = sin(u) + C = sin(x^2) + C`}
                </div>
                <Button variant="primary" size="sm" onClick={() => setActiveStep(3)} rightIcon={<ArrowRight className="w-4 h-4" />}>
                  Proceed to Step 3: Misconception Drill
                </Button>
              </div>
            )}

            {activeStep === 3 && (
              <div className="space-y-4">
                <div className="flex items-center space-x-2">
                  <Badge variant="warning">Step 3 — Misconception Cure Drill</Badge>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Taxonomy Cure Practice</h3>
                <p className="text-sm text-slate-600 dark:text-slate-300">
                  {plan.step_by_step_path[2]?.description ||
                    "Complete 2 diagnostic drills specifically architected to target calculus substitution boundary mistakes."}
                </p>
                <Button variant="primary" size="sm" onClick={() => setActiveStep(4)} rightIcon={<ArrowRight className="w-4 h-4" />}>
                  Proceed to Step 4: Verify Mastery
                </Button>
              </div>
            )}

            {activeStep === 4 && (
              <div className="space-y-5">
                <div className="flex items-center justify-between">
                  <Badge variant="success">Step 4 — Closed-Loop Verification</Badge>
                  <span className="text-xs font-mono text-slate-400">Digital Twin Mutation Trigger</span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Mastery Verification Challenge</h3>
                
                {quiz && quiz.length > 0 ? (
                  <div className="space-y-4 bg-white dark:bg-obsidian-900/80 p-4 rounded-lg border border-slate-200 dark:border-white/5">
                    <p className="text-sm font-medium text-slate-900 dark:text-white">{quiz[0].question_text}</p>
                    <div className="space-y-2">
                      {quiz[0].options.map((opt, idx) => (
                        <div
                          key={idx}
                          onClick={() => !verificationResult?.verified && setSelectedOption(idx)}
                          className={`p-3 rounded-lg border text-sm cursor-pointer transition-all ${
                            selectedOption === idx
                              ? "bg-indigo-500/20 border-indigo-500 text-slate-900 dark:text-white"
                              : "bg-slate-50 dark:bg-obsidian-900 border-slate-200 dark:border-white/5 text-slate-600 dark:text-slate-300 hover:border-slate-300 dark:border-white/20"
                          }`}
                        >
                          <span className="font-mono font-bold mr-2">{String.fromCharCode(65 + idx)}.</span> {opt}
                        </div>
                      ))}
                    </div>

                    {verificationResult && (
                      <div className={`p-3 rounded-lg text-sm flex items-center space-x-2 ${
                        verificationResult.verified ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30" : "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                      }`}>
                        {verificationResult.verified ? <CheckCircle2 className="w-5 h-5 shrink-0" /> : <AlertCircle className="w-5 h-5 shrink-0" />}
                        <span>{verificationResult.message}</span>
                      </div>
                    )}

                    {!verificationResult?.verified && (
                      <Button
                        variant="primary"
                        size="md"
                        disabled={selectedOption === null}
                        onClick={handleVerifySubmission}
                        leftIcon={<ShieldCheck className="w-4 h-4" />}
                        className="w-full mt-2"
                      >
                        Submit & Verify Remediation
                      </Button>
                    )}
                  </div>
                ) : (
                  <p className="text-sm text-slate-400">No diagnostic drill questions found for this concept.</p>
                )}
              </div>
            )}
          </div>

          <div className="flex justify-end space-x-3 pt-2">
            <Button variant="outline" size="sm" onClick={onClose}>
              {verificationResult?.verified ? "Close & Resume Studies" : "Close"}
            </Button>
          </div>
        </div>
      ) : (
        <div className="py-8 text-center text-slate-400">Failed to load remediation plan.</div>
      )}
    </Modal>
  );
};
