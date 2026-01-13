import React from 'react';
import type { ChatMessage as ChatMessageType } from '../../hooks/useChat';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
        }`}
      >
        {/* Message Content */}
        <div className="whitespace-pre-wrap break-words">
          {message.content || (
            <span className="inline-flex items-center">
              <LoadingDots />
            </span>
          )}
        </div>

        {/* Tool Use Display */}
        {message.toolUse && message.toolUse.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
            {message.toolUse.map((tool, index) => (
              <div key={index} className="text-sm opacity-80">
                <div className="flex items-center gap-1">
                  <span className="font-mono text-xs bg-gray-200 dark:bg-gray-700 px-1 rounded">
                    {tool.tool}
                  </span>
                  {tool.output ? (
                    <span className="text-green-600 dark:text-green-400">✓</span>
                  ) : (
                    <LoadingDots small />
                  )}
                </div>
                {tool.output && (
                  <pre className="mt-1 text-xs overflow-x-auto bg-gray-50 dark:bg-gray-900 p-2 rounded">
                    {typeof tool.output === 'string'
                      ? tool.output.slice(0, 200)
                      : JSON.stringify(tool.output, null, 2).slice(0, 200)}
                    {(tool.output?.length || 0) > 200 && '...'}
                  </pre>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Timestamp */}
        <div
          className={`text-xs mt-1 ${
            isUser ? 'text-blue-200' : 'text-gray-400'
          }`}
        >
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

const LoadingDots: React.FC<{ small?: boolean }> = ({ small }) => (
  <span className={`inline-flex gap-1 ${small ? 'scale-75' : ''}`}>
    <span className="animate-bounce" style={{ animationDelay: '0ms' }}>
      •
    </span>
    <span className="animate-bounce" style={{ animationDelay: '150ms' }}>
      •
    </span>
    <span className="animate-bounce" style={{ animationDelay: '300ms' }}>
      •
    </span>
  </span>
);
