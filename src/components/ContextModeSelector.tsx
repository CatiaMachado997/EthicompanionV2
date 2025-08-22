/**
 * Componente para Seletor de Modo de Contexto
 * Permite escolher entre diferentes tipos de memória
 */

import React from 'react';

type ContextMode = 'hybrid' | 'recent_only' | 'semantic_only' | 'none';

interface ContextModeSelectorProps {
  currentMode: ContextMode;
  onChange: (mode: ContextMode) => void;
  disabled?: boolean;
  className?: string;
}

interface ContextModeOption {
  value: ContextMode;
  label: string;
  description: string;
  icon: string;
  color: string;
}

const contextModeOptions: ContextModeOption[] = [
  {
    value: 'hybrid',
    label: 'Memória Híbrida',
    description: 'Combina histórico recente com memórias relevantes',
    icon: '🧠',
    color: 'border-purple-200 bg-purple-50 text-purple-700'
  },
  {
    value: 'recent_only',
    label: 'Apenas Recente',
    description: 'Usa apenas o histórico desta conversa',
    icon: '📚',
    color: 'border-blue-200 bg-blue-50 text-blue-700'
  },
  {
    value: 'semantic_only',
    label: 'Apenas Semântica',
    description: 'Pesquisa memórias por relevância semântica',
    icon: '🔍',
    color: 'border-green-200 bg-green-50 text-green-700'
  },
  {
    value: 'none',
    label: 'Sem Memória',
    description: 'Conversa sem contexto de memórias anteriores',
    icon: '💭',
    color: 'border-gray-200 bg-gray-50 text-gray-700'
  }
];

export function ContextModeSelector({ 
  currentMode, 
  onChange, 
  disabled = false,
  className = '' 
}: ContextModeSelectorProps) {
  const currentOption = contextModeOptions.find(opt => opt.value === currentMode);

  return (
    <div className={`${className}`}>
      {/* Dropdown Compacto */}
      <div className="relative">
        <select
          value={currentMode}
          onChange={(e) => onChange(e.target.value as ContextMode)}
          disabled={disabled}
          className={`
            appearance-none w-full px-3 py-2 pr-8 text-sm
            border border-gray-300 rounded-lg
            bg-white text-gray-700
            focus:ring-2 focus:ring-purple-500 focus:border-purple-500
            disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed
            hover:border-gray-400 transition-colors
          `}
        >
          {contextModeOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.icon} {option.label}
            </option>
          ))}
        </select>
        
        {/* Seta do dropdown */}
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-400">
          <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
          </svg>
        </div>
      </div>

      {/* Descrição do modo atual */}
      {currentOption && (
        <div className="mt-2 text-xs text-gray-600">
          <div className="flex items-center gap-1">
            <span>{currentOption.icon}</span>
            <span className="font-medium">{currentOption.label}:</span>
          </div>
          <div className="mt-1 text-gray-500">
            {currentOption.description}
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Versão expandida com cards visuais
 */
interface ContextModeCardSelectorProps extends ContextModeSelectorProps {
  showDescriptions?: boolean;
}

export function ContextModeCardSelector({ 
  currentMode, 
  onChange, 
  disabled = false,
  showDescriptions = true,
  className = '' 
}: ContextModeCardSelectorProps) {
  return (
    <div className={`space-y-2 ${className}`}>
      <div className="text-sm font-medium text-gray-700 mb-3">
        Modo de Memória:
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {contextModeOptions.map((option) => {
          const isSelected = currentMode === option.value;
          
          return (
            <button
              key={option.value}
              onClick={() => !disabled && onChange(option.value)}
              disabled={disabled}
              className={`
                p-3 rounded-lg border-2 text-left transition-all
                ${isSelected 
                  ? option.color + ' border-opacity-100 shadow-sm' 
                  : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
                }
                ${disabled 
                  ? 'opacity-50 cursor-not-allowed' 
                  : 'cursor-pointer hover:shadow-sm'
                }
              `}
            >
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">{option.icon}</span>
                <span className="font-medium text-sm">{option.label}</span>
                {isSelected && (
                  <span className="ml-auto text-xs">✓</span>
                )}
              </div>
              
              {showDescriptions && (
                <div className="text-xs opacity-75">
                  {option.description}
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}

/**
 * Badge compacto que mostra o modo atual
 */
export function ContextModeBadge({ 
  mode, 
  onClick 
}: { 
  mode: ContextMode; 
  onClick?: () => void; 
}) {
  const option = contextModeOptions.find(opt => opt.value === mode);
  
  if (!option) return null;

  return (
    <button
      onClick={onClick}
      className={`
        inline-flex items-center gap-1 px-2 py-1 rounded text-xs
        ${option.color}
        ${onClick ? 'hover:opacity-80 cursor-pointer' : 'cursor-default'}
        transition-opacity
      `}
      title={option.description}
    >
      <span>{option.icon}</span>
      <span>{option.label}</span>
    </button>
  );
}

/**
 * Tooltip explicativo sobre os modos de contexto
 */
export function ContextModeTooltip() {
  return (
    <div className="text-xs bg-gray-900 text-white p-3 rounded-lg shadow-lg max-w-xs">
      <div className="font-medium mb-2">Modos de Memória:</div>
      <div className="space-y-2">
        {contextModeOptions.map((option) => (
          <div key={option.value} className="flex gap-2">
            <span>{option.icon}</span>
            <div>
              <div className="font-medium">{option.label}</div>
              <div className="opacity-75">{option.description}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
