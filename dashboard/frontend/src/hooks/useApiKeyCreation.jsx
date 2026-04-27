import { useCallback, useState } from "react"

import { createApiKey } from "../api/management/keys/Create"

/**
 * Hook for managing API key creation with validation and error/success states.
 *
 * @param {object} params - Hook parameters.
 * @param {number | null} params.projectId - Project identifier for key creation.
 * @param {number | null} params.userId - Current user identifier.
 * @returns {object} Hook return value.
 * @returns {string} return.apiKeyCreateError - Error message if creation failed.
 * @returns {string} return.apiKeyCreateSuccess - Success message if creation succeeded.
 * @returns {boolean} return.apiKeyCreateLoading - Whether a creation request is in progress.
 * @returns {string} return.createdApiKeyValue - Newly created API key value.
 * @returns {number} return.apiKeyCreateReloadKey - Key for triggering table refreshes.
 * @returns {Function} return.handleCreateApiKey - Function to create an API key from payload.
 */
export default function useApiKeyCreation({ projectId = null, userId = null }) {
    const [apiKeyCreateError, setApiKeyCreateError] = useState("")
    const [apiKeyCreateSuccess, setApiKeyCreateSuccess] = useState("")
    const [apiKeyCreateLoading, setApiKeyCreateLoading] = useState(false)
    const [createdApiKeyValue, setCreatedApiKeyValue] = useState("")
    const [apiKeyCreateReloadKey, setApiKeyCreateReloadKey] = useState(0)

    const handleCreateApiKey = useCallback(async (payload) => {
        const name = payload?.name?.trim() ?? ""

        setApiKeyCreateError("")
        setApiKeyCreateSuccess("")

        if (!projectId) {
            setApiKeyCreateError("Select a project before creating an API key.")
            return null
        }

        if (!userId) {
            setApiKeyCreateError("You must be signed in to create API keys.")
            return null
        }

        if (!name) {
            setApiKeyCreateError("API key name is required.")
            return null
        }

        setApiKeyCreateLoading(true)

        try {
            const createdKey = await createApiKey({
                project_id: projectId,
                name,
            })
            setApiKeyCreateReloadKey((prev) => prev + 1)
            setCreatedApiKeyValue(createdKey?.api_key || "")
            setApiKeyCreateSuccess("API key created successfully.")
            return createdKey
        } catch (err) {
            setApiKeyCreateError(err.message || "Could not create API key. Please try again.")
            return null
        } finally {
            setApiKeyCreateLoading(false)
        }
    }, [projectId, userId])

    return {
        apiKeyCreateError,
        apiKeyCreateSuccess,
        apiKeyCreateLoading,
        createdApiKeyValue,
        apiKeyCreateReloadKey,
        handleCreateApiKey,
    }
}