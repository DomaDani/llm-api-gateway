import { useCallback, useState } from "react"

import { addUserToProject } from "../api/management/project/AddUser"

/**
 * Hook for managing addition of users to a project with error and success states.
 *
 * @param {object} params - Hook parameters.
 * @param {number} params.projectId - Project identifier.
 * @returns {object} Hook return value.
 * @returns {string} return.projectUserAddError - Error message if addition failed.
 * @returns {string} return.projectUserAddSuccess - Success message if addition succeeded.
 * @returns {number} return.projectUserAddReloadKey - Key for triggering table refreshes.
 * @returns {Function} return.handleAddProjectUser - Function to add a user to the project.
 */
export default function useProjectUserAddition({ projectId }) {
    const [projectUserAddError, setProjectUserAddError] = useState("")
    const [projectUserAddSuccess, setProjectUserAddSuccess] = useState("")
    const [projectUserAddReloadKey, setProjectUserAddReloadKey] = useState(0)

    const handleAddProjectUser = useCallback(async ({ user_id }) => {
        setProjectUserAddError("")
        setProjectUserAddSuccess("")

        if (!projectId) {
            setProjectUserAddError("No project selected.")
            return
        }

        if (!user_id) {
            setProjectUserAddError("Please select a user to add.")
            return
        }

        try {
            const result = await addUserToProject({
                project_id: projectId,
                user_id,
            })
            setProjectUserAddReloadKey((prev) => prev + 1)
            setProjectUserAddSuccess(result?.message || "User added to project successfully.")
        } catch (err) {
            setProjectUserAddError(err.message || "Could not add user to project. Please try again.")
        }
    }, [projectId])

    return {
        projectUserAddError,
        projectUserAddSuccess,
        projectUserAddReloadKey,
        handleAddProjectUser,
    }
}
