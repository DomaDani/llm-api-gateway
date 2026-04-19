import { useCallback, useState } from "react"

import { createQuota } from "../api/management/quotas/Create"

/**
 * Hook for managing quota creation with validation and error/success states.
 *
 * @param {object} params - Hook parameters.
 * @param {number | null} params.projectId - Project identifier, or null for global quotas.
 * @returns {object} Hook return value.
 * @returns {string} return.quotaCreateError - Error message if creation failed.
 * @returns {string} return.quotaCreateSuccess - Success message if creation succeeded.
 * @returns {number} return.quotaCreateReloadKey - Key for triggering table refreshes.
 * @returns {Function} return.handleCreateQuota - Function to create a quota from payload.
 */
export default function useQuotaCreation({ projectId = null }) {
    const [quotaCreateError, setQuotaCreateError] = useState("")
    const [quotaCreateSuccess, setQuotaCreateSuccess] = useState("")
    const [quotaCreateReloadKey, setQuotaCreateReloadKey] = useState(0)

    const handleCreateQuota = useCallback(async (payload) => {
        setQuotaCreateError("")
        setQuotaCreateSuccess("")

        const limitId = payload?.limit_id
        const limitValue = payload?.value
        const period = payload?.period
        const userId = payload?.user_id ?? null
        const keyId = payload?.key_id ?? null
        const isPermanent = Boolean(payload?.isPermanent)
        const expiration = payload?.expiration

        if (!limitId) {
            setQuotaCreateError("Quota type is required.")
            return
        }

        if (limitValue == null || limitValue === "") {
            setQuotaCreateError("Quota value is required.")
            return
        }

        if (!period) {
            setQuotaCreateError("Refresh frequency is required.")
            return
        }

        if (!isPermanent && !expiration) {
            setQuotaCreateError("Expiration date is required unless quota is permanent.")
            return
        }

        if (userId != null && keyId != null) {
            setQuotaCreateError("Select either a user or a key target, not both.")
            return
        }

        try {
            await createQuota({
                project_id: projectId,
                user_id: userId,
                key_id: keyId,
                limit_id: limitId,
                limit_value: Number(limitValue),
                period,
                expires_at: isPermanent ? null : `${expiration}T00:00:00`,
            })
            setQuotaCreateReloadKey((prev) => prev + 1)
            setQuotaCreateSuccess("Quota created successfully.")
        } catch (err) {
            setQuotaCreateError(err.message || "Could not create quota. Please try again.")
        }
    }, [projectId])

    return {
        quotaCreateError,
        quotaCreateSuccess,
        quotaCreateReloadKey,
        handleCreateQuota,
    }
}
