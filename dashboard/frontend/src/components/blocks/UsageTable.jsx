export default function UsageTable({ title, rows = [] })
{
    return (
        <div className="flex flex-col rounded-md bg-white/5 outline outline-1 outline-white/10">

            {/* Table header */}
            <div className="border-b border-white/10 px-4 py-3 bg-indigo-500/10">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-400">{title}</h3>
            </div>

            {/* Scrollable body */}
            <div className="max-h-64 overflow-y-auto">
                <table className="w-full table-fixed text-sm">
                    <thead className="sticky top-0 bg-gray-900">
                        <tr>
                            <th className="px-4 py-2 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Time</th>
                            <th className="px-4 py-2 text-right text-xs font-medium uppercase tracking-wide text-gray-500">Tokens</th>
                            <th className="px-4 py-2 text-right text-xs font-medium uppercase tracking-wide text-gray-500">Price</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {rows.length > 0 ? (
                            rows.map((row, i) => (
                                <tr key={i} className="hover:bg-white/5">
                                    <td className="px-4 py-2 text-gray-400">{row.time}</td>
                                    <td className="px-4 py-2 text-right text-gray-300">{row.tokens.toLocaleString()}</td>
                                    <td className="px-4 py-2 text-right text-gray-300">{row.price}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan={3} className="px-4 py-6 text-center text-gray-500">No data</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
