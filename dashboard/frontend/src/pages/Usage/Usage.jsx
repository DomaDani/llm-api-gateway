import ActiveQuotasTable from "./components/ActiveQuotasTable"
import UsageRecordsTable from "./components/UsageRecordsTable"

// --- Placeholder data (replace with API calls later) ---
const ACTIVE_QUOTAS = [
    {
        id: 1,
        name: "Monthly Token Quota",
        limit_type: "Tokens",
        limit_value: 10000,
        allocated: 6800,
        percentage: 68,
        reset_date: "May 1, 2026",
    },
    {
        id: 2,
        name: "Daily Request Quota",
        limit_type: "Requests",
        limit_value: 100,
        allocated: 45,
        percentage: 45,
        reset_date: "Apr 8, 2026",
    },
    {
        id: 3,
        name: "Hourly Rate Limit",
        limit_type: "Requests/Hour",
        limit_value: 1000,
        allocated: 892,
        percentage: 89,
        reset_date: "Apr 7, 2026 22:00",
    },
    {
        id: 4,
        name: "Concurrent Requests",
        limit_type: "Connections",
        limit_value: 50,
        allocated: 47,
        percentage: 94,
        reset_date: "Ongoing",
    },
]

// --- Placeholder data (replace with API calls later) ---
const USAGE_RECORDS = [
    {
        id: 1,
        project: "Project Alpha",
        user: "GipszJakab",
        created_at: "Apr 7, 2026 14:00",
        requests: 12,
        spent_tokens: 1240,
        price: "$0.012",
        key: "9f8a...",
    },
    {
        id: 2,
        project: "Project Beta",
        user: "GipszJakab2",
        created_at: "Apr 7, 2026 11:15",
        requests: 8,
        spent_tokens: 870,
        price: "$0.008",
        key: "9f8a...",
    },
    {
        id: 3,
        project: "Project Alpha",
        user: "GipszJakab",
        created_at: "Apr 6, 2026 19:45",
        requests: 20,
        spent_tokens: 2100,
        price: "$0.021",
        key: "9f8a...",
    },
    {
        id: 4,
        project: "Project Gamma",
        user: "GipszJakab3",
        created_at: "Apr 6, 2026 10:30",
        requests: 5,
        spent_tokens: 450,
        price: "$0.004",
        key: "9f8a...",
    },
]
// --------------------------------------------------------

export default function Usage() {
    return (
        <div className="flex flex-col gap-5">
            <h1 className="shrink-0 text-3xl font-bold text-white">Usage</h1>
            <div className="border-b border-white/10 pb-5">
                <ActiveQuotasTable title="Active Quotas" rows={ACTIVE_QUOTAS} />
            </div>
            <div className="border-b border-white/10 pb-5">
                <UsageRecordsTable title="Global Usage" rows={USAGE_RECORDS} showProject={true} showUser={true} />
            </div>
            <div className="border-b border-white/10 pb-5">
                <UsageRecordsTable title="Project Usage" rows={USAGE_RECORDS} showUser={true} />
            </div>
            <div className="border-b border-white/10 pb-5">
                <UsageRecordsTable title="Personal Usage" rows={USAGE_RECORDS} />
            </div>
        </div>
    )
}