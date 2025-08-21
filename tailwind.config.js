/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Gradient colors from the image
        'coral': '#FF6B6B',
        'coral-light': '#FF8E8E',
        'pink': '#FF8FA3',
        'pink-light': '#FFB3C1',
        'orange': '#FFB347',
        'orange-light': '#FFCC70',
        'yellow': '#FFD93D',
        'yellow-light': '#FFE066',
        'peach': '#FFAB91',
        'peach-light': '#FFC4A3',
        'brown': '#af4c0f',
        'brown-light': '#c56b1f',
        
        // Text colors for contrast
        'text-primary': '#2D1B0E',
        'text-secondary': '#5D4E37',
        'text-muted': '#8B7355',
        'text-light': '#A68B6B',
        
        // Neutral overlay colors
        'glass-white': 'rgba(255, 255, 255, 0.1)',
        'glass-light': 'rgba(255, 255, 255, 0.2)',
        'glass-medium': 'rgba(255, 255, 255, 0.3)',
        
        // Border colors
        'border': 'rgba(255, 255, 255, 0.2)',
      },
      fontFamily: {
        'serif': ['Playfair Display', 'Georgia', 'serif'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      backdropBlur: {
        'xs': '2px',
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
        '4xl': '2rem',
      },
    },
  },
  plugins: [],
}
