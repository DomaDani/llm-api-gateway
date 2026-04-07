import CreateQuotaForm from "../../components/blocks/CreateQuotaForm"
import UsersTable from "../../components/blocks/UsersTable"
import CreateUserForm from "./components/CreateUserForm"
import CreateProjectForm from "./components/CreateProjectForm"
import QuotasTable from "../../components/blocks/QuotasTable"

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

const PLACEHOLDER_QUOTAS = [
    {
        user: "GipszJakab",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
    {
        user: "GipszJakab2",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
    {
        user: "GipszJakab3",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
    {
        user: "GipszJakab4",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
    {
        user: "GipszJakab5",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
    {
        user: "GipszJakab6",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
    {
        user: "GipszJakab7",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
    {
        user: "GipszJakab8",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
    {
        user: "GipszJakab9",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
]

const TEST = [

]

export default function GlobalSettings() {
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
                    <QuotasTable title="Global Quotas" rows={PLACEHOLDER_QUOTAS} showUser={true} onAction={() => {}} />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <UsersTable title="Global Users" rows={PLACEHOLDER_USERS} onAction={() => {}} />
                </div>
            </div>
        </>
    )
}