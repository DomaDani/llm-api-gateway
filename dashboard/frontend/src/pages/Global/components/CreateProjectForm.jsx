import { useState } from "react"
import Dropdown from "../../../components/primitives/Dropdown"

const PLACEHOLDER_USERS = [
    "User 1",
    "User 2",
    "User 3",
    "User 4",
    "User 5",
]

export default function CreateProjectForm({ users = PLACEHOLDER_USERS, onSubmit }) {
    const [projectName, setProjectName] = useState("")
    const [projectManager, setProjectManager] = useState(null)

    function handleSubmit(event) {
        event.preventDefault()
        onSubmit?.({
            projectName,
            projectManager,
        })
    }

    return (
        <form autoComplete="off" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">Create New Project</h2>
                    {/* <p className="mt-1 text-sm/6 text-gray-400">
                    </p> */}
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
                                    items={users}
                                    itemName="user"
                                    onSelect={setProjectManager}
                                    required
                                    name="project-manager"
                                />
                            </div>
                        </div>

                    </div>
                    <div className="sm:col-span-4 pt-6">
                        <button
                            type="submit"
                            className="cursor-pointer rounded-md bg-indigo-500 px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 hover:bg-indigo-400"
                        >
                            Submit
                        </button>
                    </div>
                </div>
            </div>
        </form>
    )
}
