import ActiveQuotasTable from "./components/ActiveQuotasTable"
import UsageRecordsTable from "./components/UsageRecordsTable"
import { useEffect, useState } from "react"
import { useAuth } from "../../api/auth/AuthProvider"
import { useProject } from "../../components/shared/ProjectContext"
import { fetchQuotaInfos } from "../../api/management/quotas/Info"

/**
 * Usage page for viewing active quotas and usage records across different scopes.
 *
 * @returns {JSX.Element} The rendered usage page.
 */
export default function Usage() {
    const { selectedProject } = useProject()
    const { user } = useAuth()
    const [activeQuotas, setActiveQuotas] = useState([])
    
    useEffect(() => {
        let mounted = true

        if (!selectedProject) {
            setActiveQuotas([])
            return
        }

        fetchQuotaInfos(null, user?.id, null, true, true)
        .then((data) => {
            if (!mounted) return
            setActiveQuotas(data)
        })
        .catch((err) => {
            console.error("Failed to load quota infos:", err)
        })


        return () => { mounted = false }
    }, [selectedProject, user])

    return (
        <div className="flex flex-col gap-5">
            <h1 className="shrink-0 text-3xl font-bold text-white">Usage</h1>
            <div className="border-b border-white/10 pb-5">
                <ActiveQuotasTable title="Active Quotas" rows={activeQuotas} />
            </div>
            <div className="border-b border-white/10 pb-5">
                <UsageRecordsTable title="Global Usage" showProject={true} showUser={true} />
            </div>
            <div className="border-b border-white/10 pb-5">
                <UsageRecordsTable title="Project Usage" projectId={selectedProject?.id} showUser={true} enabled={Boolean(selectedProject?.id)} />
            </div>
            <div className="border-b border-white/10 pb-5">
                <UsageRecordsTable title="Personal Usage" projectId={selectedProject?.id} userId={user?.id} enabled={Boolean(selectedProject?.id && user?.id)} />
            </div>
        </div>
    )
}