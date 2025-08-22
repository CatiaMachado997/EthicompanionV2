/**
 * Componente de Estatísticas de Memória Híbrida
 * Mostra estado do PostgreSQL, Weaviate e contexto usado
 */

import React, { useState } from 'react';
import { ChatResponse } from '../hooks/useHybridMemoryChat';

interface MemoryStatsProps {
  memoryStats: {
    stats: ChatResponse['memory_stats'];
    status: string;
  } | null;
  contextInfo: ChatResponse['context_used'] | null;
  onRefresh: () => Promise<void>;
  className?: string;
}

export function MemoryStatsPanel({ 
  memoryStats, 
  contextInfo, 
  onRefresh, 
  className = '' 
}: MemoryStatsProps) {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await onRefresh();
    } finally {
      setIsRefreshing(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational': return 'text-green-600';
      case 'degraded': return 'text-yellow-600';
      case 'error': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getContextTypeIcon = (type: string) => {
    switch (type) {
      case 'hybrid': return '🧠';
      case 'recent_only': return '📚';
      case 'semantic_only': return '🔍';
      case 'none': return '💭';
      default: return '❓';
    }
  };

  const getContextTypeLabel = (type: string) => {
    switch (type) {
      case 'hybrid': return 'Híbrida (Recente + Semântica)';
      case 'recent_only': return 'Apenas Histórico Recente';
      case 'semantic_only': return 'Apenas Pesquisa Semântica';
      case 'none': return 'Sem Contexto';
      default: return 'Desconhecido';
    }
  };

  if (!memoryStats) {
    return (
      <div className={`bg-gray-50 border border-gray-200 rounded-lg p-4 ${className}`}>
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium text-gray-700">Estado da Memória</h3>
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 disabled:opacity-50"
          >
            {isRefreshing ? '🔄' : '↻'} Atualizar
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">A carregar estatísticas...</p>
      </div>
    );
  }

  return (
    <div className={`bg-white border border-gray-200 rounded-lg shadow-sm ${className}`}>
      {/* Header */}
      <div className="p-3 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-medium text-gray-800">Sistema de Memória</h3>
            <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(memoryStats.stats.status)} bg-opacity-10`}>
              {memoryStats.stats.status === 'operational' ? '✅' : '⚠️'} {memoryStats.stats.status}
            </span>
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-xs px-2 py-1 text-gray-600 hover:bg-gray-100 rounded"
              title={isExpanded ? 'Minimizar' : 'Expandir'}
            >
              {isExpanded ? '📖' : '📋'}
            </button>
            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="text-xs px-2 py-1 bg-blue-50 text-blue-700 rounded hover:bg-blue-100 disabled:opacity-50"
              title="Atualizar estatísticas"
            >
              {isRefreshing ? '🔄' : '↻'}
            </button>
          </div>
        </div>
      </div>

      {/* Estatísticas Compactas */}
      <div className="p-3">
        <div className="grid grid-cols-2 gap-3 text-xs">
          {/* PostgreSQL */}
          <div className="bg-blue-50 rounded p-2">
            <div className="flex items-center gap-1 mb-1">
              <span>💾</span>
              <span className="font-medium text-blue-800">PostgreSQL</span>
            </div>
            <div className="text-blue-700">
              <div>{memoryStats.stats.postgresql.total_messages || 0} mensagens</div>
              <div>{memoryStats.stats.postgresql.unique_sessions || 0} sessões</div>
            </div>
          </div>

          {/* Weaviate */}
          <div className="bg-purple-50 rounded p-2">
            <div className="flex items-center gap-1 mb-1">
              <span>🔍</span>
              <span className="font-medium text-purple-800">Weaviate</span>
            </div>
            <div className="text-purple-700">
              <div>{memoryStats.stats.weaviate.total_vectors || 0} vetores</div>
              <div className="truncate">{memoryStats.stats.weaviate.collection_name}</div>
            </div>
          </div>
        </div>

        {/* Contexto Atual */}
        {contextInfo && (
          <div className="mt-3 bg-green-50 rounded p-2">
            <div className="flex items-center gap-1 mb-1">
              <span>{getContextTypeIcon(contextInfo.type)}</span>
              <span className="font-medium text-green-800 text-xs">Último Contexto</span>
            </div>
            <div className="text-xs text-green-700">
              <div className="font-medium">{getContextTypeLabel(contextInfo.type)}</div>
              <div className="flex gap-3 mt-1">
                <span>📚 {contextInfo.recent_count} recentes</span>
                <span>🧠 {contextInfo.semantic_count} semânticas</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Detalhes Expandidos */}
      {isExpanded && (
        <div className="border-t border-gray-100 p-3 bg-gray-50">
          <h4 className="text-xs font-medium text-gray-700 mb-2">Detalhes Técnicos</h4>
          
          <div className="space-y-2 text-xs">
            {/* PostgreSQL Detalhado */}
            <div>
              <div className="font-medium text-gray-700">Base de Dados Episódica:</div>
              <div className="ml-2 text-gray-600">
                <div>• Total de mensagens: {memoryStats.stats.postgresql.total_messages}</div>
                <div>• Sessões únicas: {memoryStats.stats.postgresql.unique_sessions}</div>
                <div>• Última mensagem: {
                  memoryStats.stats.postgresql.last_message 
                    ? new Date(memoryStats.stats.postgresql.last_message).toLocaleString('pt-PT')
                    : 'Nunca'
                }</div>
              </div>
            </div>

            {/* Weaviate Detalhado */}
            <div>
              <div className="font-medium text-gray-700">Base de Dados Semântica:</div>
              <div className="ml-2 text-gray-600">
                <div>• Vetores armazenados: {memoryStats.stats.weaviate.total_vectors}</div>
                <div>• Coleção: {memoryStats.stats.weaviate.collection_name}</div>
                <div>• Estado: Operacional</div>
              </div>
            </div>

            {/* Contexto Detalhado */}
            {contextInfo && (
              <div>
                <div className="font-medium text-gray-700">Último Contexto Usado:</div>
                <div className="ml-2 text-gray-600">
                  <div>• Tipo: {getContextTypeLabel(contextInfo.type)}</div>
                  <div>• Histórico recente: {contextInfo.has_recent ? 'Sim' : 'Não'} ({contextInfo.recent_count} msgs)</div>
                  <div>• Memórias semânticas: {contextInfo.has_semantic ? 'Sim' : 'Não'} ({contextInfo.semantic_count} matches)</div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Componente compacto para mostrar apenas o status
 */
export function MemoryStatusBadge({ 
  memoryStats, 
  contextInfo 
}: Pick<MemoryStatsProps, 'memoryStats' | 'contextInfo'>) {
  if (!memoryStats) {
    return (
      <div className="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
        <span>🧠</span>
        <span>Carregando...</span>
      </div>
    );
  }

  const isOperational = memoryStats.stats.status === 'operational';
  const totalMessages = memoryStats.stats.postgresql?.total_messages || 0;
  const totalVectors = memoryStats.stats.weaviate?.total_vectors || 0;

  return (
    <div className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs ${
      isOperational 
        ? 'bg-green-100 text-green-700' 
        : 'bg-yellow-100 text-yellow-700'
    }`}>
      <span>{isOperational ? '✅' : '⚠️'}</span>
      <span>{totalMessages + totalVectors} memórias</span>
      {contextInfo && (
        <span title={`Contexto: ${contextInfo.type}`}>
          {contextInfo.type === 'hybrid' ? '🧠' : 
           contextInfo.type === 'recent_only' ? '📚' : 
           contextInfo.type === 'semantic_only' ? '🔍' : '💭'}
        </span>
      )}
    </div>
  );
}
