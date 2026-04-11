import { useMemo, useState } from "react"

const SORTABLE_COLUMNS = {
    user: "User",
    name: "Name",
    fingerprint: "Fingerprint",
    create_date: "Created",
    status: "Status",
}

const HIDDEN_ON_MOBILE = new Set(["fingerprint", "create_date"])

export default function ApiKeysTable({ title = "API Keys", rows = [], onAction, actionLabel = "Delete", showUser = true })
{
    const [sortBy, setSortBy] = useState("name")
    const [sortDirection, setSortDirection] = useState("asc")

    const visibleColumns = useMemo(() => {
        return Object.keys(SORTABLE_COLUMNS).filter((col) => {
            if (col === "user") return showUser
            return true
        })
    }, [showUser])

    const normalizedRows = useMemo(() => {
        return rows.map((row) => ({
            ...row,
            id: row.id,
            user: row.user ?? row.username ?? (row.user_id != null ? `User #${row.user_id}` : "N/A"),
            name: row.name ?? "Unnamed key",
            fingerprint: row.fingerprint ?? "N/A",
            create_date: row.create_date ?? row.created_date ?? null,
            status: row.status ?? "N/A",
        }))
    }, [rows])


    const sortedRows = useMemo(() => {
        const copy = [...normalizedRows]

        copy.sort((a, b) => {
            if (sortBy === "create_date") {
                const left = a.create_date ? new Date(a.create_date).getTime() : 0
                const right = b.create_date ? new Date(b.create_date).getTime() : 0
                return sortDirection === "asc" ? left - right : right - left
            }

            const left = String(a[sortBy] ?? "").toLowerCase()
            const right = String(b[sortBy] ?? "").toLowerCase()

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

            <div className="max-h-80 overflow-auto">
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
                                    {showUser && (
                                        <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.user}>
                                            {row.user}
                                        </td>
                                    )}
                                    <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.name}>
                                        {row.name}
                                    </td>
                                    <td className="hidden max-w-0 truncate px-4 py-2 text-gray-400 sm:table-cell" title={row.fingerprint}>
                                        {row.fingerprint}
                                    </td>
                                    <td className="hidden max-w-0 truncate px-4 py-2 text-gray-400 sm:table-cell" title={row.create_date ?? "N/A"}>
                                        {row.create_date ? new Date(row.create_date).toLocaleString() : "N/A"}
                                    </td>
                                    <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.status}>
                                        {row.status}
                                    </td>
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
                                    No API keys found
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
