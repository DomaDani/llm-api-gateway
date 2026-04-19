import { useCallback, useState } from "react"

import { createProject } from "../api/management/project/Create"

/**
 * Hook for managing project creation with validation and loading state.
 *
 * @returns {object} Hook return value.
 * @returns {string} return.projectError - Error message if creation failed.
 * @returns {string} return.projectSuccess - Success message if creation succeeded.
 * @returns {boolean} return.projectLoading - Whether a creation request is in progress.
 * @returns {Function} return.handleCreateProject - Function to create a project from payload.
 */
export default function useProjectCreation() {
    const [projectError, setProjectError] = useState("")
    const [projectSuccess, setProjectSuccess] = useState("")
    const [projectLoading, setProjectLoading] = useState(false)

    const handleCreateProject = useCallback(async (payload) => {
        setProjectError("")
        setProjectSuccess("")

        const projectName = payload?.name?.trim() ?? ""
        const managerId = payload?.manager_id

        if (!projectName) {
            setProjectError("Project name is required.")
            return false
        }

        if (!managerId) {
            setProjectError("Project manager is required.")
            return false
        }

        setProjectLoading(true)

        try {
            const result = await createProject({
                name: projectName,
                manager_id: managerId,
            })
            setProjectSuccess(result?.message || "Project created successfully.")
            return true
        } catch (err) {
            setProjectError(err.message || "Could not create project. Please try again.")
            return false
        } finally {
            setProjectLoading(false)
        }
    }, [])

    return {
        projectError,
        projectSuccess,
        projectLoading,
        handleCreateProject,
    }
}