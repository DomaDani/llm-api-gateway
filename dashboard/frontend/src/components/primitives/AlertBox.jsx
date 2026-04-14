const STYLES = {
    error: 'border-red-500/50 bg-red-500/10 text-red-300',
    success: 'border-emerald-500/50 bg-emerald-500/10 text-emerald-300',
    warning: 'border-yellow-400/50 bg-yellow-400/10 text-yellow-300'
}

export default function AlertBox({ message, variant = 'error', className = '' }) {
    if (!message) {
        return null
    }

    const variantClasses = STYLES[variant] || STYLES.error

    return (
        <div className={`max-w-sm mt-3 rounded border p-2 text-sm break-words ${variantClasses} ${className}`.trim()}>
            {message}
        </div>
    )
}