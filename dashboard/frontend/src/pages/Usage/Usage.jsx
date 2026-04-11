import ActiveQuotasTable from "./components/ActiveQuotasTable"
import UsageRecordsTable from "./components/UsageRecordsTable"
import { useEffect, useState } from "react"
import { fetchUsageLogs } from "../../api/usageLogs/UsageLogs"
import { useAuth } from "../../api/auth/AuthProvider"
import { useProject } from "../../context/ProjectContext"

// --- Placeholder data (replace with API calls later) ---
const ACTIVE_QUOTAS = [
    {
        id: 1,
        name: "Monthly Token Quota",
        limit_type: "Tokens",
        limit_value: 10000,
        allocated: 6800,
        percentage: 68,
        reset_date: "May 1, 2026",
    },
    {
        id: 2,
        name: "Daily Request Quota",
        limit_type: "Requests",
        limit_value: 100,
        allocated: 45,
        percentage: 45,
        reset_date: "Apr 8, 2026",
    },
    {
        id: 3,
        name: "Hourly Rate Limit",
        limit_type: "Requests/Hour",
        limit_value: 1000,
        allocated: 892,
        percentage: 89,
        reset_date: "Apr 7, 2026 22:00",
    },
    {
        id: 4,
        name: "Concurrent Requests",
        limit_type: "Connections",
        limit_value: 50,
        allocated: 47,
        percentage: 94,
        reset_date: "Ongoing",
    },
]
// --------------------------------------------------------

export default function Usage() {
    const { selectedProject } = useProject()
    const { user } = useAuth()
    const [globalLogs, setGlobalLogs] = useState([])
    const [projectLogs, setProjectLogs] = useState([])
    const [personalLogs, setPersonalLogs] = useState([])
    
    useEffect(() => {
        let mounted = true

        if (!selectedProject) {
            setGlobalLogs([])
            setProjectLogs([])
            setPersonalLogs([])
            return
        }

        fetchUsageLogs(null, null, true, 250)
        .then((data) => {
            if (!mounted) return
            setGlobalLogs(data)
        })
        fetchUsageLogs(selectedProject.id, null, true, 250)
        .then((data) => {
            if (!mounted) return
            setProjectLogs(data)
        })
        fetchUsageLogs(selectedProject.id, user.id, true, 250)
        .then((data) => {
            if (!mounted) return
            setPersonalLogs(data)
        })

        return () => { mounted = false }
    }, [selectedProject, user])

    return (
        <div className="flex flex-col gap-5">
            <h1 className="shrink-0 text-3xl font-bold text-white">Usage</h1>
            <div className="border-b border-white/10 pb-5">
                <ActiveQuotasTable title="Active Quotas" rows={ACTIVE_QUOTAS} />
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