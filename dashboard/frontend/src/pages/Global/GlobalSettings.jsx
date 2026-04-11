import CreateQuotaForm from "../../components/blocks/CreateQuotaForm"
import UsersTable from "../../components/blocks/UsersTable"
import CreateUserForm from "./components/CreateUserForm"
import CreateProjectForm from "./components/CreateProjectForm"
import QuotasTable from "../../components/blocks/QuotasTable"
import { useEffect, useState} from "react"
import { fetchQuotaInfos } from "../../api/management/quotas/Info"
import AlertBox from "../../components/primitives/AlertBox"
import useQuotaDeletion from "../../hooks/useQuotaDeletion"

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
    {
        id: "u-4",
        username: "david",
        email: "david@example.com",
        role: "project manager",
        createdAt: "2026-04-03",
    },
        {
        id: "u-5",
        username: "alice",
        email: "alice@example.com",
        role: "administrator",
        createdAt: "2026-03-20",
    },
    {
        id: "u-6",
        username: "bence",
        email: "bence@example.com",
        role: "project manager",
        createdAt: "2026-03-25",
    },
    {
        id: "u-7",
        username: "csilla",
        email: "csilla@example.com",
        role: "user",
        createdAt: "2026-04-01",
    },
    {
        id: "u-8",
        username: "david",
        email: "david@example.com",
        role: "project manager",
        createdAt: "2026-04-03",
    },
        {
        id: "u-9",
        username: "alice",
        email: "alice@example.com",
        role: "administrator",
        createdAt: "2026-03-20",
    },
    {
        id: "u-10",
        username: "bence",
        email: "bence@example.com",
        role: "project manager",
        createdAt: "2026-03-25",
    },
    {
        id: "u-11",
        username: "csilla",
        email: "csilla@example.com",
        role: "user",
        createdAt: "2026-04-01",
    },
    {
        id: "u-12",
        username: "david",
        email: "david@example.com",
        role: "project manager",
        createdAt: "2026-04-03",
    },
        {
        id: "u-13",
        username: "alice",
        email: "alice@example.com",
        role: "administrator",
        createdAt: "2026-03-20",
    },
    {
        id: "u-14",
        username: "bence",
        email: "bence@example.com",
        role: "project manager",
        createdAt: "2026-03-25",
    },
    {
        id: "u-15",
        username: "csilla",
        email: "csilla@example.com",
        role: "user",
        createdAt: "2026-04-01",
    },
    {
        id: "u-16",
        username: "vmjpoqwrfsscobbgayziqdbdtnqpaqdrdxrpbapodzkuanexveiwxjhpwvofdwfxsywnbcunmbelixqvpduvkoqewdfqwngwwikwjfannacmspcguffguplfxosqlriljnatyoykaclcxjwgdydzubuywgdgbuobdneylleihizzhxfsfyfmvdrekgchcuomjxzknaxdulmwaivqkbiemhqhbepifsdxniouqeuf",
        email: "david@example.com",
        role: "project manager",
        createdAt: "2026-04-03",
    },
]

export default function GlobalSettings() {
    const [quotas, setQuotas] = useState([])
    const { quotaError, quotaSuccess, quotaReloadKey, handleDeleteQuota } = useQuotaDeletion({ quotas, setQuotas })

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
                    <UsersTable title="Global Users" rows={PLACEHOLDER_USERS} onAction={() => {}} />
                </div>
            </div>
        </>
    )
}