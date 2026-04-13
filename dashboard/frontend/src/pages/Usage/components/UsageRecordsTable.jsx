import { useMemo, useState } from "react"

const SORTABLE_COLUMNS = {
    user_name: "User",
    project_name: "Project",
    timestamp: "Date / Time",
    request_count: "Requests",
    total_tokens: "Spent Tokens",
    internal_cost_final: "Price",
    fingerprint: "Key",
}

const HIDDEN_ON_MOBILE = new Set(["user_name", "project_name", "fingerprint"])

export default function UsageRecordsTable({
    title = "Usage Records",
    rows = [],
    showUser = false,
    showProject = false,
}) {
    const [sortBy, setSortBy] = useState("timestamp")
    const [sortDirection, setSortDirection] = useState("desc")

    const visibleColumns = useMemo(() => {
        return Object.keys(SORTABLE_COLUMNS).filter((column) => {
            if (column === "user_name") return showUser
            if (column === "project_name") return showProject
            return true
        })
    }, [showUser, showProject])

    const sortedRows = useMemo(() => {
        const copy = [...rows]

        const numericCols = new Set(["request_count", "total_tokens", "internal_cost_final"])

        copy.sort((leftRow, rightRow) => {
            const leftValue = leftRow[sortBy]
            const rightValue = rightRow[sortBy]

            // Numeric sorting
            if (numericCols.has(sortBy)) {
                const left = Number(leftValue ?? 0)
                const right = Number(rightValue ?? 0)
                return sortDirection === "asc" ? left - right : right - left
            }

            // Date sorting
            if (sortBy === "timestamp") {
                const left = leftValue ? new Date(leftValue).getTime() : 0
                const right = rightValue ? new Date(rightValue).getTime() : 0
                return sortDirection === "asc" ? left - right : right - left
            }

            // Fallback string sorting
            const left = String(leftValue ?? "").toLowerCase()
            const right = String(rightValue ?? "").toLowerCase()

            if (left < right) return sortDirection === "asc" ? -1 : 1
            if (left > right) return sortDirection === "asc" ? 1 : -1
            return 0
        })

        return copy
    }, [rows, sortBy, sortDirection])

    function handleSort(column) {
        if (sortBy === column) {
            setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"))
            return
        }

        setSortBy(column)
        setSortDirection("asc")
    }

    const columnCount = visibleColumns.length

    return (
        <div className="flex min-w-0 flex-col rounded-md bg-white/5 outline outline-1 outline-white/10">
            <div className="border-b border-white/10 bg-indigo-500/10 px-4 py-3">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-400">{title}</h3>
            </div>

            <div className="w-full overflow-x-auto overflow-y-auto">
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
                                const key = row.id || `${row.timestamp}-${row.fingerprint}`

                                function renderCell(column) {
                                    const hiddenClass = HIDDEN_ON_MOBILE.has(column) ? " hidden sm:table-cell" : ""

                                    if (column === "user_name") {
                                        return (
                                            <td key={column} className={`max-w-0 truncate px-4 py-3 text-gray-300${hiddenClass}`} title={row.user_name}>
                                                {row.user_name}
                                            </td>
                                        )
                                    }

                                    if (column === "project_name") {
                                        return (
                                            <td key={column} className={`max-w-0 truncate px-4 py-3 text-gray-300${hiddenClass}`} title={row.project_name}>
                                                {row.project_name}
                                            </td>
                                        )
                                    }

                                    if (column === "timestamp") {
                                        const ts = row.timestamp
                                        const display = ts
                                            ? (ts instanceof Date ? ts.toLocaleString() : new Date(ts).toLocaleString())
                                            : '-'

                                        return (
                                            <td key={column} className={`max-w-0 truncate px-4 py-3 text-gray-300${hiddenClass}`} title={String(row.timestamp)}>
                                                {display}
                                            </td>
                                        )
                                    }

                                    if (column === "request_count") {
                                        const display = row.request_count?.toLocaleString?.() ?? row.request_count ?? 0
                                        return (
                                            <td key={column} className={`max-w-0 truncate px-4 py-3 text-gray-300${hiddenClass}`} title={String(row.request_count)}>
                                                {display}
                                            </td>
                                        )
                                    }

                                    if (column === "total_tokens") {
                                        const display = Number(row.total_tokens ?? 0).toLocaleString()
                                        return (
                                            <td key={column} className={`max-w-0 truncate px-4 py-3 text-gray-300${hiddenClass}`} title={String(row.total_tokens)}>
                                                {display}
                                            </td>
                                        )
                                    }

                                    if (column === "internal_cost_final") {
                                        const display = '$' + Number(row.internal_cost_final ?? 0).toFixed(6)
                                        return (
                                            <td key={column} className={`max-w-0 truncate px-4 py-3 text-gray-300${hiddenClass}`} title={String(row.internal_cost_final)}>
                                                {display}
                                            </td>
                                        )
                                    }

                                    if (column === "fingerprint") {
                                        return (
                                            <td key={column} className={`hidden max-w-0 truncate px-4 py-3 text-gray-400 sm:table-cell`} title={row.fingerprint}>
                                                {row.fingerprint}
                                            </td>
                                        )
                                    }

                                    return (
                                        <td key={column} className={`px-4 py-3 text-gray-300${hiddenClass}`}>{String(row[column] ?? '')}</td>
                                    )
                                }

                                return (
                                    <tr key={key} className="hover:bg-white/5">
                                        {visibleColumns.map((column) => renderCell(column))}
                                    </tr>
                                )
                            })
                        ) : (
                            <tr>
                                <td colSpan={columnCount} className="px-4 py-6 text-center text-gray-500">
                                    No usage records found
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}