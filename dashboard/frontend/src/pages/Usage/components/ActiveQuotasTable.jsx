import { useMemo, useState } from "react"

/**
 * Table displaying active quotas with sortable columns and visual progress indicators.
 *
 * @param {object} props - Component props.
 * @param {string} props.title - Table header title.
 * @param {Array} props.rows - Quota data rows to display.
 * @returns {JSX.Element} The rendered table component.
 */
const SORTABLE_COLUMNS = {
    name: "Quota Name",
    limit_type: "Limit Type",
    limit_value: "Limit",
    allocated: "Used",
    percentage: "Usage %",
    reset_date: "Resets",
}

const HIDDEN_ON_MOBILE = new Set(["limit_type"])

export default function ActiveQuotasTable({ title = "Active Quotas", rows = [] }) {
    const [sortBy, setSortBy] = useState("name")
    const [sortDirection, setSortDirection] = useState("asc")

    const visibleColumns = useMemo(() => {
        return Object.keys(SORTABLE_COLUMNS)
    }, [])

    const normalizedRows = useMemo(() => {
        return rows.map((row) => {
            const limitValue = Number(row.limit_value ?? 0)
            const allocated = Number(row.allocated ?? 0)
            const percentage = limitValue > 0 ? (allocated / limitValue) * 100 : 0

            return {
                id: row.id,
                name: row.name ?? "Unnamed quota",
                limit_type: row.limit_name ?? row.limit_type ?? "",
                limit_value: row.limit_value,
                allocated: row.allocated,
                percentage,
                reset_date: row.next_reset ?? row.reset_date ?? null,
            }
        })
    }, [rows])

    const sortedRows = useMemo(() => {
        const copy = [...normalizedRows]

        copy.sort((a, b) => {
            const aVal = a[sortBy]
            const bVal = b[sortBy]

            // Handle numeric sorts
            if (sortBy === "percentage" || sortBy === "limit_value" || sortBy === "allocated") {
                const left = Number(aVal ?? 0)
                const right = Number(bVal ?? 0)
                return sortDirection === "asc" ? left - right : right - left
            }

            // Handle string sorts
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

    const getProgressBarColor = (percentage) => {
        if (percentage >= 90) return "bg-red-500"
        if (percentage >= 70) return "bg-yellow-500"
        return "bg-indigo-500"
    }

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
                                <th
                                    key={column}
                                    className={`px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-gray-500${
                                        HIDDEN_ON_MOBILE.has(column) ? " hidden sm:table-cell" : ""
                                    }`}
                                >
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
                        </tr>
                    </thead>

                    <tbody className="divide-y divide-white/5">
                        {sortedRows.length > 0 ? (
                            sortedRows.map((row) => {
                                const percentage = row.percentage || 0
                                return (
                                    <tr key={row.id || row.name} className="hover:bg-white/5">
                                        <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.name}>
                                            {row.name}
                                        </td>
                                        <td
                                            className="hidden max-w-0 truncate px-4 py-3 text-gray-400 sm:table-cell"
                                            title={row.limit_type}
                                        >
                                            {row.limit_type}
                                        </td>
                                        <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.limit_value}>
                                            {row.limit_value?.toLocaleString?.() ?? row.limit_value}
                                        </td>
                                        <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.allocated}>
                                            {row.allocated?.toLocaleString?.() ?? row.allocated}
                                        </td>
                                        <td className="px-4 py-3">
                                            <div className="flex items-center gap-2">
                                                <div className="flex-1">
                                                    <div className="h-1.5 w-full rounded-full bg-white/10">
                                                        <div
                                                            className={`h-1.5 rounded-full transition-all ${getProgressBarColor(percentage)}`}
                                                            style={{ width: `${Math.min(percentage, 100)}%` }}
                                                        />
                                                    </div>
                                                </div>
                                                <span className="min-w-12 text-right text-xs text-gray-400">
                                                    {Math.round(percentage)}%
                                                </span>
                                            </div>
                                        </td>
                                        <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.reset_date}>
                                            {row.reset_date ? new Date(row.reset_date).toLocaleString() : "N/A"}
                                        </td>
                                    </tr>
                                )
                            })
                        ) : (
                            <tr>
                                <td colSpan={visibleColumns.length} className="px-4 py-6 text-center text-gray-500">
                                    No active quotas found
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
