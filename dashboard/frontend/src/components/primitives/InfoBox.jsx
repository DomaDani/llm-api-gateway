import { useState } from "react"

export default function InfoBox({
    value,
    title = "Created API Key",
    warning = "Make sure to save this API key now. You won't be able to see it again!",
    rows = 2,
    className = "",
}) {
    const [isVisible, setIsVisible] = useState(true)
    const shouldShow = Boolean(value) && isVisible

    if (!shouldShow) {
        return null
    }

    return (
        <div className={`rounded-md border border-amber-500/40 bg-amber-500/10 p-4 ${className}`.trim()}>
            <div className="flex items-start justify-between gap-4">
                <div>
                    <p className="text-sm font-semibold text-amber-200">{title}</p>
                    <p className="mt-1 text-xs text-amber-100/90">{warning}</p>
                </div>
                <button
                    type="button"
                    onClick={() => setIsVisible(false)}
                    className="cursor-pointer rounded-md border border-amber-300/40 px-2 py-1 text-xs font-medium text-amber-100 hover:bg-amber-200/10"
                >
                    Hide
                </button>
            </div>

            <textarea
                readOnly
                value={value}
                rows={rows}
                className="mt-3 block w-full resize-none rounded-md border border-white/10 bg-black/20 px-3 py-2 font-mono text-sm text-white"
            />
        </div>
    )
}