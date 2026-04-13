import ActiveQuotasTable from "./components/ActiveQuotasTable"
import UsageRecordsTable from "./components/UsageRecordsTable"
import { useEffect, useState } from "react"
import { fetchUsageLogs } from "../../api/usageLogs/UsageLogs"
import { useAuth } from "../../api/auth/AuthProvider"
import { useProject } from "../../context/ProjectContext"
import { fetchQuotaInfos } from "../../api/management/quotas/Info"

export default function Usage() {
    const { selectedProject } = useProject()
    const { user } = useAuth()
    const [globalLogs, setGlobalLogs] = useState([])
    const [projectLogs, setProjectLogs] = useState([])
    const [personalLogs, setPersonalLogs] = useState([])
    const [activeQuotas, setActiveQuotas] = useState([])
    
    useEffect(() => {
        let mounted = true

        if (!selectedProject) {
            setGlobalLogs([])
            setProjectLogs([])
            setPersonalLogs([])
            setActiveQuotas([])
            return
        }

        fetchUsageLogs(null, null, true, 250)
        .then((data) => {
            if (!mounted) return
            setGlobalLogs(data)
        })
        .catch((err) => {
            console.error("Failed to load usage logs:", err)
        })
        fetchUsageLogs(selectedProject.id, null, true, 250)
        .then((data) => {
            if (!mounted) return
            setProjectLogs(data)
        })
        .catch((err) => {
            console.error("Failed to load usage logs:", err)
        })
        fetchUsageLogs(selectedProject.id, user.id, true, 250)
        .then((data) => {
            if (!mounted) return
            setPersonalLogs(data)
        })
        .catch((err) => {
            console.error("Failed to load usage logs:", err)
        })
        fetchQuotaInfos(null, user?.id)
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
                <UsageRecordsTable title="Global Usage" rows={globalLogs} showProject={true} showUser={true} />
            </div>
            <div className="border-b border-white/10 pb-5">
                <UsageRecordsTable title="Project Usage" rows={projectLogs} showUser={true} />
            </div>
            <div className="border-b border-white/10 pb-5">
                <UsageRecordsTable title="Personal Usage" rows={personalLogs} />
            </div>
        </div>
    )
}