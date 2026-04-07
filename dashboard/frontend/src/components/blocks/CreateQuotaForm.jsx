import { useState } from "react"
import Dropdown from "../primitives/Dropdown"

const PLACEHOLDER_QUOTA_TYPES = [
    "Token quota",
    "Request quota",
    "Daily quota",
    "Monthly quota",
]

const PLACEHOLDER_REFRESH_FREQUENCIES = [
    "Hourly",
    "Daily",
    "Weekly",
    "Monthly",
]

const PLACEHOLDER_TARGET_USERS = [
    "User 1",
    "User 2",
    "User 3",
]

const PLACEHOLDER_TARGET_KEYS = [
    "Key 1",
    "Key 2",
    "Key 3",
]

export default function CreateQuotaForm({
    title,
    typeOptions = PLACEHOLDER_QUOTA_TYPES,
    refreshFrequencyOptions = PLACEHOLDER_REFRESH_FREQUENCIES,
    targetUserOptions = PLACEHOLDER_TARGET_USERS,
    targetKeyOptions = PLACEHOLDER_TARGET_KEYS,
    enableKeyTarget = false,
    onSubmit,
}) {
    const [value, setValue] = useState("")
    const [type, setType] = useState(null)
    const [refreshFrequency, setRefreshFrequency] = useState(null)
    const [expiration, setExpiration] = useState("")
    const [isPermanent, setIsPermanent] = useState(false)
    const [isTargetedQuota, setIsTargetedQuota] = useState(false)
    const [targetType, setTargetType] = useState("user")
    const [targetValue, setTargetValue] = useState(null)

    function handleSubmit(event) {
        event.preventDefault()
        onSubmit?.({
            value,
            type,
            refreshFrequency,
            expiration,
            isPermanent,
            isTargetedQuota,
            targetType: isTargetedQuota ? targetType : null,
            targetValue: isTargetedQuota ? targetValue : null,
        })
    }

    return (
        <form autoComplete="off" onSubmit={handleSubmit}>
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
                                    items={typeOptions}
                                    itemName="type"
                                    onSelect={setType}
                                />
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <label className="block text-sm/6 font-medium text-white">
                                Refresh frequency
                            </label>
                            <div className="mt-2">
                                <Dropdown
                                    items={refreshFrequencyOptions}
                                    itemName="refresh frequency"
                                    onSelect={setRefreshFrequency}
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
                                                    setTargetValue(null)
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
                                                    setTargetValue(null)
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
                                                        setTargetValue(null)
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
                                        items={targetType === "key" ? targetKeyOptions : targetUserOptions}
                                        itemName={targetType}
                                        onSelect={setTargetValue}
                                    />
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="sm:col-span-4 pt-6">
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
