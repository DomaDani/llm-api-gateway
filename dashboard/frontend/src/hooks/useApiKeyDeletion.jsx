import { useCallback, useState } from "react"

import { deleteApiKey } from "../api/management/keys/Delete"

export default function useApiKeyDeletion({ apiKeys, setApiKeys }) {
    const [apiKeyError, setApiKeyError] = useState("")
    const [apiKeySuccess, setApiKeySuccess] = useState("")
    const [apiKeyReloadKey, setApiKeyReloadKey] = useState(0)

    const handleDeleteApiKey = useCallback(async (row) => {
        setApiKeyError("")
        setApiKeySuccess("")

        const selectedApiKey = apiKeys.find((apiKey) => apiKey.id === row.id)
        if (!selectedApiKey) {
            setApiKeyError("Could not find the selected API key. Please refresh and try again.")
            return
        }

        try {
            const result = await deleteApiKey(selectedApiKey.id)
            setApiKeys((prev) => prev.filter((apiKey) => apiKey.id !== selectedApiKey.id))
            setApiKeyReloadKey((prev) => prev + 1)
            setApiKeySuccess(result?.message || "API key deleted successfully.")
        } catch (err) {
            setApiKeyError(err.message || "Could not delete API key. Please try again.")
        }
    }, [apiKeys, setApiKeys])

    return {
        apiKeyError,
        apiKeySuccess,
        apiKeyReloadKey,
        handleDeleteApiKey,
    }
}
