import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react"

const STORAGE_KEY = "selectedProject"

const ProjectContext = createContext(null)

/**
 * @typedef {object} ProjectContextValue
 * @property {object | null} selectedProject - Currently selected project object.
 * @property {number | null} selectedProjectId - ID of the selected project.
 * @property {Function} selectProject - Set the selected project.
 * @property {Function} clearSelectedProject - Clear the selected project.
 */

function readStoredProject() {
    if (typeof window === "undefined") {
        return null
    }

    const storedProject = window.localStorage.getItem(STORAGE_KEY)

    if (!storedProject) {
        return null
    }

    try {
        return JSON.parse(storedProject)
    } catch {
        return storedProject
    }
}

/**
 * Provides project selection context with localStorage persistence.
 *
 * @param {object} props - Component props.
 * @param {JSX.Element} props.children - Child components.
 * @returns {JSX.Element} The rendered provider.
 */
export function ProjectProvider({ children }) {
    const [selectedProject, setSelectedProject] = useState(() => readStoredProject())

    useEffect(() => {
        if (typeof window === "undefined") {
            return
        }

        if (selectedProject) {
            window.localStorage.setItem(STORAGE_KEY, JSON.stringify(selectedProject))
            return
        }

        window.localStorage.removeItem(STORAGE_KEY)
    }, [selectedProject])

    const selectProject = useCallback((project) => {
        setSelectedProject(project ?? null)
    }, [])

    const clearSelectedProject = useCallback(() => {
        setSelectedProject(null)
    }, [])

    const value = useMemo(() => ({
        selectedProject,
        selectedProjectId: selectedProject?.id ?? null,
        selectProject,
        clearSelectedProject,
    }), [clearSelectedProject, selectProject, selectedProject])

    return (
        <ProjectContext.Provider value={value}>
            {children}
        </ProjectContext.Provider>
    )
}

/**
 * Hook to access the project context.
 *
 * @returns {ProjectContextValue} The project context value with selection methods.
 * @throws {Error} If used outside of ProjectProvider.
 */
export function useProject() {
    const context = useContext(ProjectContext)

    if (!context) {
        throw new Error("useProject must be used within a ProjectProvider")
    }

    return context
}
