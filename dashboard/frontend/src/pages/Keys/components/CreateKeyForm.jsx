import { useState } from "react"

import { createApiKey } from "../../../api/management/keys/Create"
import { useAuth } from "../../../api/auth/AuthProvider"
import { useProject } from "../../../context/ProjectContext"
import AlertBox from "../../../components/primitives/AlertBox"
import InfoBox from "../../../components/primitives/InfoBox"

export default function CreateKeyForm({ onCreated }) {
    const { user } = useAuth()
    const { selectedProject } = useProject()
    const [keyName, setKeyName] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [success, setSuccess] = useState("")
    const [apiKeyValue, setApiKeyValue] = useState("")

    const handleSubmit = async (event) => {
        event.preventDefault()
        setError("")
        setSuccess("")

        if (!selectedProject?.id) {
            setError("Select a project before creating an API key.")
            return
        }

        if (!user?.id) {
            setError("You must be signed in to create API keys.")
            return
        }

        setLoading(true)

        try {
            const createdKey = await createApiKey({
                project_id: selectedProject.id,
                name: keyName,
            })

            setApiKeyValue(createdKey.api_key || "")
            setSuccess("API key created successfully.")
            setKeyName("")
            onCreated?.(createdKey)
        } catch (err) {
            setError(err.message || "Could not create API key. Please try again.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <>
            <form autoComplete="off" onSubmit={handleSubmit}>
                <div className="space-y-12">
                    <div className="pb-5">
                        <h2 className="text-base/7 font-semibold text-white">Create New API Key</h2>
                        {/* <p className="mt-1 text-sm/6 text-gray-400">
                        </p> */}
                        <div className="mt-3 space-y-6">
                            <AlertBox message={error} variant="error" className="mt-0" />
                            <AlertBox message={success} variant="success" className="mt-0" />
                        </div>
                        <div className="mt-3 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                            <InfoBox value={apiKeyValue} className="sm:col-span-4" />
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
                        <div className="sm:col-span-4 pt-6">
                            <button
                                type="submit"
                                disabled={loading}
                                className={`rounded-md px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 ${loading ? 'cursor-not-allowed bg-indigo-400' : 'cursor-pointer bg-indigo-500 hover:bg-indigo-400'}`}
                            >
                                {loading ? "Creating key..." : "Submit"}
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </>
    )
}