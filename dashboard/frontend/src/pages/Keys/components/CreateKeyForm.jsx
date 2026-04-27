import { useState } from "react"

import { useAuth } from "../../../api/auth/AuthProvider"
import { useProject } from "../../../components/shared/ProjectContext"
import AlertBox from "../../../components/primitives/AlertBox"
import InfoBox from "../../../components/primitives/InfoBox"
import useApiKeyCreation from "../../../hooks/useApiKeyCreation"

/**
 * Form for creating a new API key for the selected project.
 *
 * @param {object} props - Component props.
 * @param {Function} props.onCreated - Callback fired when an API key is successfully created.
 * @returns {JSX.Element} The rendered form.
 */
export default function CreateKeyForm({ onCreated }) {
    const { user } = useAuth()
    const { selectedProject } = useProject()
    const [keyName, setKeyName] = useState("")
    const {
        apiKeyCreateError,
        apiKeyCreateSuccess,
        apiKeyCreateLoading,
        createdApiKeyValue,
        handleCreateApiKey,
    } = useApiKeyCreation({
        projectId: selectedProject?.id ?? null,
        userId: user?.id ?? null,
    })

    const handleSubmit = async (event) => {
        event.preventDefault()

        const createdKey = await handleCreateApiKey({
            name: keyName,
        })

        if (createdKey) {
            setKeyName("")
            onCreated?.(createdKey)
        }
    }

    return (
        <>
            <form autoComplete="off" className="w-full max-w-md" onSubmit={handleSubmit}>
                <div className="space-y-12">
                    <div className="pb-5">
                        <h2 className="text-base/7 font-semibold text-white">Create New API Key</h2>
                        {/* <p className="mt-1 text-sm/6 text-gray-400">
                        </p> */}
                        <div className="mt-3 space-y-6">
                            <AlertBox message={apiKeyCreateError} variant="error" className="mt-0" />
                            <AlertBox message={apiKeyCreateSuccess} variant="success" className="mt-0" />
                        </div>
                        <div className="mt-3 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                            <InfoBox value={createdApiKeyValue} className="sm:col-span-10" />
                            <div className="sm:col-span-4">
                                <label htmlFor="key-name" className="block text-sm/6 font-medium text-white">
                                    Key Name
                                </label>
                                <div className="mt-2">
                                    <input
                                        id="key-name"
                                        name="key-name"
                                        type="text"
                                        placeholder="Key Name"
                                        autoComplete="off"
                                        value={keyName}
                                        onChange={(event) => setKeyName(event.target.value)}
                                        required
                                        className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
                                    />
                                </div>
                            </div>
                        </div>
                        <div className="pt-6">
                            <button
                                type="submit"
                                disabled={apiKeyCreateLoading}
                                className={`rounded-md px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 ${apiKeyCreateLoading ? 'cursor-not-allowed bg-indigo-400' : 'cursor-pointer bg-indigo-500 hover:bg-indigo-400'}`}
                            >
                                {apiKeyCreateLoading ? "Creating key..." : "Submit"}
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </>
    )
}