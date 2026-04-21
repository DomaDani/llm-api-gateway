import { useMemo, useState } from "react"

/**
 * Displays a sortable table of users with optional delete action.
 *
 * @param {object} props - Component props.
 * @param {string} props.title - Table header title.
 * @param {Array} props.rows - User data rows to display.
 * @param {Function} props.onAction - Callback fired when the action button is clicked for a row.
 * @param {string} props.actionLabel - Label for the action button.
 * @returns {JSX.Element} The rendered table component.
 */
const SORTABLE_COLUMNS = {
    username: "Username",
    email: "Email",
    role: "Role",
    createdAt: "Created",
}

const HIDDEN_ON_MOBILE = new Set(["role", "createdAt"])

export default function UsersTable({ title = "Users", rows = [], onAction, actionLabel = "Delete" })
{
    const [sortBy, setSortBy] = useState("username")
    const [sortDirection, setSortDirection] = useState("asc")

    const sortedRows = useMemo(() => {
        const copy = [...rows]

        copy.sort((a, b) => {
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
    }, [rows, sortBy, sortDirection])

    function handleSort(column) {
        if (sortBy === column) {
            setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"))
            return
        }

        setSortBy(column)
        setSortDirection("asc")
    }

    const desktopColumnCount = onAction ? 5 : 4
    const mobileColumnCount = onAction ? 3 : 2

    return (
        <div className="flex min-w-0 flex-col rounded-md bg-white/5 outline outline-1 outline-white/10">
            <div className="border-b border-white/10 bg-indigo-500/10 px-4 py-3">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-400">{title}</h3>
            </div>

            <div className="max-h-80 overflow-auto">
                <table className="w-full table-fixed text-sm">
                    <thead className="sticky top-0 bg-gray-900">
                        <tr>
                            {Object.entries(SORTABLE_COLUMNS).map(([column, label]) => (
                                <th key={column} className={`px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-gray-500${HIDDEN_ON_MOBILE.has(column) ? " hidden sm:table-cell" : ""}`}>
                                    <button
                                        type="button"
                                        onClick={() => handleSort(column)}
                                        className="inline-flex cursor-pointer items-center gap-1 hover:text-white"
                                    >
                                        {label}
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
                                    <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.username}>{row.username}</td>
                                    <td className="max-w-0 truncate px-4 py-2 text-gray-300" title={row.email}>{row.email}</td>
                                    <td className="hidden max-w-0 truncate px-4 py-2 text-gray-400 sm:table-cell" title={row.role}>{row.role}</td>
                                    <td className="hidden max-w-0 truncate px-4 py-2 text-gray-400 sm:table-cell" title={new Date(row.createdAt)}>{new Date(row.createdAt).toLocaleDateString()}</td>
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
                                <td colSpan={mobileColumnCount} className="px-4 py-6 text-center text-gray-500 sm:hidden">
                                    No users found
                                </td>
                                <td colSpan={desktopColumnCount} className="hidden px-4 py-6 text-center text-gray-500 sm:table-cell">
                                    No users found
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
