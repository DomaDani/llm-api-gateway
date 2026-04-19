import { useCallback, useState } from "react"

import { deleteProject } from "../api/management/project/Delete"

/**
 * Hook for managing project deletion with error and success states.
 *
 * @returns {object} Hook return value.
 * @returns {string} return.projectError - Error message if deletion failed.
 * @returns {string} return.projectSuccess - Success message if deletion succeeded.
 * @returns {number} return.projectReloadKey - Key for triggering table refreshes.
 * @returns {Function} return.handleDeleteProject - Function to delete a project by ID.
 */
export default function useProjectDeletion() {
    const [projectError, setProjectError] = useState("")
    const [projectSuccess, setProjectSuccess] = useState("")
    const [projectReloadKey, setProjectReloadKey] = useState(0)

    const handleDeleteProject = useCallback(async (projectId) => {
        setProjectError("")
        setProjectSuccess("")

        if (!projectId) {
            setProjectError("No project selected.")
            return false
        }

        try {
            const result = await deleteProject(projectId)
            setProjectReloadKey((prev) => prev + 1)
            setProjectSuccess(result?.message || "Project deleted successfully.")
            return true
        } catch (err) {
            setProjectError(err.message || "Could not delete project. Please try again.")
            return false
        }
    }, [])

    return {
        projectError,
        projectSuccess,
        projectReloadKey,
        handleDeleteProject,
    }
}
