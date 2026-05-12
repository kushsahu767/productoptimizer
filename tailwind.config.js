/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        base: "#090909",
        panel: "#111111",
        panelSoft: "#181818",
        accent: "#f5d90a",
        accentSoft: "#fff2a6",
        success: "#88ff4d",
        border: "rgba(255,255,255,0.12)"
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["Manrope", "sans-serif"]
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(245,217,10,0.25), 0 25px 60px rgba(245,217,10,0.08)"
      },
      backgroundImage: {
        radialGrid:
          "radial-gradient(circle at top, rgba(245,217,10,0.1), transparent 32%), linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)"
      },
      backgroundSize: {
        grid: "100% 100%, 28px 28px, 28px 28px"
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-6px)" }
        },
        rise: {
          "0%": { opacity: 0, transform: "translateY(16px)" },
          "100%": { opacity: 1, transform: "translateY(0)" }
        }
      },
      animation: {
        float: "float 5s ease-in-out infinite",
        rise: "rise 0.5s ease forwards"
      }
    }
  },
  plugins: []
};
