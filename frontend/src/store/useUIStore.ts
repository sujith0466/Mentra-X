import { create } from "zustand";

export interface UIState {
  theme: "dark" | "light";
  isSidebarCollapsed: boolean;
  isChatOpen: boolean;
  toggleTheme: () => void;
  toggleSidebar: () => void;
  toggleChat: () => void;
  initTheme: () => void;
}

const getInitialTheme = (): "dark" | "light" => {
  if (typeof window !== "undefined" && localStorage.getItem("mentra-theme")) {
    return localStorage.getItem("mentra-theme") as "dark" | "light";
  }
  return "dark";
};

export const useUIStore = create<UIState>((set) => ({
  theme: getInitialTheme(),
  isSidebarCollapsed: false,
  isChatOpen: false,
  initTheme: () => {
    const current = getInitialTheme();
    if (current === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    set({ theme: current });
  },
  toggleTheme: () =>
    set((state) => {
      const nextTheme = state.theme === "dark" ? "light" : "dark";
      if (nextTheme === "dark") {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
      if (typeof window !== "undefined") {
        localStorage.setItem("mentra-theme", nextTheme);
      }
      return { theme: nextTheme };
    }),
  toggleSidebar: () => set((state) => ({ isSidebarCollapsed: !state.isSidebarCollapsed })),
  toggleChat: () => set((state) => ({ isChatOpen: !state.isChatOpen })),
}));

