/**
 * Hook personalizado para Chat com Sistema de Memória Híbrida
 * Integração React com backend FastAPI + PostgreSQL + Weaviate
 */

import { useState, useEffect, useCallback, useRef } from 'react';

// Função para gerar UUID simples sem dependência externa
function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

// Tipos TypeScript para o sistema de memória
export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  sessionId?: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  timestamp: string;
  context_used: {
    type: string;
    recent_count: number;
    semantic_count: number;
    has_recent: boolean;
    has_semantic: boolean;
  };
  memory_stats: {
    postgresql: {
      total_messages: number;
      unique_sessions: number;
      last_message: string | null;
    };
    weaviate: {
      total_vectors: number;
      collection_name: string;
    };
    status: string;
  };
}

export interface MemoryStats {
  stats: ChatResponse['memory_stats'];
  status: string;
}

export interface ChatHookOptions {
  apiBaseUrl?: string;
  sessionId?: string;
  contextMode?: 'hybrid' | 'recent_only' | 'semantic_only' | 'none';
  autoGenerateSessionId?: boolean;
}

export interface ChatHookReturn {
  // Estados principais
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  sessionId: string;
  
  // Estatísticas de memória
  memoryStats: MemoryStats | null;
  contextInfo: ChatResponse['context_used'] | null;
  
  // Funções principais
  sendMessage: (message: string) => Promise<void>;
  clearMessages: () => void;
  refreshMemoryStats: () => Promise<void>;
  
  // Gestão de sessões
  startNewSession: () => void;
  loadSessionContext: (query?: string) => Promise<string>;
  
  // Configurações
  setContextMode: (mode: ChatHookOptions['contextMode']) => void;
  contextMode: ChatHookOptions['contextMode'];
}

const DEFAULT_API_BASE = 'http://localhost:8000';

export function useHybridMemoryChat(options: ChatHookOptions = {}): ChatHookReturn {
  const {
    apiBaseUrl = DEFAULT_API_BASE,
    sessionId: initialSessionId,
    contextMode: initialContextMode = 'hybrid',
    autoGenerateSessionId = true
  } = options;

  // Estados principais
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string>(
    initialSessionId || (autoGenerateSessionId ? generateUUID() : '')
  );
  const [contextMode, setContextMode] = useState<ChatHookOptions['contextMode']>(initialContextMode);
  
  // Estados de memória
  const [memoryStats, setMemoryStats] = useState<MemoryStats | null>(null);
  const [contextInfo, setContextInfo] = useState<ChatResponse['context_used'] | null>(null);
  
  // Refs para evitar re-renders desnecessários
  const abortControllerRef = useRef<AbortController | null>(null);

  // Função para fazer requests ao backend
  const makeApiRequest = useCallback(async <T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> => {
    const url = `${apiBaseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(
        errorData?.detail || `HTTP ${response.status}: ${response.statusText}`
      );
    }

    return response.json();
  }, [apiBaseUrl]);

  // Função principal para enviar mensagens
  const sendMessage = useCallback(async (messageText: string) => {
    if (!messageText.trim() || isLoading) return;

    // Cancelar request anterior se existir
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Criar novo abort controller
    const controller = new AbortController();
    abortControllerRef.current = controller;

    setIsLoading(true);
    setError(null);

    // Adicionar mensagem do utilizador imediatamente
    const userMessage: Message = {
      id: generateUUID(),
      text: messageText,
      sender: 'user',
      timestamp: new Date(),
      sessionId,
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      // Fazer request para o backend
      const response = await makeApiRequest<ChatResponse>('/api/message', {
        method: 'POST',
        signal: controller.signal,
        body: JSON.stringify({
          message: messageText,
          session_id: sessionId,
          context_mode: contextMode,
        }),
      });

      // Atualizar session ID se foi gerado pelo backend
      if (response.session_id && response.session_id !== sessionId) {
        setSessionId(response.session_id);
      }

      // Adicionar resposta do assistente
      const assistantMessage: Message = {
        id: generateUUID(),
        text: response.response,
        sender: 'assistant',
        timestamp: new Date(response.timestamp),
        sessionId: response.session_id,
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Atualizar informações de contexto e memória
      setContextInfo(response.context_used);
      if (response.memory_stats) {
        setMemoryStats({
          stats: response.memory_stats,
          status: 'success'
        });
      }

    } catch (error: any) {
      if (error.name === 'AbortError') {
        return; // Request foi cancelado, não mostrar erro
      }

      const errorMessage = error.message || 'Erro inesperado ao enviar mensagem';
      setError(errorMessage);

      // Adicionar mensagem de erro
      const errorMsg: Message = {
        id: generateUUID(),
        text: `❌ ${errorMessage}. Podes tentar novamente?`,
        sender: 'assistant',
        timestamp: new Date(),
        sessionId,
      };

      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  }, [sessionId, contextMode, isLoading, makeApiRequest]);

  // Função para obter estatísticas de memória
  const refreshMemoryStats = useCallback(async () => {
    try {
      const stats = await makeApiRequest<MemoryStats>('/api/memory/stats');
      setMemoryStats(stats);
    } catch (error: any) {
      console.error('Erro ao obter estatísticas de memória:', error);
      setError('Erro ao carregar estatísticas de memória');
    }
  }, [makeApiRequest]);

  // Função para carregar contexto de uma sessão
  const loadSessionContext = useCallback(async (query: string = 'conversa geral'): Promise<string> => {
    try {
      const response = await makeApiRequest<{
        session_id: string;
        query: string;
        context: string;
        context_analysis: ChatResponse['context_used'];
      }>(`/api/sessions/${sessionId}/context?query=${encodeURIComponent(query)}`);
      
      setContextInfo(response.context_analysis);
      return response.context;
    } catch (error: any) {
      console.error('Erro ao carregar contexto:', error);
      throw error;
    }
  }, [sessionId, makeApiRequest]);

  // Função para iniciar nova sessão
  const startNewSession = useCallback(() => {
    // Cancelar request ativo
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Reset estados
    const newSessionId = generateUUID();
    setSessionId(newSessionId);
    setMessages([]);
    setError(null);
    setContextInfo(null);
    setIsLoading(false);
  }, []);

  // Função para limpar mensagens
  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  // Carregar estatísticas iniciais
  useEffect(() => {
    refreshMemoryStats();
  }, [refreshMemoryStats]);

  // Cleanup no desmonte
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  return {
    // Estados principais
    messages,
    isLoading,
    error,
    sessionId,
    
    // Estados de memória
    memoryStats,
    contextInfo,
    
    // Funções principais
    sendMessage,
    clearMessages,
    refreshMemoryStats,
    
    // Gestão de sessões
    startNewSession,
    loadSessionContext,
    
    // Configurações
    setContextMode,
    contextMode,
  };
}
