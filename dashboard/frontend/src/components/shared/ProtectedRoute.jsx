import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../api/auth/AuthProvider';

export default function ProtectedRoute() {
    const { token } = useAuth();

    if(!token) {
        return <Navigate to="/" replace/>;
    } else {
        return <Outlet/>;
    }
};