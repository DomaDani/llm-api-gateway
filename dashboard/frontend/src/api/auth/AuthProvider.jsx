import { createContext, useState, useContext, useEffect, useCallback } from "react";
import api from '../axios'
import { useNavigate } from "react-router-dom";
import { getTokenExpiryMs, isTokenExpired } from './token'
import { useProject } from "../../components/shared/ProjectContext";

const AuthContext = createContext();

/**
 * Provides authentication state and actions to the component tree.
 *
 * @param {object} props - Component props.
 * @param {React.ReactNode} props.children - Child elements rendered inside the provider.
 * @returns {JSX.Element} The auth context provider.
 */
export const AuthProvider = ({ children }) => {
    const { selectedProject, clearSelectedProject } = useProject()

    const [token, setToken] = useState(() => {
        const storedToken = localStorage.getItem('token')

        if (storedToken && !isTokenExpired(storedToken)) {
            return storedToken
        }

        localStorage.removeItem('token')
        return null
    });
    const [user, setUser] = useState(null);
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);

    /**
     * Clear the current auth state and redirect to the home page.
     *
     * @returns {void}
     */
    const logout = useCallback(() => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('token');
        clearSelectedProject();
        navigate('/');
    }, [navigate]);

    /**
     * Load the current authenticated user and store it in state.
     *
     * @returns {Promise<void>}
     */
    const fetchMe = useCallback(async () => {
        try {
            const params = selectedProject ? { project_id: selectedProject.id } : {}
            const response = await api.get('/users/me', { params });
            setUser(response.data);
        } catch (error) {
            logout();
        } finally {
            setLoading(false);
        }
    }, [logout, selectedProject]);

    /**
     * Check for an existing token and load the user if valid. If the token is expired, clear it from storage.
     */
    useEffect(() => {
        if(token) {
            if (isTokenExpired(token)) {
                logout();
                setLoading(false);
                return;
            }

            fetchMe();
        } else {
            setLoading(false);
        }
    }, [fetchMe, logout, token]);

    /**
     * Automatically log out the user when the token expires by calculating the remaining time until expiration and setting a timeout to trigger the logout action. Also listens for a custom 'auth:expired' event to handle token expiration across multiple tabs or windows.
     */
    useEffect(() => {
        if (!token) {
            return
        }

        const expirationMs = getTokenExpiryMs(token)

        if (!expirationMs) {
            return
        }

        const timeoutMs = Math.max(expirationMs - Date.now(), 0)
        const timeoutId = window.setTimeout(() => {
            logout()
        }, timeoutMs)

        return () => {
            window.clearTimeout(timeoutId)
        }
    }, [logout, token])

    /**
     * Listen for a custom 'auth:expired' event to handle token expiration across multiple tabs or windows. When the event is triggered, the user will be logged out in all open instances of the application.
     */
    useEffect(() => {
        const onAuthExpired = () => {
            logout()
        }

        window.addEventListener('auth:expired', onAuthExpired)

        return () => {
            window.removeEventListener('auth:expired', onAuthExpired)
        }
    }, [logout])

    /**
     * Authenticate a user and store the returned token.
     *
     * @param {string} email - User email address.
     * @param {string} password - User password.
     * @returns {Promise<void>}
     */
    const login = async (email, password) => {
        try {
            const response = await api.post('/auth/login', { email, password });
            
            const receivedToken = response.data.access_token;

            if (isTokenExpired(receivedToken)) {
                throw new Error('Received expired token. Please sign in again.')
            }
            
            setToken(receivedToken);
            localStorage.setItem('token', receivedToken);
            
            setLoading(true);

            navigate('/home');
        } catch (error) {
            console.error(error);
            throw error;
        }
    };

    return (
        <AuthContext.Provider value={{token, user, login, logout, loading}}>
            {!loading ? children : <div className="bg-gray-900 min-h-screen text-white flex items-center justify-center">Loading...</div>}
        </AuthContext.Provider>
    );
};

/**
 * Access the current authentication context.
 *
 * @returns {AuthContextValue} The auth context value.
 */
export const useAuth = () => {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider.");
    }

    return context;
};