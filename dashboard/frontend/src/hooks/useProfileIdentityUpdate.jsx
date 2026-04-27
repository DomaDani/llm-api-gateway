import { useCallback, useEffect, useState } from "react"

import { changeIdentity } from "../api/management/user/ChangeIdentity"

/**
 * Hook for managing profile identity updates with validation and error/success states.
 *
 * @param {object} params - Hook parameters.
 * @param {boolean} params.sessionExpired - Whether the current auth session is expired.
 * @returns {object} Hook return value.
 * @returns {string} return.profileIdentityError - Error message if update failed.
 * @returns {string} return.profileIdentitySuccess - Success message if update succeeded.
 * @returns {boolean} return.profileIdentityLoading - Whether an update request is in progress.
 * @returns {Function} return.handleUpdateProfileIdentity - Function to update profile identity from payload.
 */
export default function useProfileIdentityUpdate({ sessionExpired }) {
    const [profileIdentityError, setProfileIdentityError] = useState("")
    const [profileIdentitySuccess, setProfileIdentitySuccess] = useState("")
    const [profileIdentityLoading, setProfileIdentityLoading] = useState(false)

    useEffect(() => {
        if (sessionExpired) {
            setProfileIdentityError("Your session has expired. Please sign in again.")
        }
    }, [sessionExpired])

    const handleUpdateProfileIdentity = useCallback(async (payload) => {
        if (sessionExpired) {
            setProfileIdentityError("Your session has expired. Please sign in again.")
            return false
        }

        const email = payload?.email?.trim() ?? ""
        const username = payload?.username?.trim() ?? ""

        if (!email || !username) {
            setProfileIdentityError("Username and email are required.")
            setProfileIdentitySuccess("")
            return false
        }

        setProfileIdentityError("")
        setProfileIdentitySuccess("")
        setProfileIdentityLoading(true)

        try {
            const message = await changeIdentity({
                email,
                username,
            })
            setProfileIdentitySuccess(message || "Identity updated successfully.")
            return true
        } catch (err) {
            setProfileIdentityError(err.message || "Failed to update identity.")
            return false
        } finally {
            setProfileIdentityLoading(false)
        }
    }, [sessionExpired])

    return {
        profileIdentityError,
        profileIdentitySuccess,
        profileIdentityLoading,
        handleUpdateProfileIdentity,
    }
}