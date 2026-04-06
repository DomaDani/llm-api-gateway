export default function ActiveQuotaCard({ name, resetDate, used, limit })
{
    const percentage = Math.round((used / limit) * 100)
    const barColor   = percentage >= 90 ? "bg-red-500"
                     : percentage >= 70 ? "bg-yellow-500"
                     : "bg-indigo-500"

    return (
        <div className="rounded-md bg-white/5 p-4 outline outline-1 outline-white/10">
            <div className="mb-2 flex items-center justify-between">
                <span className="text-sm font-medium text-white">{name}</span>
                <span className="text-xs text-gray-400">Resets {resetDate}</span>
            </div>
            <div className="mb-1 flex items-center justify-between text-xs text-gray-400">
                <span>{used.toLocaleString()} / {limit.toLocaleString()} tokens</span>
                <span>{percentage}%</span>
            </div>
            <div className="h-1.5 w-full rounded-full bg-white/10">
                <div
                    className={`h-1.5 rounded-full transition-all ${barColor}`}
                    style={{ width: `${percentage}%` }}
                />
            </div>
        </div>
    )
}
