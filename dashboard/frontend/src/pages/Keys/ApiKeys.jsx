import CreateKeyForm from "./components/CreateKeyForm"
import ApiKeysTable from "../../components/blocks/ApiKeysTable"
import AlertBox from "../../components/primitives/AlertBox"
import { useEffect, useState } from "react"
import { fetchKeyInfos } from "../../api/management/keys/Info"
import { useAuth } from "../../api/auth/AuthProvider"
import useApiKeyDeletion from "../../hooks/useApiKeyDeletion"

/**
 * API keys management page for creating and managing user API keys.
 *
 * @returns {JSX.Element} The rendered API keys page.
 */
export default function ApiKeys() {
    const { user } = useAuth()
    const [apiKeys, setApiKeys] = useState([])
    const { apiKeyError, apiKeySuccess, apiKeyReloadKey, handleDeleteApiKey } = useApiKeyDeletion({ apiKeys, setApiKeys })

    const handleApiKeyCreated = (createdKey) => {
        if (!createdKey?.id) {
            return
        }

        setApiKeys((prev) => [createdKey, ...prev.filter((key) => key.id !== createdKey.id)])
    }

    useEffect(() => {
        let mounted = true

        if (!user?.id) {
            setApiKeys([])
            return
        }

        fetchKeyInfos(null, user.id)
            .then((data) => {
                if (!mounted) return
                setApiKeys(data || [])
            })
            .catch((err) => {
                console.error("Failed to load user API keys:", err)
            })

        return () => { mounted = false }
    }, [user, apiKeyReloadKey])

    return (
        <>
        <div className="flex flex-col gap-5">
            <h1 className="shrink-0 text-3xl font-bold text-white">API Keys</h1>
            <div className="border-b border-white/10">
                <CreateKeyForm onCreated={handleApiKeyCreated} />
            </div>
            <div className="border-b border-white/10">
                <div className="mb-3">
                    <AlertBox message={apiKeyError} variant="error" className="mt-0" />
                    <AlertBox message={apiKeySuccess} variant="success" className="mt-0" />
                </div>
                <ApiKeysTable title="Your API Keys" rows={apiKeys} onAction={handleDeleteApiKey} showUser={false} />
            </div>
        </div>
        </>
    )
}