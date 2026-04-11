import { useCallback, useState } from "react"

import { deleteUser } from "../api/management/user/Delete"

export default function useUserDeletion({ users, setUsers }) {
    const [userError, setUserError] = useState("")
    const [userSuccess, setUserSuccess] = useState("")
    const [userReloadKey, setUserReloadKey] = useState(0)

    const handleDeleteUser = useCallback(async (row) => {
        setUserError("")
        setUserSuccess("")

        const selectedUser = users.find((user) => user.id === row.id)
        if (!selectedUser) {
            setUserError("Could not find the selected user. Please refresh and try again.")
            return
        }

        try {
            const result = await deleteUser(selectedUser.id)
            setUsers((prev) => prev.filter((user) => user.id !== selectedUser.id))
            setUserReloadKey((prev) => prev + 1)
            setUserSuccess(result?.message || "User deleted successfully.")
        } catch (err) {
            setUserError(err.message || "Could not delete user. Please try again.")
        }
    }, [users, setUsers])

    return {
        userError,
        userSuccess,
        userReloadKey,
        handleDeleteUser,
    }
}
