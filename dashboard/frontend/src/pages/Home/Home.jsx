import ActiveQuotaCard from "./components/ActiveQuotaCard"
import UsageTable from "../../components/blocks/UsageTable"

// --- Placeholder data (replace with API calls later) ---

const ACTIVE_QUOTAS = [
    { name: "Monthly Token Quota", resetDate: "May 1, 2026",  used: 6800, limit: 10000 },
    { name: "Daily Request Quota", resetDate: "Apr 7, 2026",  used: 45,   limit: 100   },
    { name: "Monthly Token Quota", resetDate: "May 1, 2026",  used: 6800, limit: 10000 },
    { name: "Daily Request Quota", resetDate: "Apr 7, 2026",  used: 45,   limit: 100   },
    
]


// limit return amount by implementing argument in backend
const QUOTA_USAGE = [
    { time: "Apr 6, 2026 14:32", tokens: 1240, price: "$0.012" },
    { time: "Apr 6, 2026 11:15", tokens:  870, price: "$0.008" },
    { time: "Apr 5, 2026 19:48", tokens: 2100, price: "$0.021" },
    { time: "Apr 5, 2026 10:03", tokens:  450, price: "$0.004" },
    { time: "Apr 4, 2026 16:22", tokens:  980, price: "$0.010" },
    { time: "Apr 6, 2026 14:32", tokens: 1240, price: "$0.012" },
    { time: "Apr 6, 2026 11:15", tokens:  870, price: "$0.008" },
    { time: "Apr 5, 2026 19:48", tokens: 2100, price: "$0.021" },
    { time: "Apr 5, 2026 10:03", tokens:  450, price: "$0.004" },
    { time: "Apr 4, 2026 16:22", tokens:  980, price: "$0.010" },
    { time: "Apr 6, 2026 14:32", tokens: 1240, price: "$0.012" },
    { time: "Apr 6, 2026 11:15", tokens:  870, price: "$0.008" },
    { time: "Apr 5, 2026 19:48", tokens: 2100, price: "$0.021" },
    { time: "Apr 5, 2026 10:03", tokens:  450, price: "$0.004" },
    { time: "Apr 4, 2026 16:22", tokens:  980, price: "$0.010" },
]

const PERSONAL_USAGE = [
    { time: "Apr 6, 2026 14:32", tokens: 340, price: "$0.003" },
    { time: "Apr 6, 2026 11:15", tokens: 210, price: "$0.002" },
    { time: "Apr 5, 2026 19:48", tokens: 590, price: "$0.006" },
    { time: "Apr 5, 2026 10:03", tokens: 120, price: "$0.001" },
]

// --------------------------------------------------------

export default function Home()
{
    return (
        <div className="flex h-90 flex-col gap-4">

            {/* Top section: project name + active quotas */}
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <h1 className="shrink-0 text-3xl font-bold text-white">Project Name</h1>
                <div className="flex max-h-70 flex-col gap-3 overflow-y-auto sm:w-96">
                    {ACTIVE_QUOTAS.map((quota) => (
                        <ActiveQuotaCard key={quota.name} {...quota} />
                    ))}
                </div>
            </div>

            {/* Bottom section: quota usage + personal usage */}
            <div className="grid min-h-0 flex-1 grid-cols-1 gap-4 md:grid-cols-2">
                <UsageTable title="Quota Usage"           rows={QUOTA_USAGE}    />
                <UsageTable title="Recent Personal Usage" rows={PERSONAL_USAGE} />
            </div>

        </div>
    )
}