import axios from 'axios';
import { isTokenExpired } from './auth/token'


const api = axios.create({
    baseURL: `${import.meta.env.FRONTEND_ADDRESS}:8080`,
    headers: {
        'Content-Type': 'application/json'
    }
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            if (isTokenExpired(token)) {
                localStorage.removeItem('token')
                window.dispatchEvent(new Event('auth:expired'))
                return Promise.reject(new Error('Session expired. Please sign in again.'))
            }

            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error)
    }
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error?.response?.status === 401) {
            localStorage.removeItem('token')
            window.dispatchEvent(new Event('auth:expired'))
        }

        return Promise.reject(error)
    }
)

export default api;