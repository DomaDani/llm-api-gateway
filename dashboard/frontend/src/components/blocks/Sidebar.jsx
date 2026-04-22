// Source: https://tailwindflex.com/@oliver-hansen/tailwind-sidebar-layout
// Reworked for react and navigation.
import { useEffect, useState } from "react"
import { NavLink } from "react-router-dom"
import { useAuth } from "../../api/auth/AuthProvider"
import Dropdown from "../primitives/Dropdown"
import { fetchProjectInfosForUser } from "../../api/management/project/Info"
import { useProject } from "../shared/ProjectContext"

/**
 * Main layout sidebar with navigation menu and project selector.
 *
 * @param {object} props - Component props.
 * @param {JSX.Element} props.children - Page content to render in the main area.
 * @returns {JSX.Element} The rendered sidebar layout component.
 */
export default function Sidebar({ children })
{
    const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false)
    const { logout, user } = useAuth()
    const { selectedProject, selectProject } = useProject()
    const [projects, setProjects] = useState([])

    useEffect(() => {
        let mounted = true

        fetchProjectInfosForUser()
            .then((data) => {
                if (!mounted) return
                setProjects(data || [])
                if (!selectedProject && Array.isArray(data) && data.length > 0) {
                    selectProject(data[0])
                }
            })
            .catch((err) => {
                console.error("Failed to load projects:", err)
            })

        return () => { mounted = false }
    }, [selectedProject, selectProject])

    return (
        <div className="flex h-screen w-full overflow-x-hidden bg-gray-900">

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

                    {user?.is_admin && (
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
                    )}

                    {selectedProject && (user?.is_admin || user?.is_project_manager) && (
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
                            Project Settings
                        </NavLink>
                    )}

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
                        API Keys
                    </NavLink>

                    {/* <NavLink
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
                    </NavLink> */}

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
            <div className="flex min-w-0 flex-1 flex-col">

                {/* Top bar */}
                <div className="flex h-16 min-w-0 items-center justify-between border-b border-white/10 bg-gray-900 px-2 sm:px-0">
                    <div className="flex min-w-0 flex-1 items-center px-2 sm:px-4">
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
                        <Dropdown
                            items={projects.map((p) => p.name)}
                            itemName="project"
                            containerClassName="mx-2 min-w-0 w-full max-w-28 sm:mx-4 sm:max-w-64"
                            selectFirst={!selectedProject}
                            initialSelected={selectedProject?.name ?? null}
                            onSelect={(name) => {
                                const proj = projects.find((p) => p.name === name)
                                if (proj) selectProject(proj)
                            }}
                        />
                    </div>

                    <div className="flex shrink-0 items-center gap-2 pr-2 sm:gap-4 sm:pr-4">
                        <NavLink
                            to="/profile"
                            className={({ isActive }) =>
                                `text-xs font-medium transition-colors sm:text-sm ${
                                    isActive
                                        ? "text-white font-bold"
                                        : "text-gray-400 hover:text-white"
                                }`
                            }
                        >
                            PROFILE
                        </NavLink>
                        <button
                            type="button"
                            onClick={logout}
                            className="cursor-pointer text-xs font-medium text-gray-400 transition-colors hover:text-white sm:text-sm"
                        >
                            SIGN OUT
                        </button>
                    </div>
                </div>

                {/* Page content */}
                <div className="flex min-h-0 min-w-0 flex-1 flex-col overflow-y-auto p-4 text-white sm:p-10">
                    {children}
                </div>

            </div>
        </div>
    )
}