import { useState, useCallback, useRef } from 'react';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolUse?: {
    tool: string;
    input: Record<string, unknown>;
    output?: string;
  }[];
}

interface UseChatOptions {
  apiUrl?: string;
  onError?: (error: Error) => void;
}

interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: Error | null;
  sessionId: string | null;
  sendMessage: (message: string) => Promise<void>;
  clearMessages: () => void;
  startNewSession: () => Promise<void>;
}

export function useChat(options: UseChatOptions = {}): UseChatReturn {
  const { apiUrl = '/api/chat', onError } = options;
  
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  
  const abortControllerRef = useRef<AbortController | null>(null);

  const startNewSession = useCallback(async () => {
    try {
      const response = await fetch(`${apiUrl}/sessions`, {
        method: 'POST',
      });
      const data = await response.json();
      setSessionId(data.session_id);
      setMessages([]);
      setError(null);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to start session');
      setError(error);
      onError?.(error);
    }
  }, [apiUrl, onError]);

  const sendMessage = useCallback(async (message: string) => {
    if (!message.trim() || isLoading) return;

    // Cancel any existing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    // Add user message
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    // Create placeholder for assistant message
    const assistantMessageId = `assistant-${Date.now()}`;
    const assistantMessage: ChatMessage = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      toolUse: [],
    };
    
    setMessages(prev => [...prev, assistantMessage]);

    try {
      const response = await fetch(`${apiUrl}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: sessionId,
        }),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Get session ID from response header
      const newSessionId = response.headers.get('X-Session-Id');
      if (newSessionId && !sessionId) {
        setSessionId(newSessionId);
      }

      // Read SSE stream
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('No response body');
      }

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              setMessages(prev => {
                const newMessages = [...prev];
                const lastMessage = newMessages[newMessages.length - 1];
                
                if (lastMessage.id === assistantMessageId) {
                  if (data.type === 'text') {
                    lastMessage.content += data.content;
                  } else if (data.type === 'tool_use') {
                    lastMessage.toolUse = [
                      ...(lastMessage.toolUse || []),
                      { tool: data.tool, input: data.input }
                    ];
                  } else if (data.type === 'tool_result') {
                    const toolUse = lastMessage.toolUse?.find(
                      t => t.tool === data.tool && !t.output
                    );
                    if (toolUse) {
                      toolUse.output = data.output;
                    }
                  } else if (data.type === 'error') {
                    lastMessage.content += `\n\n⚠️ Error: ${data.message}`;
                  }
                }
                
                return newMessages;
              });
            } catch (e) {
              // Ignore JSON parse errors for malformed events
            }
          }
        }
      }
    } catch (err) {
      if (err instanceof Error && err.name === 'AbortError') {
        // Request was cancelled, ignore
        return;
      }
      
      const error = err instanceof Error ? err : new Error('Failed to send message');
      setError(error);
      onError?.(error);
      
      // Update assistant message with error
      setMessages(prev => {
        const newMessages = [...prev];
        const lastMessage = newMessages[newMessages.length - 1];
        if (lastMessage.id === assistantMessageId) {
          lastMessage.content = `⚠️ Error: ${error.message}`;
        }
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  }, [apiUrl, sessionId, isLoading, onError]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sessionId,
    sendMessage,
    clearMessages,
    startNewSession,
  };
}
