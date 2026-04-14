import UsersTable from "../../components/blocks/UsersTable"
import QuotasTable from "../../components/blocks/QuotasTable"
import ApiKeysTable from "../../components/blocks/ApiKeysTable"
import CreateQuotaForm from "../../components/blocks/CreateQuotaForm"
import AddUserForm from "./components/AddUserForm"
import DeleteProjectForm from "./components/DeleteProjectForm"
import { useEffect, useState } from "react"
import { useProject } from "../../components/shared/ProjectContext"
import { fetchQuotaInfos } from "../../api/management/quotas/Info"
import { fetchKeyInfos } from "../../api/management/keys/Info"
import { fetchUserInfos } from "../../api/management/user/Info"
import AlertBox from "../../components/primitives/AlertBox"
import useQuotaDeletion from "../../hooks/useQuotaDeletion"
import useApiKeyDeletion from "../../hooks/useApiKeyDeletion"
import useProjectUserRemoval from "../../hooks/useProjectUserRemoval"
import useProjectUserAddition from "../../hooks/useProjectUserAddition"
import useQuotaCreation from "../../hooks/useQuotaCreation"
import { useAuth } from "../../api/auth/AuthProvider"
import { useNavigate } from "react-router-dom"

function mapUserRow(user) {
    return {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
        createdAt: user.joined_date,
    }
}

export default function ProjectSetings() {
    const { selectedProject } = useProject()
    const { user } = useAuth()
    const navigate = useNavigate()

    useEffect(() => {
        if (user === null) return
        const allowed = user?.is_admin || user?.is_project_manager
        if (!allowed) {
            navigate('/home', { replace: true })
        }
    }, [user, navigate])
    const [quotas, setQuotas] = useState([])
    const [apiKeys, setApiKeys] = useState([])
    const [projectUsers, setProjectUsers] = useState([])
    const { quotaError, quotaSuccess, quotaReloadKey, handleDeleteQuota } = useQuotaDeletion({ quotas, setQuotas })
    const { quotaCreateError, quotaCreateSuccess, quotaCreateReloadKey, handleCreateQuota } = useQuotaCreation({
        projectId: selectedProject?.id ?? null,
    })
    const { apiKeyError, apiKeySuccess, apiKeyReloadKey, handleDeleteApiKey } = useApiKeyDeletion({ apiKeys, setApiKeys })
    const { projectUserError, projectUserSuccess, projectUserReloadKey, handleRemoveProjectUser } = useProjectUserRemoval({
        projectUsers,
        setProjectUsers,
        projectId: selectedProject?.id,
    })
    const {
        projectUserAddError,
        projectUserAddSuccess,
        projectUserAddReloadKey,
        handleAddProjectUser,
    } = useProjectUserAddition({
        projectId: selectedProject?.id,
    })

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
    }, [selectedProject, quotaReloadKey, quotaCreateReloadKey])

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

    useEffect(() => {
        let mounted = true

        if (!selectedProject) {
            setProjectUsers([])
            return
        }

        fetchUserInfos(selectedProject.id)
            .then((data) => {
                if (!mounted) return
                const mappedUsers = Array.isArray(data) ? data.map(mapUserRow) : []
                setProjectUsers(mappedUsers)
            })
            .catch((err) => {
                console.error("Failed to load project users:", err)
            })

        return () => { mounted = false }
    }, [selectedProject, projectUserReloadKey, projectUserAddReloadKey])

    return (
        <>
            <div className="flex flex-col gap-5">
                <h1 className="shrink-0 text-3xl font-bold text-white">Project Settings</h1>
                <div className="border-b border-white/10">
                    <div className="mb-3">
                        <AlertBox message={projectUserAddError} variant="error" className="mt-0" />
                        <AlertBox message={projectUserAddSuccess} variant="success" className="mt-0" />
                    </div>
                    <AddUserForm onSubmit={handleAddProjectUser} />
                </div>
                <div className="border-b border-white/10">
                    <div className="mb-3">
                        <AlertBox message={quotaCreateError} variant="error" className="mt-0" />
                        <AlertBox message={quotaCreateSuccess} variant="success" className="mt-0" />
                    </div>
                    <CreateQuotaForm title="Create Project Quota" enableKeyTarget={true} onSubmit={handleCreateQuota} />
                </div>
                <div className="border-b border-white/10">
                    <DeleteProjectForm />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <div className="mb-3">
                        <AlertBox message={quotaError} variant="error" className="mt-0" />
                        <AlertBox message={quotaSuccess} variant="success" className="mt-0" />
                    </div>
                    <QuotasTable title="Project Quotas" rows={quotas} showUser={true} showKey={true} onAction={handleDeleteQuota} />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <div className="mb-3">
                        <AlertBox message={projectUserError} variant="error" className="mt-0" />
                        <AlertBox message={projectUserSuccess} variant="success" className="mt-0" />
                    </div>
                    <UsersTable title="Project Users" rows={projectUsers} onAction={handleRemoveProjectUser} actionLabel="Remove" />
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