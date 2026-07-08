import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface DiscussionPost {
  id: string;
  title: string;
  author: string;
  authorLevel: string;
  category: string;
  snippet: string;
  content: string;
  upvotes: number;
  commentsCount: number;
  isAIAnswered: boolean;
  timeAgo: string;
  tags: string[];
  replies: Reply[];
}

export interface Reply {
  id: string;
  author: string;
  authorLevel: string;
  isAI: boolean;
  isVerified: boolean;
  timeAgo: string;
  upvotes: number;
  content: string;
}

export interface StudentRank {
  rank: number;
  name: string;
  campus: string;
  level: string;
  xp: number;
  streakDays: number;
  prCount: number;
  badge: string;
}

export interface CommunityState {
  posts: DiscussionPost[];
  leaderboard: StudentRank[];
  addPost: (post: Omit<DiscussionPost, "id" | "timeAgo" | "upvotes" | "commentsCount" | "isAIAnswered" | "replies">) => void;
  upvotePost: (id: string) => void;
  addReply: (postId: string, reply: Omit<Reply, "id" | "timeAgo" | "upvotes">) => void;
  updateLeaderboardWithUser: (name: string, campus?: string, xp?: number, streakDays?: number) => void;
}

export const useCommunityStore = create<CommunityState>()(
  persist(
    (set, get) => ({
      posts: [],
      leaderboard: [],
      addPost: (newPostData) => {
        const newPost: DiscussionPost = {
          ...newPostData,
          id: `post-${Date.now()}`,
          timeAgo: "Just now",
          upvotes: 1,
          commentsCount: 0,
          isAIAnswered: false,
          replies: [],
        };
        set((state) => ({
          posts: [newPost, ...state.posts],
        }));
      },
      upvotePost: (id) => {
        set((state) => ({
          posts: state.posts.map((post) =>
            post.id === id ? { ...post, upvotes: post.upvotes + 1 } : post
          ),
        }));
      },
      addReply: (postId, replyData) => {
        const newReply: Reply = {
          ...replyData,
          id: `rep-${Date.now()}`,
          timeAgo: "Just now",
          upvotes: 1,
        };
        set((state) => ({
          posts: state.posts.map((post) =>
            post.id === postId
              ? {
                  ...post,
                  commentsCount: post.commentsCount + 1,
                  replies: [...(post.replies || []), newReply],
                }
              : post
          ),
        }));
      },
      updateLeaderboardWithUser: (name, campus = "Enterprise University", xp = 120, streakDays = 1) => {
        const current = get().leaderboard;
        const existingIdx = current.findIndex((item) => item.name === name);
        let updated: StudentRank[];
        if (existingIdx >= 0) {
          updated = current.map((item, idx) =>
            idx === existingIdx
              ? { ...item, xp: Math.max(item.xp, xp), streakDays: Math.max(item.streakDays, streakDays) }
              : item
          );
        } else {
          updated = [
            ...current,
            {
              rank: current.length + 1,
              name,
              campus,
              level: "Level 1 Starter",
              xp,
              streakDays,
              prCount: 0,
              badge: "Pioneer",
            },
          ];
        }
        // Sort descending by XP and update ranks
        updated.sort((a, b) => b.xp - a.xp);
        updated = updated.map((item, index) => ({ ...item, rank: index + 1 }));
        set({ leaderboard: updated });
      },
    }),
    {
      name: "mentra-community-storage",
    }
  )
);
