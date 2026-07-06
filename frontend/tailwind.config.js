/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        obsidian: {
          900: '#090a0f',
          800: '#12141d',
          700: '#1c1f2e',
          600: '#272a37',
          500: '#3f4458',
        },
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          glow: 'rgba(99, 102, 241, 0.4)',
        },
        ai: {
          violet: '#8b5cf6',
          emerald: '#10b981',
          rose: '#f43f5e',
          cyan: '#06b6d4',
          amber: '#f59e0b',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        'enterprise': '0 4px 20px -2px rgba(0, 0, 0, 0.5), 0 0 15px rgba(99, 102, 241, 0.15)',
        'glow': '0 0 25px rgba(99, 102, 241, 0.35)',
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'glass-surface': 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%)',
      }
    },
  },
  plugins: [],
}
