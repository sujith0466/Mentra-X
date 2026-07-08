import { create } from "zustand";
import { persist } from "zustand/middleware";

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

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      logout: () => set({ user: null, isAuthenticated: false }),
    }),
    {
      name: "mentra-auth-storage",
    }
  )
);
