import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Allows Vite to listen on all network interfaces
    port: 5173,     // The port Vite will listen on (you can change this if needed)
  }
})
