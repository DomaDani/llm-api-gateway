import ProfileIdentityForm from "./components/ProfileIdentityForm"
import ProfilePasswordForm from "./components/ProfilePasswordForm"

export default function Profile() {
    return (
        <div className="flex flex-col gap-8">
            <h1 className="shrink-0 text-3xl font-bold text-white">Profile</h1>
            <div className="border-b border-white/10 pb-5">
                <ProfileIdentityForm />
            </div>
            <div className="border-b border-white/10 pb-5">
                <ProfilePasswordForm />
            </div>
        </div>
    )
}