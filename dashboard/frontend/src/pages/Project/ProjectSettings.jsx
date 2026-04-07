import UsersTable from "../../components/blocks/UsersTable"
import QuotasTable from "../../components/blocks/QuotasTable"
import ApiKeysTable from "../../components/blocks/ApiKeysTable"
import CreateQuotaForm from "../../components/blocks/CreateQuotaForm"
import AddUserForm from "./components/AddUserForm"

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
        key: "GipszJakab:asdfsafd",
        period: "Daily",
        expires_at: "n/a",
        limit_name: "Token Limit",
        limit_value: "500000",
        allocated: "12354",
        status: "Active",
    },
]

const PLACEHOLDER_KEYS = [
    {
        user: "GipszJakab",
        name: "test key",
        fingerprint: "asdfasdf",
        created_date: "2026-03-20",
        status: "Active"
    }
]

export default function ProjectSetings() {
    return (
        <>
            <div className="flex flex-col gap-5">
                <div className="border-b border-white/10">
                    <AddUserForm />
                </div>
                <div className="border-b border-white/10">
                    <CreateQuotaForm title="Create Project Quota" enableKeyTarget="true" />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <QuotasTable title="Project Quotas" rows={PLACEHOLDER_QUOTAS} showUser="true" showKey="true" onAction={() => { }} />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <UsersTable title="Project Users" rows={PLACEHOLDER_USERS} onAction={() => { }} actionLabel="Remove" />
                </div>
                <div className="border-b border-white/10 pb-5">
                    <ApiKeysTable title="Project API Keys" rows={PLACEHOLDER_KEYS} onAction={() => { }} />
                </div>
            </div>
        </>
    )
}