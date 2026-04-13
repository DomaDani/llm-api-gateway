import { useState, useEffect } from "react"
import Dropdown from "../../../components/primitives/Dropdown"
import { fetchUserInfos } from "../../../api/management/user/Info"
import AlertBox from "../../../components/primitives/AlertBox"

export default function CreateProjectForm({ onSubmit, error = "", success = "", loading = false }) {
    const [projectName, setProjectName] = useState("")
    const [projectManager, setProjectManager] = useState(null)
    const [availableUsers, setAvailableUsers] = useState([])
    const [userMap, setUserMap] = useState({})

    useEffect(() => {
        let mounted = true
        fetchUserInfos()
            .then((data) => {
                if (!mounted) return
                if (Array.isArray(data) && data.length > 0) {
                    const names = data.map((u) => u.username)
                    const map = data.reduce((acc, u) => { acc[u.username] = u.id; return acc }, {})
                    setAvailableUsers(names)
                    setUserMap(map)
                } else {
                    setAvailableUsers([])
                    setUserMap({})
                }
            })
            .catch((err) => {
                console.error("Failed to load users:", err)
                setAvailableUsers([])
                setUserMap({})
            })

        return () => { mounted = false }
    }, [])

    async function handleSubmit(event) {
        event.preventDefault()

        const created = await onSubmit?.({
            name: projectName,
            manager_id: projectManager,
        })

        if (created) {
            setProjectName("")
            setProjectManager(null)
        }
    }

    return (
        <form autoComplete="off" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">Create New Project</h2>
                    {/* <p className="mt-1 text-sm/6 text-gray-400">
                    </p> */}
                    <div className="mt-3 space-y-8">
                        <AlertBox message={error} variant="error" className="mt-0" />
                        <AlertBox message={success} variant="success" className="mt-0" />
                    </div>
                    <div className="mt-3 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                        <div className="sm:col-span-4">
                            <label htmlFor="project-name" className="block text-sm/6 font-medium text-white">
                                Project name
                            </label>
                            <div className="mt-2">
                                <input
                                    id="project-name"
                                    name="project-name"
                                    type="text"
                                    placeholder="Project Name"
                                    autoComplete="off"
                                    value={projectName}
                                    onChange={(event) => setProjectName(event.target.value)}
                                    required
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <label htmlFor="project-manager" className="block text-sm/6 font-medium text-white">
                                Project Manager
                            </label>
                            <div className="mt-2">
                                <Dropdown
                                    items={availableUsers}
                                    itemName="user"
                                    onSelect={(name) => {
                                        setProjectManager(userMap[name] ?? null)
                                    }}
                                    required
                                    name="project-manager"
                                />
                            </div>
                        </div>

                    </div>
                    <div className="sm:col-span-4 pt-6">
                        <button
                            type="submit"
                            disabled={loading}
                            className={`rounded-md px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 ${loading ? "cursor-not-allowed bg-indigo-400" : "cursor-pointer bg-indigo-500 hover:bg-indigo-400"}`}
                        >
                            {loading ? "Creating project..." : "Submit"}
                        </button>
                    </div>
                </div>
            </div>
        </form>
    )
}
