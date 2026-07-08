import React, { useState } from "react";
import { Code2, Play, CheckCircle2, Terminal, Sparkles, RefreshCw } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { AIResponseCard } from "@/components/widgets/AIResponseCard";

export const CodingArenaPage: React.FC = () => {
  const [code, setCode] = useState(
    `// Implement an AI Tool that queries Learning Memory\nexport async function searchVectorMemory(query: string, limit: number = 5) {\n  // Add similarity query logic here\n  return [{ id: 1, score: 0.98, text: "Sample embedding" }];\n}`
  );
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState<string | null>(null);
  const [aiFeedback, setAiFeedback] = useState<string | null>(null);

  const handleRunCode = () => {
    setIsRunning(true);
    setOutput(null);
    setAiFeedback(null);

    setTimeout(() => {
      setIsRunning(false);
      setOutput(`[SUCCESS]: Tool compiled cleanly.\n[EXECUTION]: Returned 1 mock embedding with similarity score 0.980.\n[SAFETY_VERIFY]: Memory boundaries checked and approved.`);
      setAiFeedback(`Great job! Your tool signature matches the safety contract. To optimize for high throughput, make sure to add a connection pool singleton for the database client.`);
    }, 1000);
  };

  return (
    <div className="space-y-6 py-4">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 dark:border-obsidian-600 pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <Badge variant="cyan">Coding Arena</Badge>
            <Badge variant="success">AI Safety Sandbox Active</Badge>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white mt-1">Interactive Coding Challenge #4: Vector Retrieval Tool</h1>
        </div>
        <div className="flex items-center space-x-3">
          <Button size="sm" variant="outline" onClick={() => setCode(`// Reset code\nexport async function searchVectorMemory(query: string) {}`)} leftIcon={<RefreshCw className="w-3.5 h-3.5" />}>
            Reset Editor
          </Button>
          <Button size="md" onClick={handleRunCode} isLoading={isRunning} leftIcon={<Play className="w-4 h-4 fill-current" />}>
            Run & Submit Solution
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Code Editor Area */}
        <Card variant="default" className="p-4 space-y-3 flex flex-col h-[500px]">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200 dark:border-obsidian-600 text-xs text-slate-400 font-mono">
            <span className="flex items-center gap-1.5"><Code2 className="w-4 h-4 text-indigo-400" /> solution.ts (TypeScript)</span>
            <span>UTF-8 • Strict Mode</span>
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full flex-1 bg-white dark:bg-obsidian-900 border border-slate-200 dark:border-obsidian-600 rounded-lg p-4 font-mono text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:ring-1 focus:ring-primary-500 resize-none leading-relaxed"
          />
        </Card>

        {/* Output & AI Feedback Area */}
        <div className="space-y-6 flex flex-col justify-between">
          <Card variant="default" className="p-4 space-y-3 flex-1 flex flex-col">
            <div className="flex items-center justify-between pb-2 border-b border-slate-200 dark:border-obsidian-600 text-xs font-semibold text-slate-900 dark:text-white">
              <span className="flex items-center gap-1.5"><Terminal className="w-4 h-4 text-emerald-400" /> Console Execution Output</span>
              {output && <Badge variant="success">Exit Code: 0</Badge>}
            </div>
            <div className="bg-white dark:bg-obsidian-900 border border-slate-200 dark:border-obsidian-600 rounded-lg p-4 font-mono text-xs text-slate-600 dark:text-slate-300 flex-1 overflow-y-auto whitespace-pre-wrap">
              {output ? output : "// Click 'Run & Submit Solution' to execute code in the AI safety sandbox."}
            </div>
          </Card>

          {aiFeedback && (
            <AIResponseCard
              title="AI Code Review Assistant"
              content={aiFeedback}
              confidenceScore={0.99}
              modelName="AI Code Audit v2.5"
            />
          )}
        </div>
      </div>
    </div>
  );
};
