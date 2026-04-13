import { useCallback, useState } from "react"

import { removeUserFromProject } from "../api/management/project/RemoveUser"

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
