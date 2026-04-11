import { useCallback, useState } from "react"

import { addUserToProject } from "../api/management/project/AddUser"

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
