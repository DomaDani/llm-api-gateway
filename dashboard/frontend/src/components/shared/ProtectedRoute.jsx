import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../api/auth/AuthProvider';
import { isTokenExpired } from '../../api/auth/token'

/**
 * Route wrapper that protects routes requiring authentication and checks token validity.
 * Redirects to login if token is expired or missing, and enforces password change if needed.
 *
 * @returns {JSX.Element} The protected outlet or a redirect.
 */
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