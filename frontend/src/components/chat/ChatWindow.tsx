import React, { useRef, useEffect } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { useChat } from '../../hooks/useChat';

interface ChatWindowProps {
  title?: string;
  welcomeMessage?: string;
  apiUrl?: string;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  title = 'AI Assistant',
  welcomeMessage = 'Hello! How can I help you today?',
  apiUrl,
}) => {
  const { messages, isLoading, error, sendMessage, clearMessages } = useChat({
    apiUrl,
    onError: (err) => console.error('Chat error:', err),
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
          {title}
        </h2>
        <button
          onClick={clearMessages}
          className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          Clear
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-gray-500 dark:text-gray-400">
              <div className="text-4xl mb-4">💬</div>
              <p>{welcomeMessage}</p>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {/* Error display */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-3 rounded-lg mb-4">
            {error.message}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4">
        <ChatInput
          onSend={sendMessage}
          disabled={isLoading}
          placeholder={isLoading ? 'Thinking...' : 'Type a message...'}
        />
      </div>
    </div>
  );
};
