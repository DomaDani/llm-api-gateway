import { createContext, useState, useContext, useEffect } from "react";
import api from './axios'
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem("token") || null);
    const [user, setUser] = useState(null);
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);

    const fetchMe = async () => {
        try {
            const response = await api.get('/users/me');
            setUser(response.data);
        } catch (error) {
            logout();
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if(token) {
            fetchMe();
        } else {
            setLoading(false);
        }
    }, [token]);

    const login = async (email, password) => {
        try {
            const response = await api.post('/login', { email, password });
            
            const receivedToken = response.data.access_token;
            
            setToken(receivedToken);
            localStorage.setItem('token', receivedToken);
            
            setLoading(true);

            navigate('/home');
        } catch (error) {
            console.error(error);
            throw error;
        }
    };

    const logout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('token');
        navigate('/');
    };

    return (
        <AuthContext.Provider value={{token, user, login, logout, loading}}>
            {!loading ? children : <div className="bg-gray-900 min-h-screen text-white flex items-center justify-center">Loading...</div>}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);