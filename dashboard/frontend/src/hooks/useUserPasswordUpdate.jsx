import { useCallback, useEffect, useState } from "react"

import { changePassword } from "../api/management/user/ChangePassword"

/**
 * Hook for managing admin-driven user password updates with validation and error/success states.
 *
 * @param {object} params - Hook parameters.
 * @param {boolean} params.sessionExpired - Whether the current auth session is expired.
 * @returns {object} Hook return value.
 * @returns {string} return.userPasswordError - Error message if update failed.
 * @returns {string} return.userPasswordSuccess - Success message if update succeeded.
 * @returns {boolean} return.userPasswordLoading - Whether an update request is in progress.
 * @returns {Function} return.handleUpdateUserPassword - Function to update a user's password from payload.
 */
export default function useUserPasswordUpdate({ sessionExpired }) {
    const [userPasswordError, setUserPasswordError] = useState("")
    const [userPasswordSuccess, setUserPasswordSuccess] = useState("")
    const [userPasswordLoading, setUserPasswordLoading] = useState(false)

    useEffect(() => {
        if (sessionExpired) {
            setUserPasswordError("Your session has expired. Please sign in again.")
        }
    }, [sessionExpired])

    const handleUpdateUserPassword = useCallback(async (payload) => {
        if (sessionExpired) {
            setUserPasswordError("Your session has expired. Please sign in again.")
            return false
        }

        const userId = payload?.userId ? Number(payload.userId) : null
        const newPassword = payload?.newPassword ?? ""
        const mandateReset = Boolean(payload?.mandateReset)

        if (!userId || !newPassword) {
            setUserPasswordError("User and new password are required.")
            setUserPasswordSuccess("")
            return false
        }

        setUserPasswordError("")
        setUserPasswordSuccess("")
        setUserPasswordLoading(true)

        try {
            const message = await changePassword({
                userId,
                newPassword,
                newPasswordConfirm: newPassword,
                mandateReset,
            })
            setUserPasswordSuccess(message || "Password updated successfully.")
            return true
        } catch (err) {
            setUserPasswordError(err.message || "Could not update password. Please try again.")
            return false
        } finally {
            setUserPasswordLoading(false)
        }
    }, [sessionExpired])

    return {
        userPasswordError,
        userPasswordSuccess,
        userPasswordLoading,
        handleUpdateUserPassword,
    }
}