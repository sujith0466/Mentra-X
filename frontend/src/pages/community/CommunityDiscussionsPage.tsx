import React, { useState } from "react";
import { MessageSquare, Plus, Search, ThumbsUp, MessageCircle, Award, Sparkles, Filter, CheckCircle2 } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Badge } from "@/components/ui/Badge";
import { Link } from "react-router-dom";
import { Modal } from "@/components/ui/Modal";

interface DiscussionPost {
  id: string;
  title: string;
  author: string;
  authorLevel: string;
  category: string;
  snippet: string;
  upvotes: number;
  commentsCount: number;
  isAIAnswered: boolean;
  timeAgo: string;
  tags: string[];
}

export const CommunityDiscussionsPage: React.FC = () => {
  const [posts, setPosts] = useState<DiscussionPost[]>([
    {
      id: "post-1",
      title: "Optimal chunk size for embedding PDF textbooks into Qdrant?",
      author: "Elena Rostova",
      authorLevel: "Level 7 Scholar",
      category: "Vector Databases",
      snippet: "When chunking 500-page computer science textbooks, what is the best balance between semantic context preservation and embedding token limits using text-embedding-3-large?",
      upvotes: 42,
      commentsCount: 14,
      isAIAnswered: true,
      timeAgo: "3 hours ago",
      tags: ["Qdrant", "RAG", "Embeddings"],
    },
    {
      id: "post-2",
      title: "How to prevent recursive tool calling loops in Mastra swarms?",
      author: "Marcus Vance",
      authorLevel: "Level 9 Architect",
      category: "Mastra Swarms",
      snippet: "My DevTools AI agent occasionally enters an infinite retry loop when an external API returns a 429 rate limit. What is the recommended fallback pattern in Python?",
      upvotes: 29,
      commentsCount: 8,
      isAIAnswered: true,
      timeAgo: "5 hours ago",
      tags: ["Mastra", "Python", "Agents"],
    },
    {
      id: "post-3",
      title: "Understanding Enkrypt Layer 6 cosine similarity thresholds",
      author: "Sarah Jenkins",
      authorLevel: "Level 5 Student",
      category: "AI Security",
      snippet: "Why did my prompt get flagged by Layer 6 when asking for a mock SQL injection script for my cybersecurity assignment? Can we adjust confidence boundaries?",
      upvotes: 18,
      commentsCount: 5,
      isAIAnswered: false,
      timeAgo: "1 day ago",
      tags: ["Enkrypt", "Security", "ESDLC"],
    },
  ]);

  const [searchQuery, setSearchQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState<string>("All");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newCategory, setNewCategory] = useState("Vector Databases");
  const [newContent, setNewContent] = useState("");
  const [newTags, setNewTags] = useState("");

  const categories = ["All", "Vector Databases", "Mastra Swarms", "AI Security", "Algorithms", "Career Advice"];

  const handleCreatePost = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newContent.trim()) return;

    const created: DiscussionPost = {
      id: `post-${Date.now()}`,
      title: newTitle,
      author: "Alex Chen (You)",
      authorLevel: "Level 8 Scholar",
      category: newCategory,
      snippet: newContent,
      upvotes: 1,
      commentsCount: 0,
      isAIAnswered: false,
      timeAgo: "Just now",
      tags: newTags.split(",").map((t) => t.trim()).filter(Boolean),
    };

    setPosts([created, ...posts]);
    setIsModalOpen(false);
    setNewTitle("");
    setNewContent("");
    setNewTags("");
  };

  const handleUpvote = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    setPosts((prev) =>
      prev.map((p) => (p.id === id ? { ...p, upvotes: p.upvotes + 1 } : p))
    );
  };

  const filteredPosts = posts.filter((post) => {
    const matchesCat = activeCategory === "All" || post.category === activeCategory;
    const matchesSearch =
      post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.snippet.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.tags.some((t) => t.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCat && matchesSearch;
  });

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <MessageSquare className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Peer & AI Collaborative Network
          </Badge>
          <h1 className="text-3xl font-extrabold text-white">Community Forum & Discussions</h1>
          <p className="text-sm text-slate-400">Ask technical questions, share architectural patterns, and receive verified answers from AI swarm mentors.</p>
        </div>
        <Button variant="primary" onClick={() => setIsModalOpen(true)} className="px-5 py-2.5 self-start sm:self-center">
          <Plus className="w-4 h-4 mr-2" />
          Start New Discussion
        </Button>
      </div>

      {/* Search & Filters */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div className="relative flex-1 max-w-xl">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
          <Input
            placeholder="Search discussions, tags, or authors..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 w-full"
          />
        </div>

        {/* Category Tabs */}
        <div className="flex flex-wrap gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeCategory === cat
                  ? "bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md shadow-indigo-500/20"
                  : "bg-obsidian-800/60 text-slate-400 hover:text-white border border-white/5"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Posts List */}
      <div className="space-y-4">
        {filteredPosts.length === 0 ? (
          <Card variant="glass" className="p-12 text-center text-slate-400">
            No discussions found matching your filter criteria. Be the first to start a discussion!
          </Card>
        ) : (
          filteredPosts.map((post) => (
            <Link key={post.id} to={`/community/discussions/${post.id}`} className="block">
              <Card variant="default" className="p-6 transition-all hover:border-indigo-500/50 hover:shadow-lg">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div className="space-y-2 flex-1">
                    <div className="flex flex-wrap items-center gap-2 text-xs">
                      <span className="font-bold text-white">{post.author}</span>
                      <Badge variant="default" className="text-[10px]">{post.authorLevel}</Badge>
                      <span className="text-slate-500">&bull;</span>
                      <span className="text-indigo-400 font-semibold">{post.category}</span>
                      <span className="text-slate-500">&bull;</span>
                      <span className="text-slate-400">{post.timeAgo}</span>
                    </div>

                    <h3 className="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors">
                      {post.title}
                    </h3>
                    <p className="text-sm text-slate-300 line-clamp-2 leading-relaxed font-sans">
                      {post.snippet}
                    </p>

                    <div className="flex flex-wrap gap-1.5 pt-2">
                      {post.tags.map((tag) => (
                        <span key={tag} className="px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 text-xs border border-white/5">
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="flex sm:flex-col items-center justify-between sm:justify-center gap-4 sm:gap-2 w-full sm:w-auto pt-4 sm:pt-0 border-t sm:border-t-0 border-white/10 shrink-0">
                    <button
                      onClick={(e) => handleUpvote(post.id, e)}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-obsidian-900 hover:bg-indigo-600/20 hover:text-indigo-400 border border-white/10 text-slate-300 text-xs font-bold transition-all"
                    >
                      <ThumbsUp className="w-3.5 h-3.5" />
                      <span>{post.upvotes}</span>
                    </button>

                    <div className="flex items-center gap-1.5 text-xs text-slate-400 font-semibold">
                      <MessageCircle className="w-4 h-4 text-cyan-400" />
                      <span>{post.commentsCount} replies</span>
                    </div>

                    {post.isAIAnswered && (
                      <span className="inline-flex items-center gap-1 text-[10px] text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                        <CheckCircle2 className="w-3 h-3" />
                        AI Solved
                      </span>
                    )}
                  </div>
                </div>
              </Card>
            </Link>
          ))
        )}
      </div>

      {/* New Post Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Start a Community Discussion">
        <form onSubmit={handleCreatePost} className="space-y-4 text-slate-300">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Title / Question Summary</label>
            <Input
              placeholder="e.g., How to optimize attention memory in PyTorch?"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Category</label>
            <select
              value={newCategory}
              onChange={(e) => setNewCategory(e.target.value)}
              className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="Vector Databases">Vector Databases</option>
              <option value="Mastra Swarms">Mastra Swarms</option>
              <option value="AI Security">AI Security</option>
              <option value="Algorithms">Algorithms</option>
              <option value="Career Advice">Career Advice</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Detailed Explanation / Context</label>
            <textarea
              rows={5}
              placeholder="Provide background, code snippets, or error messages..."
              value={newContent}
              onChange={(e) => setNewContent(e.target.value)}
              required
              className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Tags (comma separated)</label>
            <Input
              placeholder="e.g., PyTorch, Transformers, Attention"
              value={newTags}
              onChange={(e) => setNewTags(e.target.value)}
            />
          </div>
          <div className="pt-4 flex justify-end gap-3">
            <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary">
              Post Discussion
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
