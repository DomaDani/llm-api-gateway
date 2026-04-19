import ActiveQuotaCard from "./components/ActiveQuotaCard"
import UsageTable from "../../components/blocks/UsageTable"
import { useProject } from "../../components/shared/ProjectContext"
import { fetchUsageLogs } from "../../api/usageLogs/UsageLogs"
import { useEffect, useState } from "react"
import { useAuth } from "../../api/auth/AuthProvider"
import { fetchQuotaInfos } from "../../api/management/quotas/Info"

/**
 * Dashboard home page showing selected project overview with active quotas and usage logs.
 *
 * @returns {JSX.Element} The rendered home page.
 */
export default function Home()
{
    const { selectedProject } = useProject()
    const [projectLogs, setProjectLogs] = useState([])
    const [personalLogs, setPersonalLogs] = useState([])
    const { user } = useAuth()
    const [activeQuotas, setActiveQuotas] = useState([])

    useEffect(() => {
        let mounted = true
        
        if (!selectedProject) {
            setProjectLogs([])
            setPersonalLogs([])
            setActiveQuotas([])
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
        fetchQuotaInfos(selectedProject.id)
            .then((data) => {
                if(!mounted) return
                setActiveQuotas(data || [])
            })
            .catch((err) => {
                console.error("Failed to load active quotas:", err)
            })

        return () => { mounted = false }
    }, [selectedProject])

    return (
        <div className="flex h-90 flex-col gap-4">

            {/* Top section: project name + active quotas */}
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <h1 className="shrink-0 text-3xl font-bold text-white">{selectedProject?.name || "Project Name"}</h1>
                <div className="flex max-h-70 flex-col gap-3 overflow-y-auto sm:w-96">
                    {activeQuotas.map((quota) => (
                        <ActiveQuotaCard key={quota.name} name={quota.name} resetDate={quota.next_reset} used={quota.allocated} limit={quota.limit_value} type={quota.limit_name} />
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