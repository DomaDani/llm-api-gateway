import { Navigate } from "react-router-dom";
import { useAuth } from "../../api/auth/AuthProvider";
import { useProject } from "./ProjectContext";

export default function RequirePermissions({ children, requirements }) {
    const { user, loading } = useAuth()
    const { selectedProject } = useProject()

    if (loading) {
        return <div className="bg-gray-900 min-h-screen text-white flex items-center justify-center">Loading...</div>
    }

    const allowed = requirements ? requirements(user, selectedProject) : !!user
    return allowed ? children : <Navigate to="/home" replace />
}
