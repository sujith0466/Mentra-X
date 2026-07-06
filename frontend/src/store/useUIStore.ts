import { create } from "zustand";

export interface UIState {
  theme: "dark" | "light";
  isSidebarCollapsed: boolean;
  isChatOpen: boolean;
  toggleTheme: () => void;
  toggleSidebar: () => void;
  toggleChat: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  theme: "dark",
  isSidebarCollapsed: false,
  isChatOpen: false,
  toggleTheme: () =>
    set((state) => {
      const nextTheme = state.theme === "dark" ? "light" : "dark";
      if (nextTheme === "dark") {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
      return { theme: nextTheme };
    }),
  toggleSidebar: () => set((state) => ({ isSidebarCollapsed: !state.isSidebarCollapsed })),
  toggleChat: () => set((state) => ({ isChatOpen: !state.isChatOpen })),
}));
