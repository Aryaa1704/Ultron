/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        jet: "#06080D",
        surface: "#101826",
        neon: "#1B9CFC",
        neonSoft: "#65B9FF"
      }
    }
  },
  plugins: []
};
