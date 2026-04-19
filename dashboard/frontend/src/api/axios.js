import axios from 'axios';
import { isTokenExpired } from './auth/token'


/**
 * Shared Axios client configured for the dashboard frontend API.
 */
const api = axios.create({
    baseURL: `${import.meta.env.FRONTEND_ADDRESS}:8080`,
    headers: {
        'Content-Type': 'application/json'
    }
});

/**
 * Axios interceptor for handling requests.
 */
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

/**
 * Axios interceptor for handling responses, specifically to catch 401 Unauthorized errors that indicate an expired or invalid token.
 * Upon catching a 401 error with an Authorization header, it removes the token and dispatches a custom 'auth:expired' event to notify the application of the authentication expiration, prompting a logout across all tabs or windows.
 */
api.interceptors.response.use(
    (response) => response,
    (error) => {
        const isUnauthorized = error?.response?.status === 401
        const authHeader = error?.config?.headers?.Authorization ?? error?.config?.headers?.authorization

        if (isUnauthorized && authHeader) {
            localStorage.removeItem('token')
            window.dispatchEvent(new Event('auth:expired'))
        }

        return Promise.reject(error)
    }
)

export default api;