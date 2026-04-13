import { useMemo, useState } from "react"

const SORTABLE_COLUMNS = {
    user: "User",
    key: "Key",
    period: "Refresh Frequency",
    expires_at: "Expiration Date",
    limit_name: "Limit Type",
    limit_value: "Limit Value",
    allocated: "Allocated",
    status: "Status",
}

const HIDDEN_ON_MOBILE = new Set(["expires_at", "allocated"])

export default function QuotasTable({ title = "Quotas", rows = [], showUser = false, showKey = false, onAction, actionLabel = "Delete" })
{
    const [sortBy, setSortBy] = useState("period")
    const [sortDirection, setSortDirection] = useState("asc")

    const visibleColumns = useMemo(() => {
        return Object.keys(SORTABLE_COLUMNS).filter((col) => {
            if (col === "user") return showUser
            if (col === "key") return showKey
            return true
        })
    }, [showUser, showKey])

    const normalizedRows = useMemo(() => {
        return rows.map((row) => {
            const isUserScoped = row.user_id != null
            const isKeyScoped = row.key_id != null

            return {
                ...row,
                id: row.id,
                user: row.user_name ?? "N/A",
                key: row.fingerprint ?? "N/A",
                period: row.period ?? "N/A",
                expires_at: row.expires_at ?? null,
                limit_name: row.limit_name ?? row.limit_type ?? "N/A",
                limit_value: row.limit_value,
                allocated: row.allocated,
                status: row.status ?? "N/A",
            }
        })
    }, [rows])

    const sortedRows = useMemo(() => {
        const copy = [...normalizedRows]

        copy.sort((a, b) => {
            const aVal = a[sortBy]
            const bVal = b[sortBy]

            if (sortBy === "limit_value" || sortBy === "allocated") {
                const left = Number(aVal ?? 0)
                const right = Number(bVal ?? 0)
                return sortDirection === "asc" ? left - right : right - left
            }

            if (sortBy === "expires_at") {
                const left = aVal ? new Date(aVal).getTime() : 0
                const right = bVal ? new Date(bVal).getTime() : 0
                return sortDirection === "asc" ? left - right : right - left
            }

            const left = String(aVal ?? "").toLowerCase()
            const right = String(bVal ?? "").toLowerCase()

            if (left < right) {
                return sortDirection === "asc" ? -1 : 1
            }
            if (left > right) {
                return sortDirection === "asc" ? 1 : -1
            }
            return 0
        })

        return copy
    }, [normalizedRows, sortBy, sortDirection])

    function handleSort(column) {
        if (sortBy === column) {
            setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"))
            return
        }

        setSortBy(column)
        setSortDirection("asc")
    }

    const columnCount = visibleColumns.length + (onAction ? 1 : 0)

    return (
        <div className="flex min-w-0 flex-col rounded-md bg-white/5 outline outline-1 outline-white/10">
            <div className="border-b border-white/10 bg-indigo-500/10 px-4 py-3">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-400">{title}</h3>
            </div>

            <div className="max-h-80 w-full overflow-x-auto overflow-y-auto">
                <table className="w-full table-fixed text-sm">
                    <thead className="sticky top-0 bg-gray-900">
                        <tr>
                            {visibleColumns.map((column) => (
                                <th key={column} className={`px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-gray-500${HIDDEN_ON_MOBILE.has(column) ? " hidden sm:table-cell" : ""}`}>
                                    <button
                                        type="button"
                                        onClick={() => handleSort(column)}
                                        className="inline-flex cursor-pointer items-center gap-1 hover:text-white"
                                    >
                                        {SORTABLE_COLUMNS[column]}
                                        {sortBy === column ? (
                                            <span className="text-[10px]">{sortDirection === "asc" ? "▲" : "▼"}</span>
                                        ) : null}
                                    </button>
                                </th>
                            ))}
                            {onAction && (
                                <th className="px-4 py-2 text-right text-xs font-medium tracking-wide text-gray-500">
                                    Action
                                </th>
                            )}
                        </tr>
                    </thead>

                    <tbody className="divide-y divide-white/5">
                        {sortedRows.length > 0 ? (
                            sortedRows.map((row) => (
                                <tr key={row.id} className="hover:bg-white/5">
                                    {showUser && <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.user}>{row.user}</td>}
                                    {showKey && <td className="max-w-0 truncate px-4 py-2 text-gray-300 sm:table-cell" title={row.key}>{row.key}</td>}
                                    <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.period}>{row.period}</td>
                                    <td className="hidden max-w-0 truncate px-4 py-2 text-gray-400 sm:table-cell" title={row.expires_at ?? "N/A"}>
                                        {row.expires_at ? new Date(row.expires_at).toLocaleString() : "N/A"}
                                    </td>
                                    <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.limit_name}>{row.limit_name}</td>
                                    <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.limit_value}>
                                        {row.limit_value?.toLocaleString?.() ?? row.limit_value}
                                    </td>
                                    <td className="hidden max-w-0 truncate px-4 py-2 text-gray-400 sm:table-cell" title={row.allocated}>
                                        {row.allocated?.toLocaleString?.() ?? row.allocated}
                                    </td>
                                    <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.status}>{row.status}</td>
                                    {onAction && (
                                        <td className="px-4 py-2 text-right">
                                            <button
                                                type="button"
                                                onClick={() => onAction(row)}
                                                className="cursor-pointer rounded-md border border-red-500/40 px-2 py-1 text-xs font-semibold text-red-300 transition-colors hover:bg-red-500/20 hover:text-red-200"
                                            >
                                                {actionLabel}
                                            </button>
                                        </td>
                                    )}
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan={columnCount} className="px-4 py-6 text-center text-gray-500">
                                    No quotas found
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
