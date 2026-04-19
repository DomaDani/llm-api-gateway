import { useCallback, useState } from "react"

import { removeUserFromProject } from "../api/management/project/RemoveUser"

/**
 * Hook for managing removal of users from a project with error and success states.
 *
 * @param {object} params - Hook parameters.
 * @param {Array} params.projectUsers - Current array of project users.
 * @param {Function} params.setProjectUsers - State setter for the project users array.
 * @param {number} params.projectId - Project identifier.
 * @returns {object} Hook return value.
 * @returns {string} return.projectUserError - Error message if removal failed.
 * @returns {string} return.projectUserSuccess - Success message if removal succeeded.
 * @returns {number} return.projectUserReloadKey - Key for triggering table refreshes.
 * @returns {Function} return.handleRemoveProjectUser - Function to remove a user from the project.
 */
export default function useProjectUserRemoval({ projectUsers, setProjectUsers, projectId }) {
    const [projectUserError, setProjectUserError] = useState("")
    const [projectUserSuccess, setProjectUserSuccess] = useState("")
    const [projectUserReloadKey, setProjectUserReloadKey] = useState(0)

    const handleRemoveProjectUser = useCallback(async (row) => {
        setProjectUserError("")
        setProjectUserSuccess("")

        if (!projectId) {
            setProjectUserError("No project selected.")
            return
        }

        const selectedUser = projectUsers.find((user) => user.id === row.id)
        if (!selectedUser) {
            setProjectUserError("Could not find the selected user in this project. Please refresh and try again.")
            return
        }

        try {
            const result = await removeUserFromProject({
                project_id: projectId,
                user_id: selectedUser.id,
            })
            setProjectUsers((prev) => prev.filter((user) => user.id !== selectedUser.id))
            setProjectUserReloadKey((prev) => prev + 1)
            setProjectUserSuccess(result?.message || "User removed from project successfully.")
        } catch (err) {
            setProjectUserError(err.message || "Could not remove user from project. Please try again.")
        }
    }, [projectUsers, setProjectUsers, projectId])

    return {
        projectUserError,
        projectUserSuccess,
        projectUserReloadKey,
        handleRemoveProjectUser,
    }
}
