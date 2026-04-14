import { createContext, useState, useContext, useEffect, useCallback } from "react";
import api from '../axios'
import { useNavigate } from "react-router-dom";
import { getTokenExpiryMs, isTokenExpired } from './token'
import { useProject } from "../../components/shared/ProjectContext";

const AuthContext = createContext();

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

    const logout = useCallback(() => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('token');
        clearSelectedProject();
        navigate('/');
    }, [navigate]);

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

    useEffect(() => {
        const onAuthExpired = () => {
            logout()
        }

        window.addEventListener('auth:expired', onAuthExpired)

        return () => {
            window.removeEventListener('auth:expired', onAuthExpired)
        }
    }, [logout])

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

export const useAuth = () => useContext(AuthContext);