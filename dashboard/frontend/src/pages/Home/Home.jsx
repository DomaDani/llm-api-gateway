import ActiveQuotaCard from "./components/ActiveQuotaCard"
import UsageTable from "../../components/blocks/UsageTable"
import { useProject } from "../../context/ProjectContext"
import { fetchUsageLogs } from "../../api/usageLogs/UsageLogs"
import { useEffect, useState } from "react"
import { useAuth } from "../../api/auth/AuthProvider"

// --- Placeholder data (replace with API calls later) ---

const ACTIVE_QUOTAS = [
    { name: "Monthly Token Quota", resetDate: "May 1, 2026",  used: 6800, limit: 10000 },
    { name: "Daily Request Quota", resetDate: "Apr 7, 2026",  used: 45,   limit: 100   },
    { name: "Beep", resetDate: "May 1, 2026",  used: 6800, limit: 10000 },
    { name: "Boop", resetDate: "Apr 7, 2026",  used: 45,   limit: 100   },
    
]

// --------------------------------------------------------

export default function Home()
{
    const { selectedProject } = useProject()
    const [projectLogs, setProjectLogs] = useState([])
    const [personalLogs, setPersonalLogs] = useState([])
    const { user } = useAuth()

    useEffect(() => {
        let mounted = true
        
        if (!selectedProject) {
            setProjectLogs([])
            setPersonalLogs([])
            return
        }

        fetchUsageLogs(selectedProject.id, null, false, 50)
            .then((data) => {
                if(!mounted) return
                setProjectLogs(data || [])
            })
            .catch((err) => {
                console.error("Failed to load usage logs:", err)
            })
        fetchUsageLogs(selectedProject.id, user?.id, false, 50)
            .then((data) => {
                if(!mounted) return
                setPersonalLogs(data || [])
            })
            .catch((err) => {
                console.error("Failed to load personal usage logs:", err)
            })


    }, [selectedProject])

    return (
        <div className="flex h-90 flex-col gap-4">

            {/* Top section: project name + active quotas */}
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <h1 className="shrink-0 text-3xl font-bold text-white">{selectedProject?.name || "Project Name"}</h1>
                <div className="flex max-h-70 flex-col gap-3 overflow-y-auto sm:w-96">
                    {ACTIVE_QUOTAS.map((quota) => (
                        <ActiveQuotaCard key={quota.name} {...quota} />
                    ))}
                </div>
            </div>

            {/* Bottom section: quota usage + personal usage */}
            <div className="grid min-h-0 flex-1 grid-cols-1 gap-4 md:grid-cols-2">
                <UsageTable title="Project Usage"           rows={projectLogs}    />
                <UsageTable title="Recent Personal Usage" rows={personalLogs} />
            </div>

        </div>
    )
}