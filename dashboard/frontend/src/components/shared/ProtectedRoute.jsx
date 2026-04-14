import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../api/auth/AuthProvider';
import { isTokenExpired } from '../../api/auth/token'

export default function ProtectedRoute() {
    const { token, user, loading } = useAuth();
    const location = useLocation();

    if (!token || isTokenExpired(token)) {
        return <Navigate to="/" replace />;
    }

    if (loading) {
        return <div className="bg-gray-900 min-h-screen text-white flex items-center justify-center">Loading...</div>
    }
    
    if (user?.is_password_expired) {
        if (location.pathname !== '/profile') {
            return <Navigate to="/profile" replace />
        }
    }

    return <Outlet />
}