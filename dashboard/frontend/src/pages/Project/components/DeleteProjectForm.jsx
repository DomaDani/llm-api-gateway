import { useNavigate } from "react-router-dom"

import AlertBox from "../../../components/primitives/AlertBox"
import { useProject } from "../../../context/ProjectContext"
import useProjectDeletion from "../../../hooks/useProjectDeletion"

export default function DeleteProjectForm() {
    const navigate = useNavigate()
    const { selectedProject, clearSelectedProject } = useProject()
    const { projectError, projectSuccess, handleDeleteProject } = useProjectDeletion()

    const projectName = selectedProject?.name || "this project"

    async function handleSubmit(event) {
        event.preventDefault()

        if (!selectedProject?.id) {
            return
        }

        const confirmed = window.confirm(`Delete ${projectName}? This cannot be undone.`)
        if (!confirmed) {
            return
        }

        const deleted = await handleDeleteProject(selectedProject.id)
        if (!deleted) {
            return
        }

        clearSelectedProject()
        navigate("/home", { replace: true })
    }

    return (
        <form autoComplete="off" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">Delete Project</h2>
                    <p className="mt-1 text-sm/6 text-gray-400">
                        Deleting a project removes its settings, quotas, keys, and users from the dashboard.
                    </p>
                    <div className="mt-3">
                        <AlertBox message={projectError} variant="error" className="mt-0" />
                        <AlertBox message={projectSuccess} variant="success" className="mt-0" />
                    </div>
                    <div className="mt-6 flex items-center gap-4">
                        <button
                            type="submit"
                            disabled={!selectedProject?.id}
                            className="cursor-pointer rounded-md border border-red-500/50 bg-red-500/10 px-4 py-2 text-sm font-semibold text-red-200 transition-colors hover:bg-red-500/20 disabled:cursor-not-allowed disabled:border-white/10 disabled:bg-white/5 disabled:text-gray-500"
                        >
                            Delete Project
                        </button>
                        <span className="text-sm text-gray-400">
                            {selectedProject?.name ? `Current project: ${selectedProject.name}` : "Select a project first."}
                        </span>
                    </div>
                </div>
            </div>
        </form>
    )
}
