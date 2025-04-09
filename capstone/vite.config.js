//vite.config.js
import { defineConfig } from 'vite'
import { djangoVitePlugin } from 'django-vite-plugin'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [
        djangoVitePlugin({
            input: ['theram/index.css', 'theram/index.jsx', 'theram/login.css', 'theram/password.js', "theram/accounts.jsx"],
            pyPath: 'python3'
       }),
        react()
    ],
});