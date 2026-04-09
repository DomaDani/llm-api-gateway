import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../api/auth/AuthProvider';
import { isTokenExpired } from '../../api/auth/token'

export default function ProtectedRoute() {
    const { token } = useAuth();

    if(!token || isTokenExpired(token)) {
        return <Navigate to="/" replace/>;
    } else {
        return <Outlet/>;
    }
};