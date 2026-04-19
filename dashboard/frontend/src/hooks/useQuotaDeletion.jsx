import { useCallback, useState } from "react"

import { deleteQuota } from "../api/management/quotas/Delete"

/**
 * Hook for managing quota deletion with error and success states.
 *
 * @param {object} params - Hook parameters.
 * @param {Array} params.quotas - Current array of quotas.
 * @param {Function} params.setQuotas - State setter for the quotas array.
 * @returns {object} Hook return value.
 * @returns {string} return.quotaError - Error message if deletion failed.
 * @returns {string} return.quotaSuccess - Success message if deletion succeeded.
 * @returns {number} return.quotaReloadKey - Key for triggering table refreshes.
 * @returns {Function} return.handleDeleteQuota - Function to delete a quota by row.
 */
export default function useQuotaDeletion({ quotas, setQuotas }) {
    const [quotaError, setQuotaError] = useState("")
    const [quotaSuccess, setQuotaSuccess] = useState("")
    const [quotaReloadKey, setQuotaReloadKey] = useState(0)

    const handleDeleteQuota = useCallback(async (row) => {
        setQuotaError("")
        setQuotaSuccess("")

        const selectedQuota = quotas.find((quota) => quota.id === row.id)
        if (!selectedQuota) {
            setQuotaError("Could not find the selected quota. Please refresh and try again.")
            return
        }

        try {
            const result = await deleteQuota(selectedQuota.id)
            setQuotas((prev) => prev.filter((quota) => quota.id !== selectedQuota.id))
            setQuotaReloadKey((prev) => prev + 1)
            setQuotaSuccess(result?.message || "Quota deleted successfully.")
        } catch (err) {
            setQuotaError(err.message || "Could not delete quota. Please try again.")
        }
    }, [quotas, setQuotas])

    return {
        quotaError,
        quotaSuccess,
        quotaReloadKey,
        handleDeleteQuota,
    }
}
