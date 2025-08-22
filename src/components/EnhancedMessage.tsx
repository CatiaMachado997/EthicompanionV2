/**
 * Componente de Mensagem Melhorado com Informações de Contexto
 * Mostra mensagens do chat com detalhes sobre memória usada
 */

import React, { useState } from 'react';
import { Message, ChatResponse } from '../hooks/useHybridMemoryChat';

interface EnhancedMessageProps {
  message: Message;
  contextInfo?: ChatResponse['context_used'] | null;
  isLastMessage?: boolean;
  showContextDetails?: boolean;
}

export function EnhancedMessage({ 
  message, 
  contextInfo, 
  isLastMessage = false,
  showContextDetails = false 
}: EnhancedMessageProps) {
  const [showDetails, setShowDetails] = useState(false);
  const isUser = message.sender === 'user';
  const isAssistant = message.sender === 'assistant';

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('pt-PT', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getContextBadge = (contextInfo: ChatResponse['context_used']) => {
    const { type, recent_count, semantic_count } = contextInfo;
    
    switch (type) {
      case 'hybrid':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs">
            🧠 Híbrida ({recent_count}+{semantic_count})
          </span>
        );
      case 'recent_only':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">
            📚 Recente ({recent_count})
          </span>
        );
      case 'semantic_only':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-100 text-green-700 rounded text-xs">
            🔍 Semântica ({semantic_count})
          </span>
        );
      case 'none':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
            💭 Sem contexto
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[85%] ${isUser ? 'order-2' : 'order-1'}`}>
        {/* Avatar/Indicador */}
        <div className={`flex items-end gap-2 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
          <div className={`
            w-8 h-8 rounded-full flex items-center justify-center text-sm
            ${isUser 
              ? 'bg-blue-500 text-white' 
              : 'bg-gray-200 text-gray-600'
            }
          `}>
            {isUser ? '👤' : '🤖'}
          </div>

          {/* Mensagem Principal */}
          <div className={`
            relative max-w-full rounded-2xl px-4 py-3 shadow-sm
            ${isUser 
              ? 'bg-blue-500 text-white' 
              : 'bg-white border border-gray-200 text-gray-800'
            }
          `}>
            {/* Texto da mensagem */}
            <div className="text-sm leading-relaxed whitespace-pre-wrap">
              {message.text}
            </div>

            {/* Metadados */}
            <div className={`
              flex items-center gap-2 mt-2 text-xs
              ${isUser ? 'text-blue-100' : 'text-gray-500'}
            `}>
              <span>{formatTime(message.timestamp)}</span>
              
              {/* Badge de contexto para mensagens do assistente */}
              {isAssistant && contextInfo && isLastMessage && (
                <>
                  <span>•</span>
                  {getContextBadge(contextInfo)}
                </>
              )}

              {/* Botão de detalhes para mensagens do assistente */}
              {isAssistant && contextInfo && isLastMessage && showContextDetails && (
                <>
                  <span>•</span>
                  <button
                    onClick={() => setShowDetails(!showDetails)}
                    className="hover:underline focus:outline-none"
                  >
                    {showDetails ? 'Ocultar' : 'Detalhes'}
                  </button>
                </>
              )}
            </div>

            {/* Detalhes expandidos do contexto */}
            {showDetails && contextInfo && isAssistant && (
              <div className="mt-3 pt-3 border-t border-gray-100">
                <ContextDetails contextInfo={contextInfo} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * Componente para mostrar detalhes do contexto usado
 */
function ContextDetails({ contextInfo }: { contextInfo: ChatResponse['context_used'] }) {
  const { type, recent_count, semantic_count, has_recent, has_semantic } = contextInfo;

  return (
    <div className="bg-gray-50 rounded-lg p-3 text-xs">
      <div className="font-medium text-gray-700 mb-2">
        Contexto Usado nesta Resposta:
      </div>
      
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-gray-600">Tipo de memória:</span>
          <span className="font-medium">
            {type === 'hybrid' ? '🧠 Híbrida' :
             type === 'recent_only' ? '📚 Recente' :
             type === 'semantic_only' ? '🔍 Semântica' :
             '💭 Sem contexto'}
          </span>
        </div>

        {has_recent && (
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Mensagens recentes:</span>
            <span className="font-medium">{recent_count}</span>
          </div>
        )}

        {has_semantic && (
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Memórias relevantes:</span>
            <span className="font-medium">{semantic_count}</span>
          </div>
        )}

        <div className="pt-2 border-t border-gray-200">
          <div className="text-gray-500">
            {type === 'hybrid' 
              ? 'Esta resposta foi informada tanto pelo histórico recente desta conversa quanto por memórias relevantes de conversas anteriores.'
              : type === 'recent_only'
              ? 'Esta resposta foi baseada apenas no histórico recente desta conversa.'
              : type === 'semantic_only'
              ? 'Esta resposta foi informada por memórias relevantes de conversas anteriores.'
              : 'Esta resposta foi gerada sem contexto de conversas anteriores.'
            }
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * Componente de lista de mensagens
 */
interface MessageListProps {
  messages: Message[];
  lastContextInfo?: ChatResponse['context_used'] | null;
  showContextDetails?: boolean;
  className?: string;
}

export function MessageList({ 
  messages, 
  lastContextInfo, 
  showContextDetails = false,
  className = '' 
}: MessageListProps) {
  return (
    <div className={`space-y-1 ${className}`}>
      {messages.map((message, index) => {
        const isLastAssistantMessage = 
          message.sender === 'assistant' && 
          index === messages.length - 1;
          
        return (
          <EnhancedMessage
            key={message.id}
            message={message}
            contextInfo={isLastAssistantMessage ? lastContextInfo : null}
            isLastMessage={isLastAssistantMessage}
            showContextDetails={showContextDetails}
          />
        );
      })}
    </div>
  );
}

/**
 * Indicador de digitação melhorado
 */
export function TypingIndicator({ 
  contextMode = 'hybrid' 
}: { 
  contextMode?: 'hybrid' | 'recent_only' | 'semantic_only' | 'none' 
}) {
  const getContextIcon = (mode: string) => {
    switch (mode) {
      case 'hybrid': return '🧠';
      case 'recent_only': return '📚';
      case 'semantic_only': return '🔍';
      case 'none': return '💭';
      default: return '🤖';
    }
  };

  const getContextLabel = (mode: string) => {
    switch (mode) {
      case 'hybrid': return 'analisando memórias...';
      case 'recent_only': return 'revisando conversa...';
      case 'semantic_only': return 'pesquisando memórias...';
      case 'none': return 'pensando...';
      default: return 'processando...';
    }
  };

  return (
    <div className="flex justify-start mb-4">
      <div className="flex items-end gap-2">
        <div className="w-8 h-8 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center text-sm">
          🤖
        </div>
        <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm">
          <div className="flex items-center gap-2">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
            <span className="text-xs text-gray-500 ml-2">
              {getContextIcon(contextMode)} {getContextLabel(contextMode)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
