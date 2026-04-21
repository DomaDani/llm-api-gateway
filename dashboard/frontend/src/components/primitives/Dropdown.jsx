// Source: AI scaffolded

import { useState, useRef, useEffect } from "react"

/**
 * Searchable dropdown component with optional auto-selection and required validation.
 *
 * @param {object} props - Component props.
 * @param {string[]} props.items - List of selectable items.
 * @param {string} props.itemName - Singular name for the item type (e.g., "project").
 * @param {Function} props.onSelect - Callback fired when an item is selected.
 * @param {string} props.containerClassName - CSS classes for the dropdown container.
 * @param {boolean} props.required - Whether selection is required for form validation.
 * @param {string} props.name - HTML name attribute for the hidden input.
 * @param {boolean} props.selectFirst - Whether to auto-select the first item if none selected.
 * @param {string} props.initialSelected - Initially selected item value.
 * @returns {JSX.Element} The rendered dropdown component.
 */
export default function Dropdown({ items = [], itemName, onSelect, containerClassName = "", required = false, name, selectFirst = false, initialSelected = null })
{
    const [isOpen, setIsOpen]       = useState(false)
    const [search, setSearch]       = useState("")
    const [selected, setSelected]   = useState(initialSelected)
    const containerRef              = useRef(null)

    const filtered = items.filter((p) =>
        p.toLowerCase().includes(search.toLowerCase())
    )

    function handleSelect(items) {
        setSelected(items)
        setSearch("")
        setIsOpen(false)
        onSelect?.(items)
    }

    useEffect(() => {
        if (selectFirst && items.length > 0 && !selected) {
            handleSelect(items[0])
        }
    }, [selectFirst, items, selected])

    useEffect(() => {
        if (initialSelected) {
            setSelected(initialSelected)
        }
    }, [initialSelected])

    useEffect(() => {
        function handleClickOutside(e) {
            if (containerRef.current && !containerRef.current.contains(e.target)) {
                setIsOpen(false)
                setSearch("")
            }
        }
        document.addEventListener("mousedown", handleClickOutside)
        return () => document.removeEventListener("mousedown", handleClickOutside)
    }, [])

    return (
        <div ref={containerRef} className={`relative ${containerClassName}`.trim()}>

            {/* Invisible validation input is positioned over the control so native tooltip appears in-place. */}
            <input
                name={name ?? `dropdown-${itemName?.toLowerCase().replace(/\s+/g, "-")}`}
                value={selected ?? ""}
                required={required}
                onChange={() => {}}
                className="pointer-events-none absolute inset-0 h-full w-full opacity-0"
            />

            {/* Trigger button */}
            <button
                type="button"
                onClick={() => setIsOpen((prev) => !prev)}
                aria-required={required}
                className="flex w-full items-center justify-between rounded-md bg-white/5 px-3 py-1.5 text-sm text-white outline-1 -outline-offset-1 outline-white/10 hover:bg-white/10 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
            >
                <span className={`min-w-0 flex-1 truncate text-left ${selected ? "text-white" : "text-gray-500"}`}>
                    {selected ?? `Select ${itemName}...`}
                </span>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className={`ml-2 h-4 w-4 flex-shrink-0 text-gray-400 transition-transform ${isOpen ? "rotate-180" : ""}`}
                    fill="none" viewBox="0 0 24 24" stroke="currentColor"
                >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
            </button>

            {/* Dropdown panel */}
            {isOpen && (
                <div className="absolute left-0 top-full z-50 mt-1 w-full rounded-md bg-gray-800 py-1 shadow-lg outline-1 outline-white/10">

                    {/* Search input */}
                    <div className="px-2 pb-1">
                        <input
                            autoFocus
                            type="text"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            placeholder="Search…"
                            className="w-full rounded-md bg-white/5 px-3 py-1.5 text-sm text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
                        />
                    </div>

                    {/* Item list */}
                    <ul className="max-h-48 overflow-y-auto">
                        {filtered.length > 0 ? (
                            filtered.map((items) => (
                                <li key={items}>
                                    <button
                                        type="button"
                                        onClick={() => handleSelect(items)}
                                        className={`w-full px-3 py-2 text-left text-sm transition-colors hover:bg-white/5 hover:text-white ${
                                            selected === items
                                                ? "bg-indigo-500/20 text-white"
                                                : "text-gray-400"
                                        }`}
                                    >
                                        {items}
                                    </button>
                                </li>
                            ))
                        ) : (
                            <li className="px-3 py-2 text-sm text-gray-500">No {itemName} found</li>
                        )}
                    </ul>
                </div>
            )}
        </div>
    )
}
