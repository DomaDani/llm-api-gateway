import CreateQuotaForm from "../../components/blocks/CreateQuotaForm"
import UsersTable from "../../components/blocks/UsersTable"
import CreateUserForm from "./components/CreateUserForm"
import CreateProjectForm from "./components/CreateProjectForm"
import QuotasTable from "../../components/blocks/QuotasTable"
import { useEffect, useState} from "react"
import { fetchQuotaInfos } from "../../api/management/quotas/Info"
import { fetchUserInfos } from "../../api/management/user/Info"
import AlertBox from "../../components/primitives/AlertBox"
import useQuotaDeletion from "../../hooks/useQuotaDeletion"
import useUserDeletion from "../../hooks/useUserDeletion"

function mapUserRow(user) {
    return {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
        createdAt: user.joined_date,
    }
}

export default function GlobalSettings() {
    const [quotas, setQuotas] = useState([])
    const [users, setUsers] = useState([])
    const { quotaError, quotaSuccess, quotaReloadKey, handleDeleteQuota } = useQuotaDeletion({ quotas, setQuotas })
    const { userError, userSuccess, userReloadKey, handleDeleteUser } = useUserDeletion({ users, setUsers })

    useEffect(() => {
        let mounted = true

        fetchQuotaInfos()
        .then((data) => {
            if (!mounted) return
            setQuotas(data)
        })
        .catch((err) => {
            console.error("Failed to load quota infos:", err)
        })

        return () => { mounted = false }
    }, [quotaReloadKey])

    useEffect(() => {
        let mounted = true

        fetchUserInfos()
            .then((data) => {
                if (!mounted) return
                const mappedUsers = Array.isArray(data) ? data.map(mapUserRow) : []
                setUsers(mappedUsers)
            })
            .catch((err) => {
                console.error("Failed to load users:", err)
            })

        return () => { mounted = false }
    }, [userReloadKey])

    return (
        <>
            <div className="flex flex-col gap-5">
                <h1 className="shrink-0 text-3xl font-bold text-white">Global Settings</h1>
                <div className="border-b border-white/10">
                    <CreateUserForm />
                </div>
                <div className="border-b border-white/10">
                    <CreateProjectForm />
                </div>
                <div className="border-b border-white/10">
                    <CreateQuotaForm title="Create Global Quota" />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <div className="mb-3">
                        <AlertBox message={quotaError} variant="error" className="mt-0" />
                        <AlertBox message={quotaSuccess} variant="success" className="mt-0" />
                    </div>
                    <QuotasTable title="Global Quotas" rows={quotas} showUser={true} onAction={handleDeleteQuota} />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <div className="mb-3">
                        <AlertBox message={userError} variant="error" className="mt-0" />
                        <AlertBox message={userSuccess} variant="success" className="mt-0" />
                    </div>
                    <UsersTable title="Global Users" rows={users} onAction={handleDeleteUser} />
                </div>
            </div>
        </>
    )
}