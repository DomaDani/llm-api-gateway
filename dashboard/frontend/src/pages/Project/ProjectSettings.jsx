import UsersTable from "../../components/blocks/UsersTable"
import QuotasTable from "../../components/blocks/QuotasTable"
import ApiKeysTable from "../../components/blocks/ApiKeysTable"
import CreateQuotaForm from "../../components/blocks/CreateQuotaForm"
import AddUserForm from "./components/AddUserForm"
import { useEffect, useState } from "react"
import { useProject } from "../../context/ProjectContext"
import { fetchQuotaInfos } from "../../api/management/quotas/Info"
import { fetchKeyInfos } from "../../api/management/keys/Info"
import AlertBox from "../../components/primitives/AlertBox"
import useQuotaDeletion from "../../hooks/useQuotaDeletion"
import useApiKeyDeletion from "../../hooks/useApiKeyDeletion"

const PLACEHOLDER_USERS = [
    {
        id: "u-1",
        username: "alice",
        email: "alice@example.com",
        role: "administrator",
        createdAt: "2026-03-20",
    },
    {
        id: "u-2",
        username: "bence",
        email: "bence@example.com",
        role: "project manager",
        createdAt: "2026-03-25",
    },
    {
        id: "u-3",
        username: "csilla",
        email: "csilla@example.com",
        role: "user",
        createdAt: "2026-04-01",
    },
]

export default function ProjectSetings() {
    const { selectedProject } = useProject()
    const [quotas, setQuotas] = useState([])
    const [apiKeys, setApiKeys] = useState([])
    const { quotaError, quotaSuccess, quotaReloadKey, handleDeleteQuota } = useQuotaDeletion({ quotas, setQuotas })
    const { apiKeyError, apiKeySuccess, apiKeyReloadKey, handleDeleteApiKey } = useApiKeyDeletion({ apiKeys, setApiKeys })

    useEffect(() => {
        let mounted = true

        if (!selectedProject) {
            setQuotas([])
            return
        }

        fetchQuotaInfos(selectedProject.id, null, null, false, false)
            .then((data) => {
                if (!mounted) return
                setQuotas(data || [])
            })
            .catch((err) => {
                console.error("Failed to load project quotas:", err)
            })

        return () => { mounted = false }
    }, [selectedProject, quotaReloadKey])

    useEffect(() => {
        let mounted = true

        if (!selectedProject) {
            setApiKeys([])
            return
        }

        fetchKeyInfos(selectedProject.id, null)
            .then((data) => {
                if (!mounted) return
                setApiKeys(data || [])
            })
            .catch((err) => {
                console.error("Failed to load project API keys:", err)
            })

        return () => { mounted = false }
    }, [selectedProject, apiKeyReloadKey])

    return (
        <>
            <div className="flex flex-col gap-5">
                <h1 className="shrink-0 text-3xl font-bold text-white">Project Settings</h1>
                <div className="border-b border-white/10">
                    <AddUserForm />
                </div>
                <div className="border-b border-white/10">
                    <CreateQuotaForm title="Create Project Quota" enableKeyTarget={true} />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <div className="mb-3">
                        <AlertBox message={quotaError} variant="error" className="mt-0" />
                        <AlertBox message={quotaSuccess} variant="success" className="mt-0" />
                    </div>
                    <QuotasTable title="Project Quotas" rows={quotas} showUser={true} showKey={true} onAction={handleDeleteQuota} />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <UsersTable title="Project Users" rows={PLACEHOLDER_USERS} onAction={() => { }} actionLabel="Remove" />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <div className="mb-3">
                        <AlertBox message={apiKeyError} variant="error" className="mt-0" />
                        <AlertBox message={apiKeySuccess} variant="success" className="mt-0" />
                    </div>
                    <ApiKeysTable title="Project API Keys" rows={apiKeys} onAction={handleDeleteApiKey} />
                </div>
            </div>
        </>
    )
}