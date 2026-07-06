import { create } from "zustand";

export interface UserProfile {
  id: number | string;
  name: string;
  email: string;
  role: "student" | "admin" | "instructor";
  twin_id?: string;
}

export interface AuthState {
  user: UserProfile | null;
  isAuthenticated: boolean;
  setUser: (user: UserProfile | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: {
    id: "stu_101",
    name: "Sujith Kumar",
    email: "sujith@mentrax.ai",
    role: "student",
    twin_id: "twin_alpha_99",
  },
  isAuthenticated: true,
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  logout: () => set({ user: null, isAuthenticated: false }),
}));
