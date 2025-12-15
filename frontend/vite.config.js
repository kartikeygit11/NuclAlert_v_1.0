import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/load_data': 'http://localhost:5000',
      '/get_data': 'http://localhost:5000',
      '/download_processed': 'http://localhost:5000',
      '/static': 'http://localhost:5000',
    },
  },
})
