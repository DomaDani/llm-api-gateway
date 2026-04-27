import { useCallback, useEffect, useState } from "react"

import { changePassword } from "../api/management/user/ChangePassword"

/**
 * Hook for managing profile password updates with validation and error/success states.
 *
 * @param {object} params - Hook parameters.
 * @param {boolean} params.sessionExpired - Whether the current auth session is expired.
 * @returns {object} Hook return value.
 * @returns {string} return.profilePasswordError - Error message if update failed.
 * @returns {string} return.profilePasswordSuccess - Success message if update succeeded.
 * @returns {boolean} return.profilePasswordLoading - Whether an update request is in progress.
 * @returns {Function} return.handleUpdateProfilePassword - Function to update profile password from payload.
 */
export default function useProfilePasswordUpdate({ sessionExpired }) {
    const [profilePasswordError, setProfilePasswordError] = useState("")
    const [profilePasswordSuccess, setProfilePasswordSuccess] = useState("")
    const [profilePasswordLoading, setProfilePasswordLoading] = useState(false)

    useEffect(() => {
        if (sessionExpired) {
            setProfilePasswordError("Your session has expired. Please sign in again.")
        }
    }, [sessionExpired])

    const handleUpdateProfilePassword = useCallback(async (payload) => {
        if (sessionExpired) {
            setProfilePasswordError("Your session has expired. Please sign in again.")
            return false
        }

        const currentPassword = payload?.currentPassword ?? ""
        const newPassword = payload?.newPassword ?? ""
        const newPasswordConfirm = payload?.newPasswordConfirm ?? ""

        if (!currentPassword || !newPassword || !newPasswordConfirm) {
            setProfilePasswordError("All password fields are required.")
            setProfilePasswordSuccess("")
            return false
        }

        setProfilePasswordError("")
        setProfilePasswordSuccess("")
        setProfilePasswordLoading(true)

        try {
            const message = await changePassword({
                currentPassword,
                newPassword,
                newPasswordConfirm,
            })
            setProfilePasswordSuccess(message || "Password updated successfully.")
            return true
        } catch (err) {
            setProfilePasswordError(err.message || "Failed to update password.")
            return false
        } finally {
            setProfilePasswordLoading(false)
        }
    }, [sessionExpired])

    return {
        profilePasswordError,
        profilePasswordSuccess,
        profilePasswordLoading,
        handleUpdateProfilePassword,
    }
}