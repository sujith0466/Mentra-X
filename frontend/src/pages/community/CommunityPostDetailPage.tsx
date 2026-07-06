import React, { useState } from "react";
import { ArrowLeft, ThumbsUp, MessageCircle, CheckCircle2, Send, Sparkles, Shield, User, CornerDownRight } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Link, useParams } from "react-router-dom";

export const CommunityPostDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  const [post, setPost] = useState({
    id: id || "post-1",
    title: "Optimal chunk size for embedding PDF textbooks into Qdrant?",
    author: "Elena Rostova",
    authorLevel: "Level 7 Scholar",
    category: "Vector Databases",
    timeAgo: "3 hours ago",
    upvotes: 42,
    content: `When building an enterprise document ingestion pipeline for our campus knowledge base, we are processing 500-page computer science textbooks. We are using OpenAI's text-embedding-3-large model (3072 dimensions, reduced to 1536 via MTEB normalization).\n\nWhat is the recommended balance between chunk token size and overlap? If chunks are too small (e.g., 256 tokens), we lose the broader architectural context of algorithmic proofs. If they are too large (e.g., 2048 tokens), Qdrant cosine similarity scores get diluted by irrelevant intro/outro text.\n\nHere is our current LangChain splitter setup:\n\`\`\`python\ntext_splitter = RecursiveCharacterTextSplitter(\n    chunk_size=1024,\n    chunk_overlap=128,\n    separators=["\\n\\n", "\\n", " ", ""]\n)\n\`\`\`\nShould we implement hierarchical parent-document retrieval instead?`,
    tags: ["Qdrant", "RAG", "Embeddings", "LangChain"],
  });

  const [replies, setReplies] = useState([
    {
      id: "rep-1",
      author: "Mastra Swarm Agent (Tutor AI)",
      authorLevel: "Autonomous AI Mentor",
      isAI: true,
      isVerified: true,
      timeAgo: "2 hours ago",
      upvotes: 28,
      content: `### Enkrypt Verified Swarm Synthesis\n\nFor dense academic textbooks with mathematical proofs, standard fixed-size chunking often dilutes vector similarity. We recommend a **Hierarchical Parent-Document Retrieval (PDR)** pattern combined with Qdrant payload filtering:\n\n1. **Child Chunks (256–512 tokens, 64 token overlap):** Embed these small chunks into Qdrant for high-precision vector similarity math.\n2. **Parent Document Store:** Store the larger section (e.g., 2048 tokens or entire chapter markdown) in your relational MySQL or document table.\n3. **Query Execution:** When Qdrant retrieves top-k child embeddings, use their payload \`parent_id\` to inject the full chapter context into the LLM prompt window.\n\nThis gives you sub-millisecond precision retrieval without sacrificing pedagogical context!`,
    },
    {
      id: "rep-2",
      author: "Marcus Vance",
      authorLevel: "Level 9 Architect",
      isAI: false,
      isVerified: false,
      timeAgo: "1 hour ago",
      upvotes: 11,
      content: `I second the AI Swarm's recommendation on Parent-Document retrieval! We implemented this exact pattern for our Systems Architecture syllabus. One additional tip: make sure to prepend section headers (e.g., "Chapter 4: AVL Trees - Section 4.2: Balancing") to every child chunk before embedding. It boosts Qdrant retrieval scores by almost 15%!`,
    },
  ]);

  const [newReply, setNewReply] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleAddReply = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newReply.trim()) return;
    setSubmitting(true);

    setTimeout(() => {
      const added = {
        id: `rep-${Date.now()}`,
        author: "Alex Chen (You)",
        authorLevel: "Level 8 Scholar",
        isAI: false,
        isVerified: false,
        timeAgo: "Just now",
        upvotes: 1,
        content: newReply,
      };
      setReplies([...replies, added]);
      setNewReply("");
      setSubmitting(false);
    }, 1000);
  };

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Back Button */}
      <div>
        <Link to="/community/discussions" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" />
          Back to Discussions Forum
        </Link>
      </div>

      {/* Main Question Card */}
      <Card variant="glow" className="p-8 space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-white/10">
          <div className="space-y-1">
            <div className="flex flex-wrap items-center gap-2 text-xs">
              <span className="font-bold text-white">{post.author}</span>
              <Badge variant="default" className="text-[10px]">{post.authorLevel}</Badge>
              <span className="text-slate-500">&bull;</span>
              <span className="text-indigo-400 font-semibold">{post.category}</span>
              <span className="text-slate-500">&bull;</span>
              <span className="text-slate-400">{post.timeAgo}</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white pt-1">{post.title}</h1>
          </div>
          
          <button
            onClick={() => setPost({ ...post, upvotes: post.upvotes + 1 })}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600/20 border border-indigo-500/40 text-indigo-300 font-bold text-sm hover:bg-indigo-600/30 transition-all shrink-0"
          >
            <ThumbsUp className="w-4 h-4" />
            <span>{post.upvotes} Upvotes</span>
          </button>
        </div>

        <div className="prose prose-invert max-w-none text-sm text-slate-300 whitespace-pre-line leading-relaxed font-sans">
          {post.content}
        </div>

        <div className="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-white/10">
          <div className="flex gap-2">
            {post.tags.map((tag) => (
              <span key={tag} className="px-2.5 py-1 rounded-md bg-obsidian-900 text-slate-300 text-xs font-mono border border-white/5">
                #{tag}
              </span>
            ))}
          </div>
          <span className="inline-flex items-center gap-1.5 text-xs text-emerald-400 font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            Active Discussion &bull; Enkrypt Audited
          </span>
        </div>
      </Card>

      {/* Answers Section */}
      <div className="space-y-6">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <MessageCircle className="w-5 h-5 text-cyan-400" />
          Replies & AI Syntheses ({replies.length})
        </h2>

        <div className="space-y-4">
          {replies.map((rep) => (
            <Card
              key={rep.id}
              variant={rep.isAI ? "gradient" : "default"}
              className={`p-6 space-y-4 ${rep.isAI ? "border-emerald-500/30 shadow-lg" : "border-white/10"}`}
            >
              <div className="flex items-center justify-between pb-3 border-b border-white/10">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${
                    rep.isAI ? "bg-emerald-500 text-obsidian-950" : "bg-indigo-600 text-white"
                  }`}>
                    {rep.isAI ? <Sparkles className="w-4 h-4" /> : <User className="w-4 h-4" />}
                  </div>
                  <div>
                    <span className="text-sm font-bold text-white mr-2">{rep.author}</span>
                    <Badge variant={rep.isAI ? "success" : "default"} className="text-[10px]">{rep.authorLevel}</Badge>
                  </div>
                </div>
                <div className="flex items-center gap-3 text-xs text-slate-400">
                  <span>{rep.timeAgo}</span>
                  <button className="flex items-center gap-1 px-2.5 py-1 rounded bg-obsidian-900 border border-white/10 hover:text-white font-bold">
                    <ThumbsUp className="w-3 h-3" />
                    <span>{rep.upvotes}</span>
                  </button>
                </div>
              </div>

              <div className="text-sm text-slate-300 whitespace-pre-line leading-relaxed font-sans">
                {rep.content}
              </div>

              {rep.isAI && (
                <div className="pt-2 flex items-center justify-between text-[10px] text-emerald-400 font-mono">
                  <span className="inline-flex items-center gap-1">
                    <Shield className="w-3.5 h-3.5" />
                    Generated by Mastra Swarm (Tutor AI) &bull; Verified by Enkrypt Layer 6
                  </span>
                  <span>Confidence Score: 0.99</span>
                </div>
              )}
            </Card>
          ))}
        </div>
      </div>

      {/* Add Reply Form */}
      <Card variant="default" className="p-6 sm:p-8 space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <CornerDownRight className="w-5 h-5 text-indigo-400" />
          Contribute Your Answer
        </h3>
        <form onSubmit={handleAddReply} className="space-y-4">
          <textarea
            rows={5}
            placeholder="Write your answer, share code patterns, or suggest documentation citations..."
            value={newReply}
            onChange={(e) => setNewReply(e.target.value)}
            required
            className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-sans"
          />
          <div className="flex justify-between items-center pt-2">
            <span className="text-xs text-slate-400 inline-flex items-center gap-1">
              <Shield className="w-3.5 h-3.5 text-indigo-400" />
              All replies are screened for code safety and academic integrity.
            </span>
            <Button type="submit" variant="primary" disabled={submitting} className="px-6 py-2.5">
              <Send className="w-4 h-4 mr-2" />
              {submitting ? "Publishing Reply..." : "Post Reply"}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
