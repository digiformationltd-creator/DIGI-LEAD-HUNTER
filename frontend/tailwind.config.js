/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        digi: {
          dark: '#080C14',
          card: '#0F1626',
          border: '#1E293B',
          accent: '#3B82F6',
          teal: '#06B6D4',
          emerald: '#10B981',
          gold: '#F59E0B'
        }
      }
    },
  },
  plugins: [],
}
