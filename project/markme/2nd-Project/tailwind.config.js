/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Hajri Hub brand green — matches visitor site exactly
        primary: {
          50:  '#f3f9eb',
          100: '#e4f2d0',
          200: '#c9e6a1',
          300: '#aed872',
          400: '#97cc55',
          500: '#82bc4a',   // --primary-green
          600: '#6aa33a',   // slightly darker for hover
          700: '#5a8f2a',   // --primary-dark
          800: '#477020',
          900: '#345218',
        },
        dark: {
          800: '#1e1e2d',
          900: '#151521',
        },
      },
      fontFamily: {
        sans:    ['Inter', 'sans-serif'],
        display: ['Outfit', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
