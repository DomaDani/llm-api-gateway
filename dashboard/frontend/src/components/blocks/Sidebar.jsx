// Source: https://tailwindflex.com/@oliver-hansen/tailwind-sidebar-layout
// Reworked for react and navigation.
import { useState } from "react"
import { NavLink } from "react-router-dom"
import Dropdown from "../primitives/Dropdown"

const PLACEHOLDER_PROJECTS = [
    "Project 1",
    "Project 2",
    "Project 3",
    "Project 4",
    "Project 5",
]

export default function Sidebar({ children })
{
    const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false)

    return (
        <div className="flex h-screen bg-gray-900">

            {/* Mobile backdrop */}
            {isMobileSidebarOpen && (
                <button
                    type="button"
                    aria-label="Close sidebar overlay"
                    className="fixed inset-0 z-20 bg-black/60 md:hidden"
                    onClick={() => setIsMobileSidebarOpen(false)}
                />
            )}

            {/* Sidebar */}
            <div
                className={`fixed inset-y-0 left-0 z-30 flex w-64 flex-col bg-gray-900 transition-transform duration-300 ease-in-out md:static md:z-auto md:translate-x-0 ${
                    isMobileSidebarOpen ? "translate-x-0" : "-translate-x-full"
                }`}
            >
                <div className="flex h-16 items-center justify-center border-b border-white/10">
                    <span className="font-bold uppercase tracking-tight text-white">LLM API Gateway</span>
                </div>

                <nav className="flex-1 overflow-y-auto px-2 py-4">
                    <NavLink
                        to="/home"
                        className={({ isActive }) =>
                            `flex items-center rounded-md px-4 py-2 text-sm font-medium transition-colors ${
                                isActive
                                    ? "bg-indigo-500/20 text-white"
                                    : "text-gray-400 hover:bg-white/5 hover:text-white"
                            }`
                        }
                        onClick={() => setIsMobileSidebarOpen(false)}
                    >
                        Home
                    </NavLink>

                    <NavLink
                        to="/global"
                        className={({ isActive }) =>
                            `mt-1 flex items-center rounded-md px-4 py-2 text-sm font-medium transition-colors ${
                                isActive
                                    ? "bg-indigo-500/20 text-white"
                                    : "text-gray-400 hover:bg-white/5 hover:text-white"
                            }`
                        }
                        onClick={() => setIsMobileSidebarOpen(false)}
                    >
                        Global Settings
                    </NavLink>

                    <NavLink
                        to="/project"
                        className={({ isActive }) =>
                            `mt-1 flex items-center rounded-md px-4 py-2 text-sm font-medium transition-colors ${
                                isActive
                                    ? "bg-indigo-500/20 text-white"
                                    : "text-gray-400 hover:bg-white/5 hover:text-white"
                            }`
                        }
                        onClick={() => setIsMobileSidebarOpen(false)}
                    >
                        Project settings
                    </NavLink>

                    <NavLink
                        to="/keys"
                        className={({ isActive }) =>
                            `mt-1 flex items-center rounded-md px-4 py-2 text-sm font-medium transition-colors ${
                                isActive
                                    ? "bg-indigo-500/20 text-white"
                                    : "text-gray-400 hover:bg-white/5 hover:text-white"
                            }`
                        }
                        onClick={() => setIsMobileSidebarOpen(false)}
                    >
                        API keys
                    </NavLink>

                    <NavLink
                        to="/statistics"
                        className={({ isActive }) =>
                            `mt-1 flex items-center rounded-md px-4 py-2 text-sm font-medium transition-colors ${
                                isActive
                                    ? "bg-indigo-500/20 text-white"
                                    : "text-gray-400 hover:bg-white/5 hover:text-white"
                            }`
                        }
                        onClick={() => setIsMobileSidebarOpen(false)}
                    >
                        Statistics
                    </NavLink>

                    <NavLink
                        to="/usage"
                        className={({ isActive }) =>
                            `mt-1 flex items-center rounded-md px-4 py-2 text-sm font-medium transition-colors ${
                                isActive
                                    ? "bg-indigo-500/20 text-white"
                                    : "text-gray-400 hover:bg-white/5 hover:text-white"
                            }`
                        }
                        onClick={() => setIsMobileSidebarOpen(false)}
                    >
                        Usage
                    </NavLink>
                </nav>
            </div>

            {/* Main content */}
            <div className="flex flex-1 flex-col">

                {/* Top bar */}
                <div className="flex h-16 items-center justify-between border-b border-white/10 bg-gray-900">
                    <div className="flex items-center px-4">
                        <button
                            type="button"
                            aria-label="Toggle sidebar"
                            className="text-gray-400 hover:text-white focus:outline-none md:hidden"
                            onClick={() => setIsMobileSidebarOpen((prev) => !prev)}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                        <Dropdown items={PLACEHOLDER_PROJECTS} itemName="project" />
                    </div>

                    <div className="flex items-center pr-4">
                        <NavLink
                            to="/profile"
                            className={({ isActive }) =>
                                `text-sm font-medium transition-colors ${
                                    isActive
                                        ? "text-white font-bold"
                                        : "text-gray-400 hover:text-white"
                                }`
                            }
                        >
                            PROFILE
                        </NavLink>
                    </div>
                </div>

                {/* Page content */}
                <div className="flex flex-1 flex-col overflow-y p-10 text-white">
                    {children}
                </div>

            </div>
        </div>
    )
}