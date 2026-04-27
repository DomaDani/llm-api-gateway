import { useCallback, useEffect, useState } from "react"

import { registerUser } from "../api/auth/Registration"

/**
 * Hook for managing user creation with validation and error/success states.
 *
 * @param {object} params - Hook parameters.
 * @param {boolean} params.sessionExpired - Whether the current auth session is expired.
 * @returns {object} Hook return value.
 * @returns {string} return.userCreateError - Error message if creation failed.
 * @returns {string} return.userCreateSuccess - Success message if creation succeeded.
 * @returns {boolean} return.userCreateLoading - Whether a creation request is in progress.
 * @returns {number} return.userCreateReloadKey - Key for triggering table refreshes.
 * @returns {Function} return.handleCreateUser - Function to create a user from payload.
 */
export default function useUserCreation({ sessionExpired }) {
    const [userCreateError, setUserCreateError] = useState("")
    const [userCreateSuccess, setUserCreateSuccess] = useState("")
    const [userCreateLoading, setUserCreateLoading] = useState(false)
    const [userCreateReloadKey, setUserCreateReloadKey] = useState(0)

    useEffect(() => {
        if (sessionExpired) {
            setUserCreateError("Your session has expired. Please sign in again.")
        }
    }, [sessionExpired])

    const handleCreateUser = useCallback(async (payload) => {
        if (sessionExpired) {
            setUserCreateError("Your session has expired. Please sign in again.")
            return false
        }

        const username = payload?.username?.trim() ?? ""
        const email = payload?.email?.trim() ?? ""
        const password = payload?.password ?? ""
        const mandateReset = Boolean(payload?.mandateReset)

        if (!username || !email || !password) {
            setUserCreateError("All fields are required.")
            setUserCreateSuccess("")
            return false
        }

        setUserCreateError("")
        setUserCreateSuccess("")
        setUserCreateLoading(true)

        try {
            const message = await registerUser({
                username,
                email,
                password,
                mandateReset,
            })
            setUserCreateReloadKey((prev) => prev + 1)
            setUserCreateSuccess(message || "User created successfully.")
            return true
        } catch (err) {
            setUserCreateError(err.message || "Could not create user. Please try again.")
            return false
        } finally {
            setUserCreateLoading(false)
        }
    }, [sessionExpired])

    return {
        userCreateError,
        userCreateSuccess,
        userCreateLoading,
        userCreateReloadKey,
        handleCreateUser,
    }
}