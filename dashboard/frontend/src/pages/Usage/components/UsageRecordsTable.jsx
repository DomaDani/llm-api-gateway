import { useMemo, useState } from "react"

const SORTABLE_COLUMNS = {
    user: "User",
    project: "Project",
    created_at: "Date / Time",
    requests: "Requests",
    spent_tokens: "Spent Tokens",
    price: "Price",
    key: "Key",
}

const HIDDEN_ON_MOBILE = new Set(["user", "project", "key"])

export default function UsageRecordsTable({
    title = "Usage Records",
    rows = [],
    showUser = false,
    showProject = false,
}) {
    const [sortBy, setSortBy] = useState("created_at")
    const [sortDirection, setSortDirection] = useState("desc")

    const visibleColumns = useMemo(() => {
        return Object.keys(SORTABLE_COLUMNS).filter((column) => {
            if (column === "user") return showUser
            if (column === "project") return showProject
            return true
        })
    }, [showUser, showProject])

    const sortedRows = useMemo(() => {
        const copy = [...rows]

        copy.sort((leftRow, rightRow) => {
            const leftValue = leftRow[sortBy]
            const rightValue = rightRow[sortBy]

            if (sortBy === "requests" || sortBy === "spent_tokens" || sortBy === "price") {
                const left = Number(leftValue ?? 0)
                const right = Number(rightValue ?? 0)
                return sortDirection === "asc" ? left - right : right - left
            }

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
                            sortedRows.map((row) => (
                                <tr key={row.id || `${row.created_at}-${row.key}`} className="hover:bg-white/5">
                                    {showUser && (
                                        <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.user}>
                                            {row.user}
                                        </td>
                                    )}
                                    {showProject && (
                                        <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.project}>
                                            {row.project}
                                        </td>
                                    )}
                                    <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.created_at}>
                                        {row.created_at}
                                    </td>
                                    <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.requests}>
                                        {row.requests?.toLocaleString?.() ?? row.requests}
                                    </td>
                                    <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.spent_tokens}>
                                        {row.spent_tokens?.toLocaleString?.() ?? row.spent_tokens}
                                    </td>
                                    <td className="max-w-0 truncate px-4 py-3 text-gray-300" title={row.price}>
                                        {row.price}
                                    </td>
                                    <td className="hidden max-w-0 truncate px-4 py-3 text-gray-400 sm:table-cell" title={row.key}>
                                        {row.key}
                                    </td>
                                </tr>
                            ))
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