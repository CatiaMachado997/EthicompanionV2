/**
 * Componente de indicador "A Pensar" para streaming
 * Mostra animação de pontos enquanto o assistente processa
 */

import React from 'react';

interface ThinkingIndicatorProps {
  isVisible: boolean;
  message?: string;
}

export function ThinkingIndicator({ isVisible, message = "A pensar" }: ThinkingIndicatorProps) {
  if (!isVisible) return null;

  return (
    <div className="flex items-center space-x-2 text-gray-500 text-sm py-2">
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
      </div>
      <span className="italic">{message}...</span>
    </div>
  );
}

interface StreamingMessageProps {
  text: string;
  isStreaming: boolean;
  isComplete: boolean;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

export function StreamingMessage({ 
  text, 
  isStreaming, 
  isComplete, 
  sender, 
  timestamp 
}: StreamingMessageProps) {
  const isAssistant = sender === 'assistant';
  
  return (
    <div className={`flex ${isAssistant ? 'justify-start' : 'justify-end'} mb-4`}>
      <div
        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
          isAssistant
            ? 'bg-gray-100 text-gray-800'
            : 'bg-blue-500 text-white'
        } ${isStreaming ? 'animate-pulse' : ''}`}
      >
        <div className="text-sm">
          {text}
          {isStreaming && (
            <span className="inline-flex ml-1">
              <span className="animate-pulse">|</span>
            </span>
          )}
        </div>
        
        {isComplete && (
          <div className="text-xs opacity-70 mt-1">
            {timestamp.toLocaleTimeString([], { 
              hour: '2-digit', 
              minute: '2-digit' 
            })}
            {isStreaming && (
              <span className="ml-2 text-yellow-600">🔄 Streaming</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
