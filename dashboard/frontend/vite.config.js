import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import dotenv from 'dotenv'
import path from 'path'

dotenv.config({ path: path.resolve(__dirname, '../../.env') })

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  define: {
    'import.meta.env.FRONTEND_ADDRESS': JSON.stringify(process.env.FRONTEND_ADDRESS),
    'import.meta.env.DASHBOARD_BACKEND_PORT': JSON.stringify(process.env.DASHBOARD_BACKEND_PORT),
  },
})
