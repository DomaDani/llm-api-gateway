import CreateKeyForm from "./components/CreateKeyForm"
import ApiKeysTable from "../../components/blocks/ApiKeysTable"

const PLACEHOLDER_KEYS = [
    {
        user: "GipszJakab",
        name: "test key",
        fingerprint: "asdfasdf",
        created_date: "2026-03-20",
        status: "Active"
    },
]

export default function ApiKeys() {
    return (
        <>
        <div className="flex flex-col gap-5">
            <div className="border-b border-white/10">
                <CreateKeyForm />
            </div>
            <div className="border-b border-white/10">
                <ApiKeysTable title="Your API Keys" rows={PLACEHOLDER_KEYS} onAction={() => { }} showUser={false} />
            </div>
        </div>
        </>
    )
}