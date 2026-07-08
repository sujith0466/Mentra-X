import React, { useState } from "react";
import { ArrowLeft, ThumbsUp, MessageCircle, CheckCircle2, Send, Sparkles, Shield, User, CornerDownRight } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Link, useParams } from "react-router-dom";
import { useAuthStore } from "@/store/useAuthStore";
import { useCommunityStore } from "@/store/useCommunityStore";

export const CommunityPostDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuthStore();
  const { posts, upvotePost, addReply } = useCommunityStore();

  const post = posts.find((p) => p.id === id);

  const [newReply, setNewReply] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (!post) {
    return (
      <div className="max-w-5xl mx-auto py-16 px-4 text-center space-y-4">
        <Card variant="glass" className="p-12 space-y-4">
          <MessageCircle className="w-12 h-12 text-slate-500 mx-auto" />
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">Discussion Post Not Found</h2>
          <p className="text-sm text-slate-400">The discussion post you are looking for does not exist or has been removed.</p>
          <Link to="/community/discussions">
            <Button variant="primary" size="md">Return to Discussions Forum</Button>
          </Link>
        </Card>
      </div>
    );
  }

  const handleAddReply = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newReply.trim()) return;
    setSubmitting(true);

    setTimeout(() => {
      addReply(post.id, {
        author: `${user?.name || "You"}`,
        authorLevel: "Level 1 Starter",
        isAI: false,
        isVerified: false,
        content: newReply,
      });
      setNewReply("");
      setSubmitting(false);
    }, 500);
  };

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Back Button */}
      <div>
        <Link to="/community/discussions" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" />
          Back to Discussions Forum
        </Link>
      </div>

      {/* Main Discussion Card */}
      <Card variant="glow" className="p-8 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 dark:border-white/10 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-indigo-300 font-bold">
              {post.author.slice(0, 2).toUpperCase()}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-slate-900 dark:text-white text-base">{post.author}</span>
                <Badge variant="default" className="text-xs">{post.authorLevel}</Badge>
              </div>
              <span className="text-xs text-slate-400">Posted {post.timeAgo} in <strong className="text-indigo-400">{post.category}</strong></span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="purple" className="px-3 py-1">
              <Sparkles className="w-3.5 h-3.5 mr-1.5 inline" />
              Learning Memory Indexed
            </Badge>
          </div>
        </div>

        <div className="space-y-4">
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white leading-tight">
            {post.title}
          </h1>
          <div className="prose prose-invert max-w-none text-slate-600 dark:text-slate-300 space-y-4 text-sm sm:text-base leading-relaxed font-sans whitespace-pre-wrap">
            {post.content || post.snippet}
          </div>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-4 pt-6 border-t border-slate-200 dark:border-white/10">
          <div className="flex items-center gap-2">
            {post.tags.map((tag) => (
              <span key={tag} className="px-2.5 py-1 rounded-lg bg-slate-50 dark:bg-obsidian-900 text-slate-400 text-xs font-mono border border-slate-200 dark:border-white/5">
                #{tag}
              </span>
            ))}
          </div>

          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              size="sm"
              leftIcon={<ThumbsUp className="w-4 h-4 text-indigo-400" />}
              onClick={() => upvotePost(post.id)}
              className="bg-slate-50 dark:bg-obsidian-900"
            >
              Upvote ({post.upvotes})
            </Button>
          </div>
        </div>
      </Card>

      {/* Replies Section */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <MessageCircle className="w-5 h-5 text-cyan-400" />
            Discussion Replies ({post.commentsCount || (post.replies && post.replies.length) || 0})
          </h3>
          <span className="text-xs text-slate-400">Verified by AI Safety Monitors</span>
        </div>

        <div className="space-y-4">
          {(!post.replies || post.replies.length === 0) ? (
            <Card variant="default" className="p-8 text-center text-slate-500">
              No replies yet. Be the first to share your thoughts or answer this question!
            </Card>
          ) : (
            post.replies.map((rep) => (
              <Card
                key={rep.id}
                variant={rep.isAI ? "gradient" : "default"}
                className={`p-6 space-y-4 transition-all ${
                  rep.isAI ? "border-emerald-500/30 bg-emerald-950/10" : ""
                }`}
              >
                <div className="flex items-center justify-between border-b border-slate-200 dark:border-white/5 pb-3">
                  <div className="flex items-center gap-2.5">
                    {rep.isAI ? (
                      <div className="w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
                        <Sparkles className="w-4 h-4 animate-pulse" />
                      </div>
                    ) : (
                      <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-200 dark:border-white/10 flex items-center justify-center text-slate-600 dark:text-slate-300 font-bold text-xs">
                        <User className="w-4 h-4" />
                      </div>
                    )}
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold text-slate-900 dark:text-white mr-2">{rep.author}</span>
                        <Badge variant={rep.isAI ? "success" : "default"} className="text-[10px]">{rep.authorLevel}</Badge>
                        {rep.isVerified && (
                          <span className="inline-flex items-center gap-1 text-[10px] text-emerald-400 font-semibold">
                            <CheckCircle2 className="w-3 h-3" /> Safety Verified
                          </span>
                        )}
                      </div>
                      <span className="text-[10px] text-slate-400">{rep.timeAgo}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 text-xs font-bold text-slate-400">
                    <ThumbsUp className="w-3.5 h-3.5 text-indigo-400" />
                    <span>{rep.upvotes}</span>
                  </div>
                </div>

                <div className="text-sm text-slate-700 dark:text-slate-200 leading-relaxed font-sans whitespace-pre-wrap pl-10">
                  {rep.content}
                </div>
              </Card>
            ))
          )}
        </div>

        {/* Add Reply Form */}
        <Card variant="default" className="p-6 space-y-4">
          <h4 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <CornerDownRight className="w-4 h-4 text-indigo-400" /> Join the Discussion
          </h4>
          <form onSubmit={handleAddReply} className="space-y-4">
            <textarea
              rows={4}
              placeholder="Write a supportive, constructive reply or solution..."
              value={newReply}
              onChange={(e) => setNewReply(e.target.value)}
              className="w-full bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 rounded-xl p-4 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all font-sans"
              required
            />
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-400 flex items-center gap-1.5">
                <Shield className="w-3.5 h-3.5 text-emerald-400" /> Automated ESDLC PII & Injection Redaction
              </span>
              <Button
                type="submit"
                variant="primary"
                size="md"
                isLoading={submitting}
                rightIcon={<Send className="w-4 h-4" />}
              >
                Post Reply
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};
