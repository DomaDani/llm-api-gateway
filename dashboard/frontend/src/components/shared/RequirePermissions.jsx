import { Navigate } from "react-router-dom";
import { useAuth } from "../../api/auth/AuthProvider";
import { useProject } from "./ProjectContext";

/**
 * Route wrapper that enforces permission requirements based on user and project context.
 *
 * @param {object} props - Component props.
 * @param {JSX.Element} props.children - Content to render if requirements are met.
 * @param {Function} props.requirements - Function taking (user, selectedProject) and returning boolean.
 * @returns {JSX.Element} The children if allowed, or a redirect to home.
 */
export default function RequirePermissions({ children, requirements }) {
    const { user, loading } = useAuth()
    const { selectedProject } = useProject()

    if (loading) {
        return <div className="bg-gray-900 min-h-screen text-white flex items-center justify-center">Loading...</div>
    }

    const allowed = requirements ? requirements(user, selectedProject) : !!user
    return allowed ? children : <Navigate to="/home" replace />
}
