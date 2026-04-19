/**
 * Card displaying a single active quota with usage progress bar and reset date.
 *
 * @param {object} props - Component props.
 * @param {string} props.name - Quota name.
 * @param {string} props.resetDate - Date/time when the quota resets.
 * @param {number} props.used - Current usage amount.
 * @param {number} props.limit - Maximum limit value.
 * @param {string} props.type - Quota type (e.g., 'Request Limit', 'Token Limit').
 * @returns {JSX.Element} The rendered quota card.
 */
export default function ActiveQuotaCard({ name, resetDate, used, limit, type })
{
    let typeName = ""
    if (type === "Request Limit") typeName = "Requests"
    if (type === "Token Limit") typeName = "Tokens"
    if (type === "Price Limit") typeName = "$"

    resetDate = resetDate ? new Date(resetDate).toLocaleString() : "N/A"
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
                <span>{used.toLocaleString()} / {limit.toLocaleString()} {typeName}</span>
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
