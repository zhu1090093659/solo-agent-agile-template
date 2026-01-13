import { ChatWindow } from '../components/chat'

export default function HomePage() {
  return (
    <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-950">
      {/* Header */}
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">
            [AGENT_NAME]
          </h1>
          <span className="text-sm text-gray-500 dark:text-gray-400">
            Powered by Claude
          </span>
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-hidden">
        <div className="h-full max-w-4xl mx-auto">
          <ChatWindow
            title="[AGENT_NAME]"
            welcomeMessage="Hello! I'm [AGENT_NAME], your AI assistant. How can I help you today?"
          />
        </div>
      </main>
    </div>
  )
}
