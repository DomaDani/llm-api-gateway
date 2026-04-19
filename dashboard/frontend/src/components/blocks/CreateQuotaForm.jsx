import { useState, useEffect } from "react"
import Dropdown from "../primitives/Dropdown"
import { fetchQuotaLimitTypes, fetchQuotaPeriods } from "../../api/management/quotas/Info"
import { fetchUserInfos } from "../../api/management/user/Info"
import { fetchKeyInfos } from "../../api/management/keys/Info"
import { useProject } from "../shared/ProjectContext"

/**
 * Form for creating a new quota with limit type, period, value, and optional targeting.
 *
 * @param {object} props - Component props.
 * @param {string} props.title - Form title.
 * @param {boolean} props.enableKeyTarget - Whether to allow targeting by API key.
 * @param {Function} props.onSubmit - Callback fired with form data on submission.
 * @param {boolean} props.isGlobal - Whether the quota is global or project-specific.
 * @returns {JSX.Element} The rendered form component.
 */
export default function CreateQuotaForm({
    title,
    enableKeyTarget = false,
    onSubmit,
    isGlobal = false
}) {
    const [value, setValue] = useState("")
    const [type, setType] = useState(null)
    const [refreshFrequency, setRefreshFrequency] = useState(null)
    const [expiration, setExpiration] = useState("")
    const [isPermanent, setIsPermanent] = useState(false)
    const [isTargetedQuota, setIsTargetedQuota] = useState(false)
    const [targetType, setTargetType] = useState("user")
    const [limitTypeOptions, setLimitTypeOptions] = useState([])
    const [limitTypeMap, setLimitTypeMap] = useState({})
    const [periodOptions, setPeriodOptions] = useState([])
    const [periodMap, setPeriodMap] = useState({})
    const [availableUsers, setAvailableUsers] = useState([])
    const [userMap, setUserMap] = useState({})
    const [user, setUser] = useState(null)
    const [project, setProject] = useState(null)
    const [key, setKey] = useState(null)
    const [targetKeyOptions, setTargetKeyOptions] = useState([])
    const [keyMap, setKeyMap] = useState({})
    const { selectedProject } = useProject()

    function handleSubmit(event) {
        event.preventDefault()
        onSubmit?.({
            value,
            limit_id: type,
            period: refreshFrequency,
            expiration,
            isPermanent,
            user_id: isTargetedQuota && targetType === "user" ? user : null,
            key_id: isTargetedQuota && targetType === "key" ? key : null,
        })
    }

    useEffect(() => {
        let mounted = true

        fetchQuotaLimitTypes()
            .then((data) => {
                if (!mounted) return
                if (Array.isArray(data) && data.length > 0) {
                    const names = data.map((d) => d.name)
                    const map = data.reduce((acc, d) => { acc[d.name] = d.id; return acc }, {})
                    setLimitTypeOptions(names)
                    setLimitTypeMap(map)
                }
            })
            .catch((err) => console.error("Failed to load limit types:", err))

        fetchQuotaPeriods()
            .then((data) => {
                if (!mounted) return
                if (Array.isArray(data) && data.length > 0) {
                    const names = data.map((d) => d.name)
                    const map = data.reduce((acc, d) => { acc[d.name] = d.name.toLowerCase(); return acc }, {})
                    setPeriodOptions(names)
                    setPeriodMap(map)
                }
            })
            .catch((err) => console.error("Failed to load periods:", err))

        fetchUserInfos(isGlobal ? null : selectedProject?.id)
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
            .catch((err) => console.error("Failed to load users:", err))

        if (isGlobal || !selectedProject?.id) {
            setTargetKeyOptions([])
            setKeyMap({})
        } else {
            fetchKeyInfos(selectedProject.id, null)
                .then((data) => {
                    if (!mounted) return

                    if (Array.isArray(data) && data.length > 0) {
                        const selectedProjectId = Number(selectedProject.id)
                        const filteredKeys = data.filter((keyInfo) => Number(keyInfo.project_id) === selectedProjectId)
                        const labels = filteredKeys.map((keyInfo) => {
                            const owner = keyInfo.username ? `${keyInfo.username}: ` : ""
                            return `${owner}${keyInfo.name} (${keyInfo.fingerprint})`
                        })
                        const map = filteredKeys.reduce((acc, keyInfo) => {
                            const owner = keyInfo.username ? `${keyInfo.username}: ` : ""
                            const label = `${owner}${keyInfo.name} (${keyInfo.fingerprint})`
                            acc[label] = keyInfo.id
                            return acc
                        }, {})

                        setTargetKeyOptions(labels)
                        setKeyMap(map)
                    } else {
                        setTargetKeyOptions([])
                        setKeyMap({})
                    }
                })
                .catch((err) => {
                    console.error("Failed to load keys:", err)
                    setTargetKeyOptions([])
                    setKeyMap({})
                })
        }

        return () => { mounted = false }
    }, [isGlobal, selectedProject])

    return (
        <form autoComplete="off" className="w-full max-w-md" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">{title}</h2>
                    <div className="mt-3 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                        
                        <div className="sm:col-span-4">
                            <label className="block text-sm/6 font-medium text-white">
                                Type
                            </label>
                            <div className="mt-2">
                                <Dropdown
                                    items={limitTypeOptions}
                                    itemName="type"
                                    onSelect={(name) => setType(limitTypeMap[name] ?? null)}
                                    required
                                    name="quota-type"
                                />
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <label className="block text-sm/6 font-medium text-white">
                                Refresh frequency
                            </label>
                            <div className="mt-2">
                                <Dropdown
                                    items={periodOptions}
                                    itemName="refresh frequency"
                                    onSelect={(name) => setRefreshFrequency(periodMap[name] ?? null)}
                                    required
                                    name="refresh-frequency"
                                />
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <label htmlFor="quota-value" className="block text-sm/6 font-medium text-white">
                                Quota value
                            </label>
                            <div className="mt-2">
                                <input
                                    id="quota-value"
                                    name="quota-value"
                                    type="number"
                                    min="0"
                                    placeholder="Value"
                                    autoComplete="off"
                                    value={value}
                                    onChange={(event) => setValue(event.target.value)}
                                    required
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <label htmlFor="quota-expiration" className="block text-sm/6 font-medium text-white">
                                Expiration
                            </label>
                            <div className="mt-2">
                                <input
                                    id="quota-expiration"
                                    name="quota-expiration"
                                    type="date"
                                    value={expiration}
                                    disabled={isPermanent}
                                    onChange={(event) => setExpiration(event.target.value)}
                                    required={!isPermanent}
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 [color-scheme:dark] focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 disabled:cursor-not-allowed disabled:opacity-50 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <div className="flex gap-3">
                                <div className="flex h-6 shrink-0 items-center">
                                    <div className="group grid size-4 grid-cols-1">
                                        <input
                                            id="quota-permanent"
                                            name="quota-permanent"
                                            type="checkbox"
                                            checked={isPermanent}
                                            onChange={(event) => {
                                                const checked = event.target.checked
                                                setIsPermanent(checked)
                                                if (checked) {
                                                    setExpiration("")
                                                }
                                            }}
                                            className="col-start-1 row-start-1 appearance-none rounded-sm border border-white/10 bg-white/5 checked:border-indigo-500 checked:bg-indigo-500 indeterminate:border-indigo-500 indeterminate:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:border-white/5 disabled:bg-white/10 disabled:checked:bg-white/10 forced-colors:appearance-auto"
                                        />
                                        <svg
                                            fill="none"
                                            viewBox="0 0 14 14"
                                            className="pointer-events-none col-start-1 row-start-1 size-3.5 self-center justify-self-center stroke-white group-has-disabled:stroke-white/25"
                                        >
                                            <path
                                                d="M3 8L6 11L11 3.5"
                                                strokeWidth={2}
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                className="opacity-0 group-has-checked:opacity-100"
                                            />
                                            <path
                                                d="M3 7H11"
                                                strokeWidth={2}
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                className="opacity-0 group-has-indeterminate:opacity-100"
                                            />
                                        </svg>
                                    </div>
                                </div>
                                <div className="text-sm/6">
                                    <label htmlFor="quota-permanent" className="font-medium text-white">
                                        Permanent?
                                    </label>
                                    <p className="text-gray-400">
                                        This quota does not expire unless it is manually changed.
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <div className="flex gap-3">
                                <div className="flex h-6 shrink-0 items-center">
                                    <div className="group grid size-4 grid-cols-1">
                                        <input
                                            id="quota-targeted"
                                            name="quota-targeted"
                                            type="checkbox"
                                            checked={isTargetedQuota}
                                            onChange={(event) => {
                                                const checked = event.target.checked
                                                setIsTargetedQuota(checked)
                                                if (!checked) {
                                                    setUser(null)
                                                    setKey(null)
                                                }
                                            }}
                                            className="col-start-1 row-start-1 appearance-none rounded-sm border border-white/10 bg-white/5 checked:border-indigo-500 checked:bg-indigo-500 indeterminate:border-indigo-500 indeterminate:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:border-white/5 disabled:bg-white/10 disabled:checked:bg-white/10 forced-colors:appearance-auto"
                                        />
                                        <svg
                                            fill="none"
                                            viewBox="0 0 14 14"
                                            className="pointer-events-none col-start-1 row-start-1 size-3.5 self-center justify-self-center stroke-white group-has-disabled:stroke-white/25"
                                        >
                                            <path
                                                d="M3 8L6 11L11 3.5"
                                                strokeWidth={2}
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                className="opacity-0 group-has-checked:opacity-100"
                                            />
                                            <path
                                                d="M3 7H11"
                                                strokeWidth={2}
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                className="opacity-0 group-has-indeterminate:opacity-100"
                                            />
                                        </svg>
                                    </div>
                                </div>
                                <div className="text-sm/6">
                                    <label htmlFor="quota-targeted" className="font-medium text-white">
                                        Targeted quota
                                    </label>
                                    <p className="text-gray-400">
                                        Quotas to limit specific users or keys.
                                    </p>
                                </div>
                            </div>
                        </div>

                        {isTargetedQuota && (
                            <div className="sm:col-span-4">
                                <fieldset>
                                    <legend className="block text-sm/6 font-medium text-white">Target type</legend>
                                    <div className="mt-2 flex items-center gap-6">
                                        <label className="inline-flex items-center gap-2 text-sm text-gray-300">
                                            <input
                                                type="radio"
                                                name="target-type"
                                                value="user"
                                                checked={targetType === "user"}
                                                onChange={() => {
                                                    setTargetType("user")
                                                    setUser(null)
                                                    setKey(null)
                                                }}
                                                className="cursor-pointer"
                                            />
                                            User
                                        </label>
                                        {enableKeyTarget && (
                                            <label className="inline-flex items-center gap-2 text-sm text-gray-300">
                                                <input
                                                    type="radio"
                                                    name="target-type"
                                                    value="key"
                                                    checked={targetType === "key"}
                                                    onChange={() => {
                                                        setTargetType("key")
                                                        setUser(null)
                                                        setKey(null)
                                                    }}
                                                    className="cursor-pointer"
                                                />
                                                Key
                                            </label>
                                        )}
                                    </div>
                                </fieldset>

                                <div className="mt-4">
                                        <Dropdown
                                            items={targetType === "key" ? targetKeyOptions : availableUsers}
                                            itemName={targetType}
                                            onSelect={(name) => {
                                                if (targetType === "key") {
                                                    setKey(keyMap[name] ?? null)
                                                } else {
                                                    setUser(userMap[name] ?? null)
                                                }
                                            }}
                                            required
                                            name="target-value"
                                        />
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="pt-6">
                        <button
                            type="submit"
                            className="cursor-pointer rounded-md bg-indigo-500 px-3 py-2 text-sm font-semibold text-white transition-colors hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
                        >
                            Submit
                        </button>
                    </div>
                </div>
            </div>
        </form>
    )
}
